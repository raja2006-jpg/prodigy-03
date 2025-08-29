import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from tkinter import font
from tkinter import ttk
import ttkbootstrap as tb

contacts = []

def load_contacts():
    global contacts
    try:
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
            update_listbox()
    except FileNotFoundError:
        contacts = []
        
def show_status(msg):
    status_var.set(msg)
    status_bar.update_idletasks()

def save_contacts():
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)
    show_status("Contacts saved successfully!")
    messagebox.showinfo("Saved", "Contacts saved successfully!")

def truncate(text, length):
    return text[:length-3] + '...' if len(text) > length else text
def update_listbox():
    contact_listbox.delete(0, tk.END)
    for contact in contacts:
        name = truncate(contact['name'], 20)
        phone = truncate(contact['phone'], 20)
        email = truncate(contact['email'], 25)
        contact_listbox.insert(tk.END, f"{name:<20} | {phone:<20} | {email:<25}")

def is_valid_phone(phone):
    return phone.isdigit()

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    if not is_valid_phone(phone):
        show_status("Phone number must contain only digits!")
        messagebox.showwarning("Input Error", "Phone number must contain only digits!")
        return
    if name and phone and email:
        contacts.append({"name": name, "phone": phone, "email": email})
        update_listbox()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        show_status(f"Contact '{name}' added.")
    else:
        show_status("Please fill all fields!")
        messagebox.showwarning("Input Error", "Please fill all fields!")

def edit_contact():
    selected = contact_listbox.curselection()
    if selected:
        index = selected[0]
        contact = contacts[index]
        new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact['name'])
        new_phone = simpledialog.askstring("Edit Phone", "Enter new phone:", initialvalue=contact['phone'])
        new_email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact['email'])
        if not is_valid_phone(new_phone):
            show_status("Phone number must contain only digits!")
            messagebox.showwarning("Input Error", "Phone number must contain only digits!")
            return
        if new_name and new_phone and new_email:
            contacts[index] = {"name": new_name, "phone": new_phone, "email": new_email}
            update_listbox()
            show_status(f"Contact '{new_name}' updated.")
    else:
        show_status("Select a contact to edit.")
        messagebox.showwarning("Select Contact", "Please select a contact to edit.")

def delete_contact():
    selected = contact_listbox.curselection()
    if selected:
        index = selected[0]
        name = contacts[index]['name']
        del contacts[index]
        update_listbox()
        show_status(f"Contact '{name}' deleted.")
    else:
        show_status("Select a contact to delete.")
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")

# Color theme
PRIMARY_BG = "#2563eb"      # Blue
ACCENT_BG = "#38bdf8"       # Teal
TITLE_BG = "#1e293b"        # Dark blue
TITLE_FG = "#f1f5f9"        # Light
INPUT_BG = "#e0e7ff"        # Light blue
BUTTON_BG = "#2563eb"
BUTTON_FG = "#f1f5f9"
STATUS_BG = "#38bdf8"
LISTBOX_BG = "#f1f5f9"
LISTBOX_SELECT = "#bae6fd"

# Button colors
ADD_BG = "#22c55e"      # Green
EDIT_BG = "#f59e42"     # Orange
DELETE_BG = "#ef4444"   # Red
SAVE_BG = BUTTON_BG      # Blue
BTN_FG = BUTTON_FG
BTN_ACTIVE = ACCENT_BG

# GUI Setup
root = tk.Tk()
root.title("Contact Manager GUI")
root.minsize(480, 400)
root.configure(bg=PRIMARY_BG)

# Set a professional font
header_font = font.Font(family="Segoe UI", size=16, weight="bold")
label_font = font.Font(family="Segoe UI", size=10)
# Use monospaced font for contact listbox
mono_font = font.Font(family="Consolas", size=10)

# Title label
title_label = tk.Label(root, text="Contact Manager", font=header_font, fg=TITLE_FG, bg=TITLE_BG, pady=8)
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 15), sticky="ew")

# Input frame with visible outline and rounded corners
input_frame = tk.Frame(root, padx=10, pady=10, bg=INPUT_BG, highlightbackground=ACCENT_BG, highlightthickness=3, bd=3, relief=tk.GROOVE)
input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

