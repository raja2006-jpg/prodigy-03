import tkinter as tk
from tkinter import messagebox, simpledialog
import json

contacts = []

def load_contacts():
    global contacts
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
            update_listbox()
    except FileNotFoundError:
        contacts = []

def save_contacts():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)
    messagebox.showinfo("Saved", "Contacts saved successfully!")

def update_listbox():
    listbox.delete(0, tk.END)
    for contact in contacts:
        listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name and phone and email:
        contacts.append({"name": name, "phone": phone, "email": email})
        update_listbox()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def edit_contact():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        contact = contacts[index]

        new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact['name'])
        new_phone = simpledialog.askstring("Edit Phone", "Enter new phone:", initialvalue=contact['phone'])
        new_email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact['email'])

        if new_name and new_phone and new_email:
            contacts[index] = {"name": new_name, "phone": new_phone, "email": new_email}
            update_listbox()
    else:
        messagebox.showwarning("Select Contact", "Please select a contact to edit.")

def delete_contact():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        del contacts[index]
        update_listbox()
    else:
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")

# GUI Setup
root = tk.Tk()
root.title("Contact Manager GUI")

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Phone").grid(row=1, column=0)
tk.Label(root, text="Email").grid(row=2, column=0)

name_entry = tk.Entry(root)
phone_entry = tk.Entry(root)
email_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
phone_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1)

tk.Button(root, text="Add Contact", command=add_contact).grid(row=3, column=0, pady=5)
tk.Button(root, text="Edit Selected", command=edit_contact).grid(row=3, column=1)
tk.Button(root, text="Delete Selected", command=delete_contact).grid(row=4, column=0)
tk.Button(root, text="Save Contacts", command=save_contacts).grid(row=4, column=1)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=5, column=0, columnspan=2, pady=10)

load_contacts()

root.mainloop()