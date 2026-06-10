import sqlite3  

conn = sqlite3.connect("phonebook.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")
conn.commit()

def show_menu():
    print("\n--- Phone Book ---")
    print("1. Add contact")
    print("2. View all contacts")
    print("3. Search contact")
    print("4. Delete contact")
    print("5. Modify contact")
    print("6. Exit")

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    print(f"{name} has been added.")

def view_contacts():
    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Phone book is empty.")
    else:
        print("\n--- All Contacts ---")
        for row in rows:
            print(f"[{row[0]}] {row[1]}: {row[2]}")

def search_contact():
    name = input("Enter name to search: ")
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Contact not found.")
    else:
        print("\n--- Search Results ---")
        for row in rows:
            print(f"[{row[0]}] {row[1]}: {row[2]}")

def delete_contact():
    name = input("Enter name of contact to delete: ")
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("No contact found with that name.")
    elif len(rows) == 1:
        row = rows[0]
        confirm = input(f"Found: [{row[0]}] {row[1]}: {row[2]} — Delete? (yes/no): ")
        if confirm.lower() in ("yes", "y"):
            cursor.execute("DELETE FROM contacts WHERE id = ?", (row[0],))
            conn.commit()
            print(f"'{row[1]}' has been deleted.")
        else:
            print("Delete cancelled.")
    else:
        print("\n--- Multiple matches found ---")
        for row in rows:
            print(f"[{row[0]}] {row[1]}: {row[2]}")
        try:
            entry_id = int(input("\nEnter the ID number of the contact to delete: "))
            cursor.execute("SELECT name FROM contacts WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            if row:
                confirm = input(f"Are you sure you want to delete '{row[0]}'? (yes/no): ")
                if confirm.lower() in ("yes", "y"):
                    cursor.execute("DELETE FROM contacts WHERE id = ?", (entry_id,))
                    conn.commit()
                    print(f"'{row[0]}' has been deleted.")
                else:
                    print("Delete cancelled.")
            else:
                print("No contact found with that ID.")
        except ValueError:
            print("Please enter a valid number.")

def modify_contact():
    name = input("Enter name of contact to modify: ")
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("No contact found with that name.")
    elif len(rows) == 1:
        row = rows[0]
        print(f"Current details — Name: {row[1]}, Phone: {row[2]}")
        new_name = input(f"Enter new name (or press Enter to keep '{row[1]}'): ")
        new_phone = input(f"Enter new phone (or press Enter to keep '{row[2]}'): ")
        if new_name == "":
            new_name = row[1]
        if new_phone == "":
            new_phone = row[2]
        cursor.execute("UPDATE contacts SET name = ?, phone = ? WHERE id = ?", (new_name, new_phone, row[0]))
        conn.commit()
        print("Contact updated successfully.")
    else:
        print("\n--- Multiple matches found ---")
        for row in rows:
            print(f"[{row[0]}] {row[1]}: {row[2]}")
        try:
            entry_id = int(input("\nEnter the ID number of the contact to modify: "))
            cursor.execute("SELECT id, name, phone FROM contacts WHERE id = ?", (entry_id,))
            row = cursor.fetchone()
            if row:
                print(f"Current details — Name: {row[1]}, Phone: {row[2]}")
                new_name = input(f"Enter new name (or press Enter to keep '{row[1]}'): ")
                new_phone = input(f"Enter new phone (or press Enter to keep '{row[2]}'): ")
                if new_name == "":
                    new_name = row[1]
                if new_phone == "":
                    new_phone = row[2]
                cursor.execute("UPDATE contacts SET name = ?, phone = ? WHERE id = ?", (new_name, new_phone, entry_id))
                conn.commit()
                print("Contact updated successfully.")
            else:
                print("No contact found with that ID.")
        except ValueError:
            print("Please enter a valid number.")

while True:
    show_menu()
    choice = input("\nEnter your choice (1-6): ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        modify_contact()
    elif choice == "6":
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Please enter 1-6.")