# Input labels and entries
name_label = tk.Label(input_frame, text="Name", font=label_font, bg=INPUT_BG)
phone_label = tk.Label(input_frame, text="Phone", font=label_font, bg=INPUT_BG)
email_label = tk.Label(input_frame, text="Email", font=label_font, bg=INPUT_BG)

# Phone entry validation: only digits allowed
vcmd = (root.register(lambda P: P.isdigit() or P == ""), '%P')

name_entry = tk.Entry(input_frame, width=25, bg=LISTBOX_BG, relief=tk.FLAT)
phone_entry = tk.Entry(input_frame, width=25, bg=LISTBOX_BG, relief=tk.FLAT, validate='key', validatecommand=vcmd)
email_entry = tk.Entry(input_frame, width=25, bg=LISTBOX_BG, relief=tk.FLAT)

# Bind Enter key for smooth navigation
name_entry.bind('<Return>', lambda e: phone_entry.focus_set())
phone_entry.bind('<Return>', lambda e: email_entry.focus_set())
email_entry.bind('<Return>', lambda e: add_contact())

name_label.grid(row=0, column=0, sticky="w", pady=2)
name_entry.grid(row=0, column=1, pady=2, padx=(0, 10))
phone_label.grid(row=1, column=0, sticky="w", pady=2)
phone_entry.grid(row=1, column=1, pady=2, padx=(0, 10))
email_label.grid(row=2, column=0, sticky="w", pady=2)
email_entry.grid(row=2, column=1, pady=2, padx=(0, 10))

# Separator for visual separation
separator = ttk.Separator(root, orient='horizontal')
separator.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))

# Button frame
button_frame = tk.Frame(root, bg=ACCENT_BG, padx=8, pady=8, highlightbackground=PRIMARY_BG, highlightthickness=2)
button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10), padx=10, sticky="ew")

# Button style using ttkbootstrap for rounded corners and custom colors
add_btn = tb.Button(button_frame, text="➕ Add", command=add_contact, bootstyle="success", width=12)
edit_btn = tb.Button(button_frame, text="✏️ Edit", command=edit_contact, bootstyle="warning", width=12)
delete_btn = tb.Button(button_frame, text="🗑️ Delete", command=delete_contact, bootstyle="danger", width=12)
save_btn = tb.Button(button_frame, text="💾 Save", command=save_contacts, bootstyle="primary", width=12)

add_btn.grid(row=0, column=0, padx=8)
edit_btn.grid(row=0, column=1, padx=8)
delete_btn.grid(row=0, column=2, padx=8)
save_btn.grid(row=0, column=3, padx=8)

# Contact headings
contact_headings_frame = tk.Frame(root, bg=PRIMARY_BG)
contact_headings_frame.grid(row=4, column=0, columnspan=3, padx=10, sticky="ew")

heading_text = f"{'Name':<20} | {'Phone':<20} | {'Email':<25}"
heading_label = tk.Label(contact_headings_frame, text=heading_text, font=mono_font, bg=PRIMARY_BG, fg=TITLE_FG, anchor="w")
heading_label.grid(row=0, column=0, sticky="ew")

# Single listbox for all contact details
contact_listbox_frame = tk.Frame(root, bg=PRIMARY_BG)
contact_listbox_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

contact_listbox = tk.Listbox(contact_listbox_frame, width=65, height=10, font=mono_font, bg=LISTBOX_BG, relief=tk.RIDGE, bd=2, selectbackground=LISTBOX_SELECT, highlightbackground=ACCENT_BG, highlightthickness=2)
contact_listbox.grid(row=0, column=0, sticky="nsew")

contact_listbox_frame.grid_rowconfigure(0, weight=1)
contact_listbox_frame.grid_columnconfigure(0, weight=1)

# Status bar
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor="w", font=("Segoe UI", 9), bg=STATUS_BG, fg=TITLE_BG)
status_bar.grid(row=6, column=0, columnspan=3, sticky="ew", padx=0, pady=(0, 0))
show_status("Ready.")

# Make window responsive
for i in range(3):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(5, weight=1)

load_contacts()

root.mainloop()
