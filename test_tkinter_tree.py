import tkinter as tk
from tkinter import ttk
import sqlite3

db_filepath = 'app.db'
table_name = 'users'

def create(table_name):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            stakeholder_id INTEGER PRIMARY KEY, 
            stakeholder_name TEXT,
            stakeholder_role TEXT
        )'''
    )
    db.commit()
    db.close()

def drop(table_name):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def insert(stakeholder_name, stakeholder_role=''):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO users (stakeholder_name, stakeholder_role) 
        VALUES (?, ?)
    ''', (stakeholder_name, stakeholder_role))
    db.commit()
    db.close()

def delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE stakeholder_id = ?", (id,))
    db.commit()
    db.close()

def get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute("SELECT * FROM users").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def stakeholder_view():
    items = get_all()
    tree.delete(*tree.get_children())
    for item in items:
        row = [val for key, val in item.items()]
        tree.insert("", tk.END, values=list(row))
    
def stakeholder_insert():
    stakeholder_name = text=entry_stakeholder_name.get()
    if stakeholder_name.strip() == '': 
        print('ERR: Stakeholder name NOT valid')
        return
    stakeholder_role = dropdown.get()
    create(table_name)
    insert(stakeholder_name, stakeholder_role)
    stakeholder_view()

# Example:
drop(table_name)
create(table_name)
insert("Alice")
items = get_all()
print(items)
# delete(1)
# get_all()
# drop(table_name)

"""
root = tk.Tk()

tree = ttk.Treeview(root, columns=("id", "name"), show="headings")
tree.pack()

for col in ("id", "name"):
    tree.heading(col, text=col)

for item in items:
    row = [val for key, val in item.items()]
    tree.insert("", tk.END, values=list(row))

entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Insert Stakeholder", command=stakeholder_insert).pack()
"""

###########################################################
# TKINTER
###########################################################


stakeholder_roles = [
    'System Architect', 
    'System Engineer', 
    'CORE Firmware Engineer',
]

root = tk.Tk()
root.geometry("1280x720")

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# TAB 1
tab1 = tk.Frame(tabs)
tabs.add(tab1, text="Records")

frame_left = tk.Frame(tab1, width=200)
frame_left.pack(side="left", fill="y")
frame_left.pack_propagate(False)

padx = 10
tk.Label(frame_left, text="Stakeholder Name").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_name = tk.Entry(frame_left)
entry_stakeholder_name.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Role").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
# entry_stakeholder_role = tk.Entry(frame_left)
# entry_stakeholder_role.pack(fill="x", padx=(padx, padx))
dropdown = ttk.Combobox(frame_left, values=stakeholder_roles)
dropdown.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Category").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_category = tk.Entry(frame_left)
entry_stakeholder_category.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Purpose").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_purpose = tk.Entry(frame_left)
entry_stakeholder_purpose.pack(fill="x", padx=(padx, padx))


tk.Button(frame_left, text="Insert Stakeholder", command=stakeholder_insert).pack(fill="x", padx=(padx, padx), pady=(10, 0))

frame_center = tk.Frame(tab1)
frame_center.pack(side="left", fill="both", expand=True)

cols = [
    "stakeholder_id", 
    "stakeholder_name",
    "stakeholder_role",
    "stakeholder_category",
    "stakeholder_purpose",
]

tree = ttk.Treeview(frame_center, columns=cols, show="headings")
tree.pack(fill="both", expand=True)

for col in cols:
    tree.heading(col, text=col)

stakeholder_view()

# TAB 2
tab2 = tk.Frame(tabs)
tabs.add(tab2, text="Settings")

tk.Label(tab2, text="Settings").pack(pady=20)

ttk.Combobox(
    tab2,
    values=["Option 1", "Option 2", "Option 3"]
).pack()

tk.Button(tab2, text="Save").pack(pady=20)

root.mainloop()