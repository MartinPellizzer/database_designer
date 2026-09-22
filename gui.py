
import sqlite3
import tkinter as tk
from tkinter import ttk

db_filepath = 'app.db'
table_name = 'users'

def create(table_name):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            stakeholder_id INTEGER PRIMARY KEY, 
            stakeholder_name TEXT
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

def insert(name):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute("INSERT INTO users (stakeholder_name) VALUES (?)", (name,))
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
    print(items)
    db.close()
    return items

# Example:
drop(table_name)
create(table_name)
insert("Alice")
# get_all()
# delete(1)
# get_all()
drop(table_name)


def show_text():
    label.config(text=entry.get())

def stakeholder_insert():
    stakeholder_name = text=entry.get()
    if stakeholder_name.strip() == '': 
        print('ERR: Stakeholder name NOT valid')
        return
    create(table_name)
    insert(stakeholder_name)
    items = get_all()
    for item in items:
        listbox.insert(tk.END, item)

root = tk.Tk()
root.title("Minimal App")
root.geometry("300x150")

entry = tk.Entry(root)
entry.pack()

tree = ttk.Treeview(root, columns=cols, show="headings")
tree.pack()

tk.Button(root, text="Insert Stakeholder", command=stakeholder_insert).pack()

listbox = tk.Listbox(root)
listbox.pack()

db = sqlite3.connect("app.db")
db.row_factory = sqlite3.Row

rows = db.execute("SELECT * FROM users").fetchall()
cols = rows[0].keys() if rows else []

print(cols)
quit()

tree = ttk.Treeview(root, columns=cols, show="headings")
tree.pack()

for col in cols:
    tree.heading(col, text=col)

for row in rows:
    tree.insert("", tk.END, values=list(row))

root.mainloop()