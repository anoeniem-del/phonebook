import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
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

# ---- MAIN WINDOW ----

root = tk.Tk()
root.title("Phone Book")
root.geometry("600x500")
root.iconbitmap("book30.ico")

# ---- SEARCH BAR ----

search_frame = ttk.Frame(root)
search_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
entry_search = ttk.Entry(search_frame, width=30)
entry_search.grid(row=0, column=1, padx=5)
ttk.Button(search_frame, text="Search", command=lambda: search_contact()).grid(row=0, column=2, padx=5)
ttk.Button(search_frame, text="Show All", command=lambda: load_contacts()).grid(row=0, column=3, padx=5)

# ---- ADD CONTACT FORM ----

form_frame = ttk.LabelFrame(root, text="Add New Contact")
form_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = ttk.Entry(form_frame, width=25)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Phone:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_phone = ttk.Entry(form_frame, width=20)
entry_phone.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(form_frame, text="Add Contact", command=lambda: add_contact()).grid(row=0, column=4, padx=10, pady=5)

# ---- CONTACT LIST ----

list_frame = ttk.LabelFrame(root, text="Contacts")
list_frame.pack(fill="both", expand=True, padx=10, pady=5)

contact_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Phone"), show="headings")
contact_tree.heading("ID", text="ID")
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone Number")
contact_tree.column("ID", width=50)
contact_tree.column("Name", width=250)
contact_tree.column("Phone", width=200)
contact_tree.pack(fill="both", expand=True, padx=5, pady=5)

btn_frame = ttk.Frame(list_frame)
btn_frame.pack(pady=5)

ttk.Button(btn_frame, text="Modify Contact", command=lambda: modify_contact()).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Delete Contact", command=lambda: delete_contact()).grid(row=0, column=1, padx=5)
# ---- ALL FUNCTIONS ----

def load_contacts():
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    cursor.execute("SELECT id, name, phone FROM contacts ORDER BY name")
    for row in cursor.fetchall():
        contact_tree.insert("", "end", values=(row[0], row[1], row[2]))

def search_contact():
    search = entry_search.get().strip()
    if not search:
        load_contacts()
        return
    for row in contact_tree.get_children():
        contact_tree.delete(row)
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", (f"%{search}%", f"%{search}%"))
    rows = cursor.fetchall()
    if not rows:
        messagebox.showinfo("Not Found", "No contacts found matching your search.")
    else:
        for row in rows:
            contact_tree.insert("", "end", values=(row[0], row[1], row[2]))

def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    if not name or not phone:
        messagebox.showwarning("Missing Info", "Please fill in both name and phone number.")
        return
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    load_contacts()

def delete_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to delete.")
        return
    item = contact_tree.item(selected[0])
    contact_id = item["values"][0]
    contact_name = item["values"][1]
    confirm = messagebox.askyesno("Confirm Delete", f"Delete '{contact_name}'?")
    if confirm:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        load_contacts()

def modify_contact():
    selected = contact_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a contact to modify.")
        return
    item = contact_tree.item(selected[0])
    contact_id = item["values"][0]
    contact_name = item["values"][1]
    contact_phone = item["values"][2]

    popup = tk.Toplevel(root)
    popup.title(f"Modify Contact - {contact_name}")
    popup.geometry("300x180")
    popup.grab_set()

    ttk.Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_mod_name = ttk.Entry(popup, width=20)
    entry_mod_name.insert(0, contact_name)
    entry_mod_name.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(popup, text="Phone:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_mod_phone = ttk.Entry(popup, width=20)
    entry_mod_phone.insert(0, contact_phone)
    entry_mod_phone.grid(row=1, column=1, padx=10, pady=5)

    def confirm_modify():
        new_name = entry_mod_name.get().strip()
        new_phone = entry_mod_phone.get().strip()
        if not new_name or not new_phone:
            messagebox.showwarning("Missing Info", "Please fill in all fields.", parent=popup)
            return
        cursor.execute("UPDATE contacts SET name = ?, phone = ? WHERE id = ?", (new_name, new_phone, contact_id))
        conn.commit()
        load_contacts()
        popup.destroy()
        messagebox.showinfo("Updated", f"'{contact_name}' has been updated.")

    ttk.Button(popup, text="Save Changes", command=confirm_modify).grid(row=2, column=0, columnspan=2, pady=15)
    # ---- START ----
load_contacts()
root.mainloop()