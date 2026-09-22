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
            stakeholder_name_first TEXT,
            stakeholder_name_last TEXT,
            stakeholder_role TEXT,
            stakeholder_category TEXT,
            stakeholder_purpose TEXT
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

def insert(
    stakeholder_name_first, 
    stakeholder_name_last, 
    stakeholder_role,
    stakeholder_category,
    stakeholder_purpose,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {table_name} (
            stakeholder_name_first, 
            stakeholder_name_last, 
            stakeholder_role,
            stakeholder_category,
            stakeholder_purpose
        ) 
        VALUES (?, ?, ?, ?, ?)
    ''', (
        stakeholder_name_first, 
        stakeholder_name_last, 
        stakeholder_role,
        stakeholder_category,
        stakeholder_purpose,
    ))
    db.commit()
    db.close()

def delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE stakeholder_id = ?", (id,))
    db.commit()
    db.close()

def get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
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
    stakeholder_name_first = text=entry_stakeholder_name_first.get()
    stakeholder_name_last = text=entry_stakeholder_name_last.get()
    stakeholder_role = dropdown.get()
    stakeholder_category = text=entry_stakeholder_category.get()
    stakeholder_purpose = text=entry_stakeholder_purpose.get()
    if stakeholder_name_first.strip() == '': 
        print('ERR: Stakeholder name NOT valid')
        return
    create(table_name)
    insert(
        stakeholder_name_first, 
        stakeholder_name_last, 
        stakeholder_role,
        stakeholder_category,
        stakeholder_purpose,
    )
    
    stakeholder_view()

def stakeholder_delete(event):
    print('here')
    if not tree.selection():
        return
    item = tree.selection()[0]
    id = tree.item(item)["values"][0]
    delete(id)
    tree.delete(item)
    stakeholder_view()

# Example:
# drop(table_name)
create(table_name)
# insert("Alice")
# items = get_all()
# print(items)
# delete(1)
# get_all()
# drop(table_name)


###########################################################
# TKINTER
###########################################################


root = tk.Tk()
root.geometry("1280x720")

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

###########################################################
# TAB 1
###########################################################

stakeholder_roles = [
    'System Architect', 
    'System Engineer', 
    'CORE Firmware Engineer',
]

tab1 = tk.Frame(tabs)
tabs.add(tab1, text="Stakeholders")

frame_left = tk.Frame(tab1, width=200)
frame_left.pack(side="left", fill="y")
frame_left.pack_propagate(False)

padx = 10
tk.Label(frame_left, text="Stakeholder First Nane").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_name_first = tk.Entry(frame_left)
entry_stakeholder_name_first.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Last Name").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_name_last = tk.Entry(frame_left)
entry_stakeholder_name_last.pack(fill="x", padx=(padx, padx))

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
    "stakeholder_name_first",
    "stakeholder_name_last",
    "stakeholder_role",
    "stakeholder_category",
    "stakeholder_purpose",
]

tree = ttk.Treeview(frame_center, columns=cols, show="headings")
tree.pack(fill="both", expand=True)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=1)

stakeholder_view()

###########################################################
# TAB 2
###########################################################
tab2 = tk.Frame(tabs)
tabs.add(tab2, text="Questions")

tk.Label(tab2, text="Settings").pack(pady=20)

ttk.Combobox(
    tab2,
    values=["Option 1", "Option 2", "Option 3"]
).pack()

tk.Button(tab2, text="Save").pack(pady=20)

###########################################################
# TAB 3
###########################################################
tab3 = tk.Frame(tabs)
tabs.add(tab3, text="Answers")

if tabs.nametowidget(tabs.select()) == tab1:
    tree.bind("<Delete>", stakeholder_delete)

def stakeholder_select(event):
    if not tree.selection():
        return

    values = tree.item(tree.selection()[0])["values"]

    entry_stakeholder_name_first.delete(0, tk.END)
    entry_stakeholder_name_first.insert(0, values[1])

    entry_stakeholder_name_last.delete(0, tk.END)
    entry_stakeholder_name_last.insert(0, values[2])

    dropdown.set(values[3])

    entry_stakeholder_category.delete(0, tk.END)
    entry_stakeholder_category.insert(0, values[4])

    entry_stakeholder_purpose.delete(0, tk.END)
    entry_stakeholder_purpose.insert(0, values[5])

tree.bind("<<TreeviewSelect>>", stakeholder_select)

def stakeholder_update():
    item = tree.selection()[0]
    id = tree.item(item)["values"][0]

    db = sqlite3.connect(db_filepath)
    db.execute("""
        UPDATE users
        SET 
            stakeholder_name_first=?, 
            stakeholder_name_last=?, 
            stakeholder_role=?,
            stakeholder_category=?,
            stakeholder_purpose=?
        WHERE stakeholder_id=?
    """, (
        entry_stakeholder_name_first.get(),
        entry_stakeholder_name_last.get(),
        dropdown.get(),
        entry_stakeholder_category.get(),
        entry_stakeholder_purpose.get(),
        id
    ))
    db.commit()
    db.close()

    stakeholder_view()

tk.Button(
    frame_left,
    text="Update",
    command=stakeholder_update
).pack(fill="x", padx=padx, pady=10)

root.mainloop()