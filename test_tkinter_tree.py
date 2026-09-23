import tkinter as tk
from tkinter import ttk
import sqlite3

db_filepath = 'app.db'
table_name = 'users'
questions_table_name = 'questions'

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
    
def sql_stakeholder_get_by_id(stakeholder_id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f'''
        SELECT * 
        FROM {table_name}
        WHERE stakeholder_id = {stakeholder_id}
    ''').fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item
    
def sql_questions_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {questions_table_name} (
            question_id INTEGER PRIMARY KEY, 
            question_text TEXT,
            stakeholder_id INTEGER
        )'''
    )
    db.commit()
    db.close()

def sql_questions_insert(
    question_text, 
    stakeholder_id, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {questions_table_name} (
            question_text,
            stakeholder_id
        ) 
        VALUES (?, ?)
    ''', (
        question_text, 
        stakeholder_id, 
    ))
    db.commit()
    db.close()

def sql_questions_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {questions_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items


def sql_questions_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {questions_table_name} 
        WHERE question_id = ?
    ''', (id,))
    db.commit()
    db.close()

def sql_questions_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {questions_table_name}
    ''')
    db.commit()
    db.close()




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


def questions_view():
    items = sql_questions_get_all()
    questions_tree.delete(*questions_tree.get_children())
    rows = []
    for item in items:
        row = [val for key, val in item.items()]
        rows.append(row)
    for row in rows:
        stakeholder_id = row[2]
        stakeholder_item = sql_stakeholder_get_by_id(stakeholder_id)
        stakeholder = f'''{stakeholder_item['stakeholder_role']} - {stakeholder_item['stakeholder_name_first']} {stakeholder_item['stakeholder_name_last']}'''
        row.append(stakeholder)
        questions_tree.insert("", tk.END, values=list(row))

def question_insert():
    questions_question_text = questions_entry_question_text.get()
    questions_stakeholder_val = questions_combobox_stakeholder.get()
    questions_stakeholder_id = questions_stakeholder_val.split('(')[0].strip()
    if questions_question_text.strip() == '': 
        print('ERR: Question text NOT valid')
        return
    sql_questions_insert(
        questions_question_text,
        questions_stakeholder_id,
    )
    
    questions_view()

def questions_delete(event):
    print('here')
    if not questions_tree.selection():
        return
    item = questions_tree.selection()[0]
    id = questions_tree.item(item)["values"][0]
    sql_questions_delete(id)
    questions_tree.delete(item)
    questions_view()



# Example:
# drop(table_name)
create(table_name)
# sql_questions_drop()
sql_questions_create()
# sql_questions_insert('test')
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
tk.Label(frame_left, text="Stakeholder First Name").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
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

# if tabs.nametowidget(tabs.select()) == tab1:
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
    db.execute(f"""
        UPDATE {table_name}
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

###########################################################
# TAB 2
###########################################################
questions_tab = tk.Frame(tabs)
tabs.add(questions_tab, text="Questions")

questions_frame_left = tk.Frame(questions_tab, width=200)
questions_frame_left.pack(side="left", fill="y")
questions_frame_left.pack_propagate(False)

padx = 10
tk.Label(questions_frame_left, text="Question Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
questions_entry_question_text = tk.Entry(questions_frame_left)
questions_entry_question_text.pack(fill="x", padx=(padx, padx))

# questions_combobox_stakeholder_values = []
# stakeholders_items = get_all()
# for stakeholders_item in stakeholders_items:
#     questions_combobox_stakeholder_value = f
#     questions_combobox_stakeholder_values.append()
#     print(stakeholders_item)
# quit()

questions_combobox_stakeholder_values = [f'''{item['stakeholder_id']} ({item['stakeholder_role']} - {item['stakeholder_name_first']} {item['stakeholder_name_last']})''' for item in get_all()]
tk.Label(questions_frame_left, text="Question Stakeholder ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
questions_combobox_stakeholder = ttk.Combobox(
    questions_frame_left, 
    values=questions_combobox_stakeholder_values
)
questions_combobox_stakeholder.pack(fill="x", padx=(padx, padx))

questions_frame_center = tk.Frame(questions_tab)
questions_frame_center.pack(side="left", fill="both", expand=True)

tk.Button(questions_frame_left, text="Insert Question", command=question_insert).pack(fill="x", padx=(padx, padx), pady=(10, 0))

questions_fields = [
    "question_id", 
    "question_text",
    "stakeholder_id",
    "stakeholder",
]

questions_tree = ttk.Treeview(
    questions_frame_center, 
    columns=questions_fields, 
    show="headings"
)
questions_tree.pack(fill="both", expand=True)

for col in questions_fields:
    questions_tree.heading(col, text=col)
    questions_tree.column(col, width=1)

questions_view()

# if tabs.nametowidget(tabs.select()) == questions_tab:
questions_tree.bind("<Delete>", questions_delete)

    
def questions_select(event):
    if not questions_tree.selection():
        return

    values = questions_tree.item(questions_tree.selection()[0])["values"]

    questions_entry_question_text.delete(0, tk.END)
    questions_entry_question_text.insert(0, values[1])

    stakeholder_id = values[2]
    stakeholder_item = sql_stakeholder_get_by_id(stakeholder_id)
    stakeholder = f'''{stakeholder_id} ({stakeholder_item['stakeholder_role']} - {stakeholder_item['stakeholder_name_first']} {stakeholder_item['stakeholder_name_last']})'''

    questions_combobox_stakeholder.set(stakeholder)

questions_tree.bind("<<TreeviewSelect>>", questions_select)

def questions_update():
    item = questions_tree.selection()[0]
    
    questions_id = questions_tree.item(item)["values"][0]
    questions_question_text = questions_entry_question_text.get()
    questions_stakeholder_val = questions_combobox_stakeholder.get()
    questions_stakeholder_id = questions_stakeholder_val.split('(')[0].strip()
    if questions_question_text.strip() == '': 
        print('ERR: Question text NOT valid')
        return

    db = sqlite3.connect(db_filepath)
    db.execute(f"""
        UPDATE {questions_table_name}
        SET 
            question_text=?, 
            stakeholder_id=?
        WHERE question_id=?
    """, (
        questions_question_text,
        questions_stakeholder_id,
        questions_id
    ))
    db.commit()
    db.close()

    questions_view()

tk.Button(
    questions_frame_left,
    text="Update",
    command=questions_update
).pack(fill="x", padx=padx, pady=10)

###########################################################
# TAB 3
###########################################################
tab3 = tk.Frame(tabs)
tabs.add(tab3, text="Answers")


root.mainloop()