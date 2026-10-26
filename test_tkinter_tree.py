import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3

from textwrap import dedent

### TODO: change db_filepath based on project
db_filepath = 'test.db'
stakeholders_table_name = 'stakeholders'
questions_table_name = 'questions'
answers_table_name = 'answers'
statements_table_name = 'statements'
requirements_table_name = 'requirements'
categories_table_name = 'categories'
categories_requirements_table_name = 'categories_requirements'


requirements_statements_list_cur = []

db = None
project_file = None


stakeholder_roles = [
    'System Architect', 
    'System Engineer', 
    'CORE Firmware Engineer',
    'Electrical Engineer',
    'Process Engineer',
    'Safety Engineer',
]

############################################################
# SQLITE FUNCTIONS
############################################################

sql_stakeholders_fields = [
    {
        "name": "stakeholder_id",
        "type": "INTEGER",
        "primary_key": True,
    },
    {
        "name": "stakeholder_name_first",
        "type": "TEXT",
    },
    {
        "name": "stakeholder_name_last",
        "type": "TEXT",
    },
    {
        "name": "stakeholder_role",
        "type": "TEXT",
    },
    {
        "name": "stakeholder_category",
        "type": "TEXT",
    },
    {
        "name": "stakeholder_purpose",
        "type": "TEXT",
    },
]


"""
def sql_create_table(table_name, fields):
    ###
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = []
    for field in fields:
        column = f"{field['name']} {field['type']}"
        if field.get("primary_key"): column += " PRIMARY KEY"
        if field.get("not_null"): column += " NOT NULL"
        if field.get("unique"): column += " UNIQUE"
        columns.append(column)
    sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {", ".join(columns)}
        )
    '''
    cur.execute(sql)
    db.commit()
    db.close()

sql_create_table(stakeholders_table_name, fields)

def sql_stakeholders_create_table(table_name, fields):
    table_name = stakeholders_table_name
    fields = sql_stakeholders_fields
    ###
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = []
    for field in fields:
        column = f"{field['name']} {field['type']}"
        if field.get("primary_key"): column += " PRIMARY KEY"
        if field.get("not_null"): column += " NOT NULL"
        if field.get("unique"): column += " UNIQUE"
        columns.append(column)
    sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {", ".join(columns)}
        )
    '''
    cur.execute(sql)
    db.commit()
    db.close()

sql_stakeholders_create_table()
"""

# ----------------------------------------------------------
# SQLITE STAKEHOLDERS
# ----------------------------------------------------------

def sql_stakeholders_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {stakeholders_table_name}
    ''')
    db.commit()
    db.close()

def sql_stakeholders_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {stakeholders_table_name} (
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

def sql_stakeholders_insert(
    stakeholder_name_first, 
    stakeholder_name_last, 
    stakeholder_role,
    stakeholder_category,
    stakeholder_purpose,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {stakeholders_table_name} (
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

def sql_stakeholders_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f"DELETE FROM {stakeholders_table_name} WHERE stakeholder_id = ?", (id,))
    db.commit()
    db.close()

def sql_stakeholders_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {stakeholders_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
def sql_stakeholders_get_by_id(stakeholder_id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f'''
        SELECT * 
        FROM {stakeholders_table_name}
        WHERE stakeholder_id = {stakeholder_id}
    ''').fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item
    
# ----------------------------------------------------------
# SQLITE QUESTIONS
# ----------------------------------------------------------

def sql_questions_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {questions_table_name}
    ''')
    db.commit()
    db.close()

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

def sql_questions_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {questions_table_name} 
        WHERE question_id = ?
    ''', (id,))
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
    
def sql_questions_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {questions_table_name}
        WHERE question_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item

# ----------------------------------------------------------
# SQLITE ANSWERS
# ----------------------------------------------------------

def sql_answers_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {answers_table_name}
    ''')
    db.commit()
    db.close()

def sql_answers_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {answers_table_name} (
            answer_id INTEGER PRIMARY KEY, 
            answer_text TEXT,
            question_id INTEGER,
            question_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_answers_insert(
    answer_text, 
    question_id, 
    question_text, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {answers_table_name} (
            answer_text,
            question_id,
            question_text
        ) 
        VALUES (?, ?, ?)
    ''', (
        answer_text, 
        question_id, 
        question_text, 
    ))
    db.commit()
    db.close()

def sql_answers_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {answers_table_name} 
        WHERE answer_id = ?
    ''', (id,))
    db.commit()
    db.close()

def sql_answers_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {answers_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
def sql_answers_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {answers_table_name}
        WHERE answer_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item
    
# ----------------------------------------------------------
# SQLITE STATEMENTS
# ----------------------------------------------------------

def sql_statements_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {statements_table_name}
    ''')
    db.commit()
    db.close()

def sql_statements_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {statements_table_name} (
            statement_id INTEGER PRIMARY KEY, 
            statement_text TEXT,
            answer_id INTEGER,
            answer_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_statements_insert(
    answer_id, 
    answer_text, 
    statement_text, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {statements_table_name} (
        statement_text,
        answer_id,
        answer_text
        ) 
        VALUES (?, ?, ?)
    ''', (
        statement_text,
        answer_id,
        answer_text,
    ))
    db.commit()
    db.close()

def sql_statements_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {statements_table_name} 
        WHERE statement_id = ?
    ''', (id,))
    db.commit()
    db.close()

def sql_statements_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {statements_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
def sql_statements_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {statements_table_name}
        WHERE statement_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item

# sql_statements_drop()
sql_statements_create()

# ----------------------------------------------------------
# SQLITE REQUIREMENTS
# ----------------------------------------------------------

def sql_requirements_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {requirements_table_name}
    ''')
    db.commit()
    db.close()

def sql_requirements_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {requirements_table_name} (
            requirement_id INTEGER PRIMARY KEY, 
            requirement_text TEXT,
            requirements_statements_ids TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_requirements_insert(
    requirement_text, 
    requirements_statements_ids, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {requirements_table_name} (
        requirement_text,
        requirements_statements_ids
        ) 
        VALUES (?, ?)
    ''', (
        requirement_text,
        requirements_statements_ids,
    ))
    db.commit()
    db.close()

def sql_requirements_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {requirements_table_name} 
        WHERE requirement_id = ?
    ''', (id,))
    db.commit()
    db.close()

def sql_requirements_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {requirements_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
def sql_requirements_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {requirements_table_name}
        WHERE requirement_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item

# sql_requirements_drop()
sql_requirements_create()

# ----------------------------------------------------------
# SQLITE CATEGORIES
# ----------------------------------------------------------

def sql_categories_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {categories_table_name}
    ''')
    db.commit()
    db.close()

def sql_categories_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {categories_table_name} (
            category_id INTEGER PRIMARY KEY, 
            category_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_categories_insert(
    category_text, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {categories_table_name} (
        category_text
        ) 
        VALUES (?)
    ''', (
        category_text,
    ))
    db.commit()
    db.close()

def sql_categories_delete(id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {categories_table_name} 
        WHERE category_id = ?
    ''', (id,))
    db.commit()
    db.close()

def sql_categories_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {categories_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
def sql_categories_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {categories_table_name}
        WHERE category_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item

# sql_categories_drop()
sql_categories_create()

# ----------------------------------------------------------
# SQLITE CATEGORIES_REQUIREMENTS
# ----------------------------------------------------------

def sql_categories_requirements_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {categories_requirements_table_name}
    ''')
    db.commit()
    db.close()

def sql_categories_requirements_create():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {categories_requirements_table_name} (
            category_requirement_id INTEGER PRIMARY KEY, 
            category_id TEXT, 
            requirement_id TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_categories_requirements_insert(
    category_id, 
    requirement_id, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {categories_requirements_table_name} (
            category_id,
            requirement_id
        ) 
        VALUES (?, ?)
    ''', (
        category_id,
        requirement_id
    ))
    db.commit()
    db.close()

def sql_categories_requirements_get_all():
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {categories_requirements_table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items
    
    
def sql_categories_requirements_get_by_category_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {categories_requirements_table_name}
        WHERE category_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql_categories_requirements_delete(category_id, requirement_id):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {categories_requirements_table_name} 
        WHERE category_id = ? AND requirement_id = ?
    ''', (category_id, requirement_id))
    db.commit()
    db.close()

# sql_categories_requirements_drop()
# sql_categories_requirements_create()
# sql_categories_requirements_insert(
#     category_id=1, 
#     requirement_id=2, 
# )

############################################################
# TKINTER FUNCTIONS
############################################################

# ----------------------------------------------------------
# TKINTER FUNCTIONS STAKEHOLDERS
# ----------------------------------------------------------

def tk_stakeholder_view():
    items = sql_stakeholders_get_all()
    tree.delete(*tree.get_children())
    for item in items:
        row = [val for key, val in item.items()]
        tree.insert("", tk.END, values=list(row))
    
def tk_stakeholder_insert():
    stakeholder_name_first = text=entry_stakeholder_name_first.get()
    stakeholder_name_last = text=entry_stakeholder_name_last.get()
    stakeholder_role = dropdown.get()
    stakeholder_category = text=entry_stakeholder_category.get()
    stakeholder_purpose = text=entry_stakeholder_purpose.get()
    if stakeholder_name_first.strip() == '': 
        print('ERR: Stakeholder name NOT valid')
        return
    sql_stakeholders_insert(
        stakeholder_name_first, 
        stakeholder_name_last, 
        stakeholder_role,
        stakeholder_category,
        stakeholder_purpose,
    )
    tk_stakeholder_view()
    
def tk_stakeholder_update():
    item = tree.selection()[0]
    id = tree.item(item)["values"][0]
    db = sqlite3.connect(db_filepath)
    db.execute(f"""
        UPDATE {stakeholders_table_name}
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
    tk_stakeholder_view()

def tk_stakeholder_delete(event):
    if not tree.selection(): return
    item = tree.selection()[0]
    id = tree.item(item)["values"][0]
    sql_stakeholders_delete(id)
    tree.delete(item)
    tk_stakeholder_view()

# ----------------------------------------------------------
# TKINTER FUNCTIONS QUESTIONS
# ----------------------------------------------------------

def questions_view():
    items = sql_questions_get_all()
    questions_tree.delete(*questions_tree.get_children())
    rows = []
    for item in items:
        row = [val for key, val in item.items()]
        rows.append(row)
    for row in rows:
        print(row)
        stakeholder_id = row[2]
        stakeholder_item = sql_stakeholders_get_by_id(stakeholder_id)
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

def questions_select(event):
    if not questions_tree.selection():
        return
    values = questions_tree.item(questions_tree.selection()[0])["values"]
    questions_entry_question_text.delete(0, tk.END)
    questions_entry_question_text.insert(0, values[1])
    stakeholder_id = values[2]
    stakeholder_item = sql_stakeholders_get_by_id(stakeholder_id)
    stakeholder = f'''{stakeholder_id} ({stakeholder_item['stakeholder_role']} - {stakeholder_item['stakeholder_name_first']} {stakeholder_item['stakeholder_name_last']})'''
    questions_combobox_stakeholder.set(stakeholder)

    answers_entry_question_id.config(state="normal")
    answers_entry_question_id.delete(0, tk.END)
    answers_entry_question_id.insert(0, values[0])
    answers_entry_question_id.config(state="disabled")

    # answers_entry_question_text.delete(0, tk.END)
    # answers_entry_question_text.insert(0, values[1])

    answers_text_question_text.config(state="normal")
    answers_text_question_text.delete("1.0", tk.END)
    answers_text_question_text.insert("1.0", values[1])
    answers_text_question_text.config(state="disabled")

def questions_delete(event):
    print('here')
    if not questions_tree.selection():
        return
    item = questions_tree.selection()[0]
    id = questions_tree.item(item)["values"][0]
    sql_questions_delete(id)
    questions_tree.delete(item)
    questions_view()

def questions_print():
    for item in questions_tree.get_children():
        print(questions_tree.item(item)["values"][1])

# ----------------------------------------------------------
# TKINTER FUNCTIONS ANSWERS
# ----------------------------------------------------------

def tk_answers_view():
    items = sql_answers_get_all()
    answers_tree.delete(*answers_tree.get_children())
    rows = []
    for item in items:
        row = [val for key, val in item.items()]
        rows.append(row)
    for row in rows:
        # print(row)
        # stakeholder_id = row[2]
        # stakeholder_item = sql_stakeholders_get_by_id(stakeholder_id)
        # stakeholder = f'''{stakeholder_item['stakeholder_role']} - {stakeholder_item['stakeholder_name_first']} {stakeholder_item['stakeholder_name_last']}'''
        # row.append(stakeholder)
        answers_tree.insert("", tk.END, values=list(row))

def tk_answers_insert():
    question_id = answers_entry_question_id.get()
    question_text = answers_text_question_text.get("1.0", tk.END).strip()
    answer_text = answers_text_answer_text.get("1.0", tk.END).strip()

    if question_id.strip() == '': 
        print('ERR: Question id NOT alid')
        return
    if question_text.strip() == '': 
        print('ERR: Question text NOT valid')
        return
    if answer_text.strip() == '': 
        print('ERR: Answer text NOT valid')
        return

    sql_answers_insert(
        answer_text, 
        question_id, 
        question_text,
    )
    tk_answers_view()
    
    answers_entry_question_id.config(state="normal")
    answers_entry_question_id.delete(0, tk.END)
    answers_entry_question_id.config(state="disabled")
    ###
    answers_text_question_text.config(state="normal")
    answers_text_question_text.delete("1.0", tk.END)
    answers_text_question_text.config(state="disabled")
    ###
    answers_text_answer_text.delete("1.0", tk.END)

def tk_answers_update():
    item = answers_tree.selection()[0]
    answer_id = answers_tree.item(item)["values"][0]

    question_id = answers_entry_question_id.get()
    question_text = answers_text_question_text.get("1.0", tk.END).strip()
    answer_text = answers_text_answer_text.get("1.0", tk.END).strip()

    if question_id.strip() == '': 
        print('ERR: ANSWERS -> Question id NOT alid')
        return
    if question_text.strip() == '': 
        print('ERR: ANSWERS -> Question text NOT valid')
        return
    if answer_text.strip() == '': 
        print('ERR: ANSWERS -> Answer text NOT valid')
        return

    db = sqlite3.connect(db_filepath)
    db.execute(f"""
        UPDATE {answers_table_name}
        SET 
            answer_text=?, 
            question_id=?,
            question_text=?
        WHERE answer_id=?
    """, (
        answer_text,
        question_id,
        question_text,
        answer_id,
    ))
    db.commit()
    db.close()
    tk_answers_view()
    
    answers_entry_question_id.config(state="normal")
    answers_entry_question_id.delete(0, tk.END)
    answers_entry_question_id.config(state="disabled")
    ###
    answers_text_question_text.config(state="normal")
    answers_text_question_text.delete("1.0", tk.END)
    answers_text_question_text.config(state="disabled")
    ###
    answers_text_answer_text.delete("1.0", tk.END)

def tk_answers_delete(event):
    if not answers_tree.selection():
        return
    item = answers_tree.selection()[0]
    id = answers_tree.item(item)["values"][0]
    sql_answers_delete(id)
    answers_tree.delete(item)
    tk_answers_view()

def tk_answers_select(event):
    if not answers_tree.selection(): return

    values = answers_tree.item(answers_tree.selection()[0])["values"]

    answers_entry_question_id.config(state="normal")
    answers_entry_question_id.delete(0, tk.END)
    answers_entry_question_id.insert(0, values[0])
    answers_entry_question_id.config(state="disabled")

    answers_text_question_text.config(state="normal")
    answers_text_question_text.delete("1.0", tk.END)
    answers_text_question_text.insert("1.0", values[3])
    answers_text_question_text.config(state="disabled")

    answers_text_answer_text.delete("1.0", tk.END)
    answers_text_answer_text.insert("1.0", values[1])

    
    statements_entry_answer_id.config(state="normal")
    statements_entry_answer_id.delete(0, tk.END)
    statements_entry_answer_id.insert(0, values[0])
    statements_entry_answer_id.config(state="disabled")

    statements_text_answer_text.config(state="normal")
    statements_text_answer_text.delete("1.0", tk.END)
    statements_text_answer_text.insert("1.0", values[1])
    statements_text_answer_text.config(state="disabled")



# ----------------------------------------------------------
# TKINTER FUNCTIONS STATEMENTS
# ----------------------------------------------------------

def tk_statements_view():
    items = sql_statements_get_all()
    statements_tree.delete(*statements_tree.get_children())
    rows = []
    # for item in items:
    #     row = [val for key, val in item.items()]
    #     rows.append(row)
    for item in items:
        # row = [val for key, val in item.items()]
        row = [
            item['statement_id'], 
            item['statement_text'],
            item['answer_id'],
            item['answer_text'],
        ]
        rows.append(row)
    for row in rows:
        statements_tree.insert("", tk.END, values=list(row))
        
    ### COLOR ROWS
    print(requirements_statements_list_cur)
    sql_requirements_items = sql_requirements_get_all()
    ids_lst = set()
    for sql_requirements_item in sql_requirements_items:
        ids_lst_cur = [val.strip() for val in str(sql_requirements_item['requirements_statements_ids']).split(',')]
        for x in ids_lst_cur:
            ids_lst.add(x)

    for item in statements_tree.get_children():
        row_id = statements_tree.item(item, "values")[0]  # ID in first column
        if row_id in requirements_statements_list_cur:
            statements_tree.item(item, tags=("tmp",))
        elif row_id in ids_lst:
            statements_tree.item(item, tags=("done",))
        else:
            statements_tree.item(item, tags=("blank",))

def tk_statements_insert():
    answer_id = statements_entry_answer_id.get()
    answer_text = statements_text_answer_text.get("1.0", tk.END).strip()
    statement_text = statements_text_statement_text.get("1.0", tk.END).strip()
    print(answer_id)
    print(answer_text)
    print(statement_text)
    if answer_id.strip() == '': 
        print('ERR: Question id NOT alid')
        return
    if answer_text.strip() == '': 
        print('ERR: Question text NOT valid')
        return
    if statement_text.strip() == '': 
        print('ERR: Answer text NOT valid')
        return
    sql_statements_insert(
        answer_id, 
        answer_text, 
        statement_text,
    )
    tk_statements_view()
    # statements_entry_answer_id.config(state="normal")
    # statements_entry_answer_id.delete(0, tk.END)
    # statements_entry_answer_id.config(state="disabled")
    ###
    # statements_text_answer_text.config(state="normal")
    # statements_text_answer_text.delete("1.0", tk.END)
    # statements_text_answer_text.config(state="disabled")
    ###
    statements_text_statement_text.delete("1.0", tk.END)

def tk_statements_update():
    item = statements_tree.selection()[0]
    statement_id = statements_tree.item(item)["values"][0]

    answer_id = statements_entry_answer_id.get()
    answer_text = statements_text_answer_text.get("1.0", tk.END).strip()
    statement_text = statements_text_statement_text.get("1.0", tk.END).strip()

    if answer_id.strip() == '': 
        print('ERR: ANSWERS -> Question id NOT alid')
        return
    if answer_text.strip() == '': 
        print('ERR: ANSWERS -> Question text NOT valid')
        return
    if statement_text.strip() == '': 
        print('ERR: ANSWERS -> Answer text NOT valid')
        return

    db = sqlite3.connect(db_filepath)
    db.execute(f"""
        UPDATE {statements_table_name}
        SET 
            answer_id=?, 
            answer_text=?,
            statement_text=?
        WHERE statement_id=?
    """, (
        answer_id,
        answer_text,
        statement_text,
        statement_id,
    ))
    db.commit()
    db.close()
    tk_statements_view()
    
    # answers_entry_question_id.config(state="normal")
    # answers_entry_question_id.delete(0, tk.END)
    # answers_entry_question_id.config(state="disabled")
    # ###
    # answers_text_question_text.config(state="normal")
    # answers_text_question_text.delete("1.0", tk.END)
    # answers_text_question_text.config(state="disabled")
    ###
    statements_text_statement_text.delete("1.0", tk.END)

def tk_statements_delete(event):
    if not statements_tree.selection(): return
    item = statements_tree.selection()[0]
    id = statements_tree.item(item)["values"][0]
    sql_statements_delete(id)
    statements_tree.delete(item)
    tk_statements_view()

def tk_statements_select(event):
    if not statements_tree.selection(): return
    values = statements_tree.item(statements_tree.selection()[0])["values"]

    statements_entry_answer_id.config(state="normal")
    statements_entry_answer_id.delete(0, tk.END)
    statements_entry_answer_id.insert(0, values[2])
    statements_entry_answer_id.config(state="disabled")

    statements_text_answer_text.config(state="normal")
    statements_text_answer_text.delete("1.0", tk.END)
    statements_text_answer_text.insert("1.0", values[3])
    statements_text_answer_text.config(state="disabled")

    statements_text_statement_text.delete("1.0", tk.END)
    statements_text_statement_text.insert("1.0", values[1])

    requirements_entry_statement_id.config(state="normal")
    requirements_entry_statement_id.delete(0, tk.END)
    requirements_entry_statement_id.insert(0, values[0])
    requirements_entry_statement_id.config(state="disabled")

    requirements_text_statement_text.config(state="normal")
    requirements_text_statement_text.delete("1.0", tk.END)
    requirements_text_statement_text.insert("1.0", values[1])
    requirements_text_statement_text.config(state="disabled")



# ----------------------------------------------------------
# TKINTER FUNCTIONS REQUIREMENTS
# ----------------------------------------------------------

def tk_requirements_view(items=None):
    if not items:
        items = sql_requirements_get_all()
    # for item in items:
    #     print(item)
    items = sorted(items, key=lambda x: x['sort_order'])
    requirements_tree.delete(*requirements_tree.get_children())
    rows = []
    for item in items:
        row = [
            item['requirement_id'], 
            item['requirement_text'],
            item['requirements_statements_ids'],
        ]
        rows.append(row)
    for row in rows:
        requirements_tree.insert("", tk.END, values=list(row))

def tk_requirements_insert():
    global requirements_statements_list_cur
    # statement_id = requirements_entry_statement_id.get()
    requirement_text = requirements_text_requirement_text.get("1.0", tk.END).strip()
    requirements_statements_ids = ','.join(requirements_listbox.get(0, tk.END))
    # if statement_id.strip() == '': 
    #     print('ERR: statement_id id NOT valid')
    #     return
    if requirement_text.strip() == '': 
        print('ERR: statement_text text NOT valid')
        return
    if requirements_statements_ids.strip() == '': 
        print('ERR: requirements_statements_ids text NOT valid')
        return
    sql_requirements_insert(
        requirement_text, 
        requirements_statements_ids,
    )
    tk_requirements_view()
    # statements_entry_answer_id.config(state="normal")
    # statements_entry_answer_id.delete(0, tk.END)
    # statements_entry_answer_id.config(state="disabled")
    ###
    # statements_text_answer_text.config(state="normal")
    # statements_text_answer_text.delete("1.0", tk.END)
    # statements_text_answer_text.config(state="disabled")
    ###
    requirements_listbox.delete(0, tk.END)
    requirements_text_requirement_text.delete("1.0", tk.END)

    requirements_statements_list_cur = []
    tk_statements_view()

def tk_requirements_update():
    global requirements_statements_list_cur
    requirement_item = requirements_tree.selection()[0]
    requirement_id = requirements_tree.item(requirement_item)["values"][0]

    # statement_id = requirements_entry_statement_id.get()
    requirement_text = requirements_text_requirement_text.get("1.0", tk.END).strip()
    requirements_statements_ids = ','.join(requirements_listbox.get(0, tk.END))
    # if statement_id.strip() == '': 
    #     print('ERR: statement_id id NOT valid')
    #     return
    if requirement_text.strip() == '': 
        print('ERR: statement_text text NOT valid')
        return
    if requirements_statements_ids.strip() == '': 
        print('ERR: requirements_statements_ids text NOT valid')
        return
    
    db = sqlite3.connect(db_filepath)
    db.execute(f"""
        UPDATE {requirements_table_name}
        SET 
            requirement_text=?,
            requirements_statements_ids=?
        WHERE requirement_id=?
    """, (
        requirement_text,
        requirements_statements_ids,
        requirement_id,
    ))
    db.commit()
    db.close()

    tk_requirements_view()
    # statements_entry_answer_id.config(state="normal")
    # statements_entry_answer_id.delete(0, tk.END)
    # statements_entry_answer_id.config(state="disabled")
    ###
    # statements_text_answer_text.config(state="normal")
    # statements_text_answer_text.delete("1.0", tk.END)
    # statements_text_answer_text.config(state="disabled")
    ###
    requirements_listbox.delete(0, tk.END)
    requirements_text_requirement_text.delete("1.0", tk.END)

    requirements_statements_list_cur = []
    tk_statements_view()

def tk_requirements_delete(event):
    global requirements_statements_list_cur
    if not requirements_tree.selection(): return
    item = requirements_tree.selection()[0]
    id = requirements_tree.item(item)["values"][0]
    ###
    sql_requirements_delete(id)
    requirements_tree.delete(item)
    tk_requirements_view()
    requirements_listbox.delete(0, tk.END)
    requirements_text_requirement_text.delete("1.0", tk.END)
    requirements_statements_list_cur = []
    tk_statements_view()

def tk_requirements_select(event):
    global requirements_statements_list_cur
    if not requirements_tree.selection(): return
    values = requirements_tree.item(requirements_tree.selection()[0])["values"]
    ids_lst = [val.strip() for val in str(values[2]).split(',')]

    # requirements_entry_statement_id.config(state="normal")
    # requirements_entry_statement_id.delete(0, tk.END)
    # requirements_entry_statement_id.insert(0, values[2])
    # requirements_entry_statement_id.config(state="disabled")

    # requirements_text_statement_text.config(state="normal")
    # requirements_text_statement_text.delete("1.0", tk.END)
    # requirements_text_statement_text.insert("1.0", values[3])
    # requirements_text_statement_text.config(state="disabled")

    requirements_listbox.delete(0, tk.END)  # Clear all items
    for item in ids_lst:
        requirements_listbox.insert(tk.END, item)

    requirements_text_requirement_text.delete("1.0", tk.END)
    requirements_text_requirement_text.insert("1.0", values[1])
    requirements_statements_list_cur = []
    tk_statements_view()

    ###
    statements_items = []
    for statement_id in ids_lst:
        statement_item = sql_statements_get_by_id(statement_id)
        statements_items.append(statement_item)
    tk_requirements_statements_view(statements_items)
    
    requirement_item = sql_requirements_get_by_id(values[0])

    categories_entry_requirement_id.config(state="normal")
    categories_entry_requirement_id.delete(0, tk.END)
    categories_entry_requirement_id.insert(0, values[0])
    categories_entry_requirement_id.config(state="disabled")

    categories_text_requirement_text.config(state="normal")
    categories_text_requirement_text.delete("1.0", tk.END)
    categories_text_requirement_text.insert("1.0", values[1])
    categories_text_requirement_text.config(state="disabled")
    # print(requirement_item)

def tk_requirements_statements_view(statements_items):
    items = statements_items
    requirements_statements_tree.delete(*requirements_statements_tree.get_children())
    rows = []
    for item in items:
        row = [
            item['statement_id'], 
            item['statement_text'],
        ]
        rows.append(row)
    for row in rows:
        requirements_statements_tree.insert("", tk.END, values=list(row))

def tk_requirements_statement_add():
    text = requirements_entry_statement_id.get().strip()
    if text and text not in requirements_statements_list_cur:
        requirements_statements_list_cur.append(text)
        requirements_listbox.insert(tk.END, text)
        # requirements_entry_statement_id.delete(0, tk.END)
    tk_statements_view()

def move_record(direction):
    selected = requirements_tree.selection()
    if not selected:
        return

    item = selected[0]
    current = requirements_tree.item(item, "values")
    current_id = current[0]  # Adjust index to your ID column

    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    
    # cur.execute(f"PRAGMA table_info({requirements_table_name})")
    # print([column[1] for column in cur.fetchall()])

    cur.execute(f'''
        SELECT sort_order 
        FROM {requirements_table_name} 
        WHERE requirement_id = ?
    ''', (current_id,))
    current_order = cur.fetchone()[0]
    # print(f'''CURRENT ORDER: {current_order}''')

    if direction == "up":
        cur.execute(f'''
            SELECT requirement_id, sort_order 
            FROM {requirements_table_name} 
            WHERE sort_order < ?
            ORDER BY sort_order DESC LIMIT 1
        ''', (current_order,))
    else:
        cur.execute(f'''
            SELECT requirement_id, sort_order FROM {requirements_table_name} 
            WHERE sort_order > ?
            ORDER BY sort_order ASC LIMIT 1
        ''', (current_order,))
    neighbor = cur.fetchone()

    if neighbor:
        neighbor_id, neighbor_order = neighbor
        cur.execute(f"UPDATE {requirements_table_name} SET sort_order = ? WHERE requirement_id = ?",
                    (neighbor_order, current_id))
        cur.execute(f"UPDATE {requirements_table_name} SET sort_order = ? WHERE requirement_id = ?",
                    (current_order, neighbor_id))
        conn.commit()
    conn.close()
    tk_requirements_view()

    print(f'CURRENT_ID: {current_id}')
    for item in requirements_tree.get_children():
        if requirements_tree.item(item, "values")[0] == current_id:
            print(requirements_tree.item(item, "values"))
            requirements_tree.selection_set(item)
            # requirements_tree.focus(item)

            requirements_tree.after_idle(
                lambda item=item: requirements_tree.focus(item)
            )
            requirements_tree.see(item)
            break

    # print(direction)
    # print(current_id)
    # print(f'''CURRENT ORDER: {current_order}''')
    # print(f'''NEIGHBOR ORDER: {neighbor}''')

# ----------------------------------------------------------
# TKINTER categories
# ----------------------------------------------------------

def tk_categories_view(items=None):
    if not items:
        items = sql_categories_get_all()
    categories_tree.delete(*categories_tree.get_children())
    rows = []
    for item in items:
        row = [
            item['category_id'], 
            item['category_text'],
        ]
        rows.append(row)
    for row in rows:
        categories_tree.insert("", tk.END, values=list(row))

def tk_categories_category_lvl1_insert():
    # category_id = categories_entry_category_lvl1_id.get()
    category_text = categories_entry_category_lvl1_text.get()
    # if category_id.strip() == '':
    #     print('ERR: category_id text NOT valid')
    #     return
    if category_text.strip() == '':
        print('ERR: category_text text NOT valid')
        return
    sql_categories_insert(
        category_text,
    )
    tk_categories_view()

def tk_categories_category_lvl1_delete(event):
    if not categories_tree.selection(): return
    item = categories_tree.selection()[0]
    id = categories_tree.item(item)["values"][0]
    ###
    sql_categories_delete(id)
    categories_tree.delete(item)

    
def tk_categories_select(event):
    if not categories_tree.selection(): return
    item = categories_tree.selection()[0]
    category_id = categories_tree.item(item)["values"][0]

    categories_requirements_items = sql_categories_requirements_get_by_category_id(category_id)
    # print(categories_requirements_items)
    tk_categories_requirements_view(items=categories_requirements_items)
    # tk_statements_view()

    # ###
    # statements_items = []
    # for statement_id in ids_lst:
    #     statement_item = sql_statements_get_by_id(statement_id)
    #     statements_items.append(statement_item)
    # tk_requirements_statements_view(statements_items)

def tk_categories_requirements_insert():
    if not categories_tree.selection(): return
    item = categories_tree.selection()[0]
    category_id = categories_tree.item(item)["values"][0]
    requirement_id = categories_entry_requirement_id.get()
    requirement_text = categories_text_requirement_text.get("1.0", tk.END).strip()
    # print(category_id)
    # print(requirement_id)
    # print(requirement_text)
    sql_categories_requirements_insert(
        category_id=category_id, 
        requirement_id=requirement_id, 
    )
    tk_categories_requirements_view()

def tk_categories_requirements_view(items=None):
    # if not items:
        # items = sql_categories_requirements_get_all()
    categories_requirements_tree.delete(*categories_requirements_tree.get_children())
    rows = []
    # print(items)
    for item in items:
        # print(item)
        category_item = sql_categories_get_by_id(int(item['category_id']))
        requirement_item = sql_requirements_get_by_id(int(item['requirement_id']))
        if category_item and requirement_item:
            row = [
                item['category_id'], 
                category_item['category_text'],
                item['requirement_id'],
                requirement_item['requirement_text'],
            ]
            rows.append(row)
    for row in rows:
        categories_requirements_tree.insert("", tk.END, values=list(row))

def tk_categories_requirements_delete(event):
    if not categories_requirements_tree.selection(): return
    item = categories_requirements_tree.selection()[0]
    category_id = categories_requirements_tree.item(item)["values"][0]
    requirement_id = categories_requirements_tree.item(item)["values"][2]
    ###
    sql_categories_requirements_delete(category_id, requirement_id)
    categories_requirements_tree.delete(item)

# ----------------------------------------------------------
# TKINTER FUNCTIONS COMPILE
# ----------------------------------------------------------

def tk_compile_markdown():
    markdown_stakeholders_create()
    markdown_questions_create()
    markdown_answers_create()
    markdown_statements_create()
    from textwrap import dedent
    items = sql_answers_get_all()
    output_text = ''
    for item in items:
        print(item)
        question_item = sql_questions_get_by_id(item['question_id'])
        stakeholder_item = sql_stakeholders_get_by_id(question_item['stakeholder_id'])
        print(stakeholder_item)
        output_text += dedent(f'''
            | Field              | Value                      |
            | ------------------ | -------------------------- |
            | Question ID        | {item['question_id']}      |
            | Answer ID          | {item['answer_id']}        |
            | Stakeholder Role   | {stakeholder_item['stakeholder_role']}        |
            | Question Text      | {item['question_text']}    |
            | Answer Text        | {item['answer_text']}      |
        ''').strip()
        output_text += f'\n\n'
    with open('output.md', 'w', encoding="utf-8") as f: f.write(output_text)


# # Example:
# # sql_stakeholders_drop()
# # sql_answers_drop()
# sql_stakeholders_create()
# sql_questions_create()
# sql_answers_create()
# # print(items)

def create_tables():
    sql_stakeholders_create()
    # sql_answers_drop()
    sql_questions_create()
    # sql_questions_drop()
    sql_answers_create()

def refresh_all():
    tk_stakeholder_view()
    questions_view()
    tk_answers_view()
    tk_statements_view()
    tk_requirements_view()
    tk_categories_view()

    
    new_values = [
        f"{item['stakeholder_id']} "
        f"({item['stakeholder_role']} - "
        f"{item['stakeholder_name_first']} "
        f"{item['stakeholder_name_last']})"
        for item in sql_stakeholders_get_all()
    ]

    questions_combobox_stakeholder["values"] = new_values

def new_project():
    global db_filepath
    project_file = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("SQLite database", "*.db")]
    )
    if not project_file: return
    db_filepath = project_file
    # 'statements.db'
    # db = sqlite3.connect(project_file)
    create_tables()
    sql_statements_create()
    refresh_all()

def open_project():
    global db_filepath
    filename = filedialog.askopenfilename(
        filetypes=[("SQLite database", "*.db")]
    )
    if not filename: return
    if db: db.close()
    db_filepath = filename
    # db = sqlite3.connect(project_file)
    # sql_requirements_drop()
    # sql_requirements_create()
    # sql_categories_drop()
    # sql_categories_create()
    # sql_categories_requirements_drop()
    # sql_categories_requirements_create()
    refresh_all()

def save_project():
    if db: db.commit()



###########################################################
# MARKDOWN
###########################################################
def markdown_stakeholders_create():
    items = sql_stakeholders_get_all()
    output_filepath = f'C:/og-new/products/aurora_module_relay_x8/v0_1_0/docs/inputs/stakeholders.md'
    output_text = ''
    output_text += dedent(f'''
        <head>
        <title>
        Aurora: Module Relay x8
        </title>
        <subtitle>
        Stakeholders
        </subtitle>
        </head>
        <rev>
        Version, Date, Author, Description
        0.1.0, 2026-07-02, Martin Pellizzer, Starting version
        </rev>
        <body>
        # Stakeholders
    ''').strip() + '\n'
    for item_i, item in enumerate(items):
        output_text += dedent(f'''
            ## Stakeholder {item_i+1}: {item['stakeholder_role']}
            {item['stakeholder_purpose']}
            | Field              | Value                      |
            | ------------------ | -------------------------- |
            | Stakeholder ID | {item['stakeholder_id']} |
            | Stakeholder First Name | {item['stakeholder_name_first']} |
            | Stakeholder Last Name | {item['stakeholder_name_last']} |
            | Stakeholder Role | {item['stakeholder_role']} |
        ''')
        # for key, val in item.items():
        #     output_text += dedent(f'''| {key} | {val} | \n''')
        output_text += f'\n\n'
    output_text += dedent(f'''
        </body>
    ''').strip() + '\n'
    with open(output_filepath, 'w', encoding="utf-8") as f: f.write(output_text)

def markdown_questions_create():
    questions_items = sql_questions_get_all()
    output_filepath = f'C:/og-new/products/aurora_module_relay_x8/v0_1_0/docs/inputs/questions.md'
    output_text = ''
    output_text += dedent(f'''
        <head>
        <title>
        Aurora: Module Relay x8
        </title>
        <subtitle>
        Stakeholders Questions
        </subtitle>
        </head>
        <rev>
        Version, Date, Author, Description
        0.1.0, 2026-07-02, Martin Pellizzer, Starting version
        </rev>
        <body>
        # Questions
    ''').strip() + '\n'
    for item_i, question_item in enumerate(questions_items):
        stakeholder_item = sql_stakeholders_get_by_id(question_item['stakeholder_id'])
        output_text += dedent(f'''
            ## Question {item_i+1}
            | Field              | Value                      |
            | ------------------ | -------------------------- |
            | Stakeholder ID | {stakeholder_item['stakeholder_id']} |
            | Stakeholder Role | {stakeholder_item['stakeholder_role']} |
            | Question ID | {question_item['question_id']} |
            | Question Text | {question_item['question_text']} |
        ''')
        output_text += f'\n\n'
    output_text += dedent(f'''
        </body>
    ''').strip() + '\n'
    with open(output_filepath, 'w', encoding="utf-8") as f: f.write(output_text)

def markdown_answers_create():
    answers_items = sql_answers_get_all()
    output_filepath = f'C:/og-new/products/aurora_module_relay_x8/v0_1_0/docs/inputs/answers.md'
    output_text = ''
    output_text += dedent(f'''
        <head>
        <title>
        Aurora: Module Relay x8
        </title>
        <subtitle>
        Stakeholders Answers
        </subtitle>
        </head>
        <rev>
        Version, Date, Author, Description
        0.1.0, 2026-07-02, Martin Pellizzer, Starting version
        </rev>
        <body>
        # Answers
    ''').strip() + '\n'
    for item_i, answer_item in enumerate(answers_items):
        question_item = sql_questions_get_by_id(answer_item['question_id'])
        stakeholder_item = sql_stakeholders_get_by_id(question_item['stakeholder_id'])
        output_text += dedent(f'''
            ## Answer {item_i+1}: {stakeholder_item['stakeholder_role']}
            ### Question
            {question_item['question_text']}
            ### Answer
            {answer_item['answer_text']}
            | Field              | Value                      |
            | ------------------ | -------------------------- |
            | Stakeholder ID | {stakeholder_item['stakeholder_id']} |
            | Question ID | {question_item['question_id']} |
            | Answer ID | {answer_item['answer_id']} |
            | Stakeholder Role | {stakeholder_item['stakeholder_role']} |
            | Question Text | {question_item['question_text']} |
            | Answer Text | {answer_item['answer_text']} |
        ''')
        output_text += f'\n\n'
    output_text += dedent(f'''
        </body>
    ''').strip() + '\n'
    with open(output_filepath, 'w', encoding="utf-8") as f: f.write(output_text)

def markdown_statements_create():
    statements_items = sql_statements_get_all()
    output_filepath = f'C:/og-new/products/aurora_module_relay_x8/v0_1_0/docs/inputs/statements.md'
    output_text = ''
    output_text += dedent(f'''
        <head>
        <title>
        Aurora: Module Relay x8
        </title>
        <subtitle>
        Stakeholders Statements
        </subtitle>
        </head>
        <rev>
        Version, Date, Author, Description
        0.1.0, 2026-07-02, Martin Pellizzer, Starting version
        </rev>
        <body>
        # Statements
    ''').strip() + '\n'
    for item_i, statement_item in enumerate(statements_items):
        answer_item = sql_answers_get_by_id(statement_item['answer_id'])
        question_item = sql_questions_get_by_id(answer_item['question_id'])
        stakeholder_item = sql_stakeholders_get_by_id(question_item['stakeholder_id'])
        output_text += dedent(f'''
            ## Statement {item_i+1}
            ### Statement
            {statement_item['statement_text']}
            ### Answer
            {answer_item['answer_text']}
            ### Question
            {question_item['question_text']}
            ### Stakeholder
            {stakeholder_item['stakeholder_role']}
            | Field              | Value                      |
            | ------------------ | -------------------------- |
            | Stakeholder ID | {stakeholder_item['stakeholder_id']} |
            | Question ID | {question_item['question_id']} |
            | Answer ID | {answer_item['answer_id']} |
            | Stakeholder Role | {stakeholder_item['stakeholder_role']} |
            | Question Text | {question_item['question_text']} |
            | Answer Text | {answer_item['answer_text']} |
            | Statement Text | {statement_item['statement_text']} |

            ---
        ''')
        output_text += f'\n\n'
    output_text += dedent(f'''
        </body>
    ''').strip() + '\n'
    with open(output_filepath, 'w', encoding="utf-8") as f: f.write(output_text)



###########################################################
# TKINTER UI
###########################################################

padx = 10

root = tk.Tk()
root.geometry("1280x720")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_project)
file_menu.add_command(label="Open...", command=open_project)
file_menu.add_command(label="Save", command=save_project)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

# ----------------------------------------------------------
# STAKEHOLDERS TAB
# ----------------------------------------------------------

stakeholders_tab = tk.Frame(tabs)
tabs.add(stakeholders_tab, text="Stakeholders")

# ..........................................................
# STAKEHOLDERS FRAME LEFT
# ..........................................................

frame_left = tk.Frame(stakeholders_tab, width=200)
frame_left.pack(side="left", fill="y")
frame_left.pack_propagate(False)

tk.Label(frame_left, text="Stakeholder First Name").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_name_first = tk.Entry(frame_left)
entry_stakeholder_name_first.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Last Name").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_name_last = tk.Entry(frame_left)
entry_stakeholder_name_last.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Role").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
dropdown = ttk.Combobox(frame_left, values=stakeholder_roles)
dropdown.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Category").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_category = tk.Entry(frame_left)
entry_stakeholder_category.pack(fill="x", padx=(padx, padx))

tk.Label(frame_left, text="Stakeholder Purpose").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
entry_stakeholder_purpose = tk.Entry(frame_left)
entry_stakeholder_purpose.pack(fill="x", padx=(padx, padx))

tk.Button(frame_left, text="Insert Stakeholder", command=tk_stakeholder_insert).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# STAKEHOLDERS FRAME CENTER
# ..........................................................

frame_center = tk.Frame(stakeholders_tab)
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

tk_stakeholder_view()

tree.bind("<Delete>", tk_stakeholder_delete)

def stakeholder_select(event):
    if not tree.selection(): return
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


tk.Button(
    frame_left,
    text="Update",
    command=tk_stakeholder_update
).pack(fill="x", padx=padx, pady=10)



###########################################################
# QUESTIONS TAB
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

questions_combobox_stakeholder_values = [
    f'''
        {item['stakeholder_id']} ({item['stakeholder_role']} - {item['stakeholder_name_first']} {item['stakeholder_name_last']})
    ''' for item in sql_stakeholders_get_all()
]
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


questions_tree.bind("<<TreeviewSelect>>", questions_select)


tk.Button(
    questions_frame_left,
    text="Update",
    command=questions_update
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

tk.Button(
    questions_frame_left,
    text="Print Questions",
    command=questions_print
).pack(fill="x", padx=(padx, padx), pady=(10, 0))



###########################################################
# ANSWERS TAB
###########################################################

padx = 10

answers_fields = [
    "answer_id", 
    "answer_text",
    "question_id",
    "question_text",
    "stakeholder_id",
    "stakeholder_text",
]

answers_tab = tk.Frame(tabs)
tabs.add(answers_tab, text="Answers")

answers_frame_left = tk.Frame(answers_tab, width=200)
answers_frame_left.pack(side="left", fill="y")
answers_frame_left.pack_propagate(False)

# tk.Label(answers_frame_left, text="Answer Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
# answers_entry_answer_text = tk.Entry(answers_frame_left)
# answers_entry_answer_text.pack(fill="x", padx=(padx, padx))

# answers_combobox_stakeholder_values = [
#     f'''
#         {item['question_id']} ({item['question_text']})
#     '''.strip()
#     for item in sql_questions_get_all()
# ]
# tk.Label(answers_frame_left, text="Question ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
# answers_combobox_stakeholder = ttk.Combobox(
#     answers_frame_left, 
#     values=answers_combobox_stakeholder_values
# )
# answers_combobox_stakeholder.pack(fill="x", padx=(padx, padx))

tk.Label(answers_frame_left, text="Question ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
answers_entry_question_id = tk.Entry(answers_frame_left)
answers_entry_question_id.pack(fill="x", padx=(padx, padx))
answers_entry_question_id.config(state="disabled")

# answers_entry_question_text = tk.Entry(answers_frame_left)
# answers_entry_question_text.pack(fill="x", padx=(padx, padx))

entry = tk.Entry(root)
entry.config(state="disabled")
bg = entry.cget("disabledbackground")
fg = entry.cget("disabledforeground")

tk.Label(answers_frame_left, text="Question Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
answers_text_question_text = tk.Text(answers_frame_left, wrap="word", height=5)
answers_text_question_text.pack(fill="x", padx=(padx, padx))
answers_text_question_text.config(state="disabled", bg=bg, fg=fg)

tk.Label(answers_frame_left, text="Answer Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
answers_text_answer_text = tk.Text(answers_frame_left, wrap="word", height=10)
answers_text_answer_text.pack(fill="x", padx=(padx, padx))

tk.Button(
    answers_frame_left,
    text="Insert Answer",
    command=tk_answers_insert
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

tk.Button(
    answers_frame_left,
    text="Update Answer",
    command=tk_answers_update
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# ANSWERS FRAME CENTER
# ..........................................................

answers_frame_center = tk.Frame(answers_tab)
answers_frame_center.pack(side="left", fill="both", expand=True)

answers_tree = ttk.Treeview(
    answers_frame_center, 
    columns=answers_fields, 
    show="headings"
)
answers_tree.pack(fill="both", expand=True)

for col in answers_fields:
    answers_tree.heading(col, text=col)
    answers_tree.column(col, width=1)

tk_answers_view()

answers_tree.bind("<Delete>", tk_answers_delete)
answers_tree.bind("<<TreeviewSelect>>", tk_answers_select)



###########################################################
# STATEMENTS TAB
###########################################################

padx = 10

statements_fields = [
    "statement_id",
    "statement_text",
    "answer_id",
    "answer_text",
]

statements_tab = tk.Frame(tabs)
tabs.add(statements_tab, text="Statements")

statements_frame_left = tk.Frame(statements_tab, width=200)
statements_frame_left.pack(side="left", fill="y")
statements_frame_left.pack_propagate(False)

tk.Label(statements_frame_left, text="Answer ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
statements_entry_answer_id = tk.Entry(statements_frame_left)
statements_entry_answer_id.pack(fill="x", padx=(padx, padx))
statements_entry_answer_id.config(state="disabled")

tk.Label(statements_frame_left, text="Answer Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
statements_text_answer_text = tk.Text(statements_frame_left, wrap="word", height=15)
statements_text_answer_text.pack(fill="x", padx=(padx, padx))
statements_text_answer_text.config(state="disabled", bg=bg, fg=fg)

tk.Label(statements_frame_left, text="Statement Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
statements_text_statement_text = tk.Text(statements_frame_left, wrap="word", height=10)
statements_text_statement_text.pack(fill="x", padx=(padx, padx))

tk.Button(
    statements_frame_left,
    text="Insert Statement",
    command=tk_statements_insert
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

tk.Button(
    statements_frame_left,
    text="Update Statement",
    command=tk_statements_update
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# STATEMENTS FRAME CENTER
# ..........................................................

statement_frame_center = tk.Frame(statements_tab)
statement_frame_center.pack(side="left", fill="both", expand=True)

statements_tree = ttk.Treeview(
    statement_frame_center, 
    columns=statements_fields, 
    show="headings"
)
statements_tree.pack(fill="both", expand=True)

for col in statements_fields:
    statements_tree.heading(col, text=col)
    statements_tree.column(
        col, 
        stretch=False
    )
statements_tree.column(
    "statement_id", 
    width=100,
    stretch=False,
)
statements_tree.column(
    "statement_text", 
    width=120,
    stretch=True,
)
statements_tree.column(
    "answer_id", 
    width=100,
    stretch=False,
)
statements_tree.column(
    "answer_text", 
    width=100,
    stretch=False,
)

statements_tree.tag_configure("blank", background="white")
statements_tree.tag_configure("tmp", background="yellow")
statements_tree.tag_configure("done", background="green")

tk_statements_view()

statements_tree.bind("<Delete>", tk_statements_delete)
statements_tree.bind("<<TreeviewSelect>>", tk_statements_select)


###########################################################
# REQUIREMENTS TAB
###########################################################

padx = 10

requirements_fields = [
    "requirement_id",
    "requirement_text",
    "requirements_statements_ids",
]

requirements_statements_fields = [
    "statement_id",
    "statement_text",
]

requirements_tab = tk.Frame(tabs)
tabs.add(requirements_tab, text="Requirements")

requirements_frame_left = tk.Frame(requirements_tab, width=200)
requirements_frame_left.pack(side="left", fill="y")
requirements_frame_left.pack_propagate(False)

tk.Label(requirements_frame_left, text="Statement ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_entry_statement_id = tk.Entry(requirements_frame_left)
requirements_entry_statement_id.pack(fill="x", padx=(padx, padx))
requirements_entry_statement_id.config(state="disabled")

tk.Label(requirements_frame_left, text="Statement Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_text_statement_text = tk.Text(requirements_frame_left, wrap="word", height=5)
requirements_text_statement_text.pack(fill="x", padx=(padx, padx))
requirements_text_statement_text.config(state="disabled", bg=bg, fg=fg)

tk.Button(
    requirements_frame_left,
    text="Add Statement",
    command=tk_requirements_statement_add
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# Listbox with multiple selection
tk.Label(requirements_frame_left, text="Statement List").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_listbox = tk.Listbox(requirements_frame_left, selectmode=tk.EXTENDED, height=5)
requirements_listbox.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(requirements_frame_left, text="Requirement Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_text_requirement_text = tk.Text(requirements_frame_left, wrap="word", height=10)
requirements_text_requirement_text.pack(fill="x", padx=(padx, padx))

def requirements_listbox_item_delete(event=None):
    for index in reversed(requirements_listbox.curselection()):
        text = requirements_listbox.get(index)
        requirements_statements_list_cur.remove(text)  # Remove matching string from your list
        requirements_listbox.delete(index)
        tk_statements_view()

requirements_listbox.bind("<Delete>", requirements_listbox_item_delete)

tk.Button(
    requirements_frame_left,
    text="Insert Requirement",
    command=tk_requirements_insert
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

tk.Button(
    requirements_frame_left,
    text="Update Requirement",
    command=tk_requirements_update
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# REQUIREMENTS FRAME CENTER
# ..........................................................

requirements_frame_center = tk.Frame(requirements_tab)
requirements_frame_center.pack(side="left", fill="both", expand=True)

tk.Label(requirements_frame_center, text="Search").pack(anchor="w", pady=(10, 0))
requirements_entry_search = tk.Entry(requirements_frame_center)
requirements_entry_search.pack(fill="x", pady=(0, padx))

def on_key_release(event):
    entry_text = requirements_entry_search.get()
    sql_requirements_items = sql_requirements_get_all()
    sql_requirements_items_filter = [
        item
        for item in sql_requirements_items
        if entry_text in item['requirement_text']
    ]
    tk_requirements_view(sql_requirements_items_filter)

    print(entry_text)  # Current text
    print(sql_requirements_items)

requirements_entry_search.bind("<KeyRelease>", on_key_release)


requirements_tree = ttk.Treeview(
    requirements_frame_center,
    columns=requirements_fields,
    show="headings"
)
requirements_tree.pack(fill="both", expand=True)

for col in requirements_fields:
    requirements_tree.heading(col, text=col)
    requirements_tree.column(
        col, 
        stretch=False
    )
requirements_tree.column(
    "requirement_id",
    width=100,
    stretch=False,
)
requirements_tree.column(
    "requirement_text",
    width=120,
    stretch=True,
)
requirements_tree.column(
    "requirements_statements_ids",
    width=100,
    stretch=False,
)

tk_requirements_view()

requirements_tree.bind("<Delete>", tk_requirements_delete)
requirements_tree.bind("<<TreeviewSelect>>", tk_requirements_select)


requirements_statements_tree = ttk.Treeview(
    requirements_frame_center,
    columns=requirements_statements_fields,
    show="headings"
)
requirements_statements_tree.pack(fill="both", expand=True)
for col in requirements_statements_fields:
    requirements_statements_tree.heading(col, text=col)
    requirements_statements_tree.column(
        col, 
        stretch=False
    )
requirements_statements_tree.column(
    "statement_id",
    width=100,
    stretch=False,
)
requirements_statements_tree.column(
    "statement_text",
    width=120,
    stretch=True,
)

requirements_tree.bind("<Control-Up>", lambda e: move_record("up"))
requirements_tree.bind("<Control-Down>", lambda e: move_record("down"))

###########################################################
# CATEGORIES TAB
###########################################################

categories_fields = [
    "category_lvl1_id",
    "category_lvl1_text",
]

categories_tab = tk.Frame(tabs)
tabs.add(categories_tab, text="Categories")

categories_frame_left = tk.Frame(categories_tab, width=200)
categories_frame_left.pack(side="left", fill="y")
categories_frame_left.pack_propagate(False)

# tk.Label(categories_frame_left, text="Category LVL1 ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
# categories_entry_category_lvl1_id = tk.Entry(categories_frame_left)
# categories_entry_category_lvl1_id.pack(fill="x", padx=(padx, padx))

tk.Label(categories_frame_left, text="Category LVL1 Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
categories_entry_category_lvl1_text = tk.Entry(categories_frame_left)
categories_entry_category_lvl1_text.pack(fill="x", padx=(padx, padx))

tk.Button(
    categories_frame_left,
    text="Insert Category",
    command=tk_categories_category_lvl1_insert
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

tk.Label(categories_frame_left, text="Requirement ID").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
categories_entry_requirement_id = tk.Entry(categories_frame_left)
categories_entry_requirement_id.pack(fill="x", padx=(padx, padx))
categories_entry_requirement_id.config(state="disabled")

tk.Label(categories_frame_left, text="Requirement Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
categories_text_requirement_text = tk.Text(categories_frame_left, wrap="word", height=5)
categories_text_requirement_text.pack(fill="x", padx=(padx, padx))
categories_text_requirement_text.config(state="disabled", bg=bg, fg=fg)

tk.Button(
    categories_frame_left,
    text="Insert Requirement",
    command=tk_categories_requirements_insert
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# CATEGORIES FRAME CENTER
# ..........................................................

categories_frame_center = tk.Frame(categories_tab)
categories_frame_center.pack(side="left", fill="both", expand=True)

# tk.Label(categories_frame_center, text="Search").pack(anchor="w", pady=(10, 0))
# categories_entry_search = tk.Entry(categories_frame_center)
# categories_entry_search.pack(fill="x", pady=(0, padx))

categories_tree = ttk.Treeview(
    categories_frame_center,
    columns=categories_fields,
    show="headings"
)
categories_tree.pack(fill="both", expand=True)

for col in categories_fields:
    categories_tree.heading(col, text=col)
    categories_tree.column(
        col, 
        stretch=False
    )
categories_tree.column(
    "category_lvl1_id",
    width=120,
    stretch=False,
)
categories_tree.column(
    "category_lvl1_text",
    width=120,
    stretch=True,
)
# categories_tree.column(
#     "requirement_id",
#     width=100,
#     stretch=False,
# )
# categories_tree.column(
#     "requirement_text",
#     width=120,
#     stretch=True,
# )

tk_categories_view()

categories_tree.bind("<Delete>", tk_categories_category_lvl1_delete)
categories_tree.bind("<<TreeviewSelect>>", tk_categories_select)


requirements_tree.bind("<<TreeviewSelect>>", tk_requirements_select)

categories_requirements_fields = [
    "category_lvl1_id",
    "category_lvl1_text",
    "requirement_id",
    "requirement_text",
]

categories_requirements_tree = ttk.Treeview(
    categories_frame_center,
    columns=categories_requirements_fields,
    show="headings"
)
categories_requirements_tree.pack(fill="both", expand=True)
for col in categories_requirements_fields:
    categories_requirements_tree.heading(col, text=col)
    categories_requirements_tree.column(col, stretch=False)
categories_requirements_tree.column(
    "category_lvl1_id",
    width=120,
    stretch=False,
)
categories_requirements_tree.column(
    "category_lvl1_text",
    width=120,
    stretch=False,
)
categories_requirements_tree.column(
    "requirement_id",
    width=120,
    stretch=False,
)
categories_requirements_tree.column(
    "requirement_text",
    width=120,
    stretch=True,
)

# tk_categories_requirements_view()

categories_requirements_tree.bind("<Delete>", tk_categories_requirements_delete)

"""
TODO
the goal is to group the requirements in hierarchical categories
ex:
1. Hardware
    1.1
    1.2
2. Software
    2.1 Report to CORE
    2.2 Local fault-handling
use max 3 levels
list grouped requirement per section

i need:
- left sidebar for
    - requirement_id
    - requirement_text
    - level 1 category
    - level 2 category
    - level 3 category
- center tree for
    - display grouped relationships
"""

"""



# Listbox with multiple selection
tk.Label(requirements_frame_left, text="Statement List").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_listbox = tk.Listbox(requirements_frame_left, selectmode=tk.EXTENDED, height=5)
requirements_listbox.pack(fill="both", expand=True, padx=10, pady=10)

tk.Label(requirements_frame_left, text="Requirement Text").pack(anchor="w", pady=(10, 0), padx=(padx, padx))
requirements_text_requirement_text = tk.Text(requirements_frame_left, wrap="word", height=10)
requirements_text_requirement_text.pack(fill="x", padx=(padx, padx))

def requirements_listbox_item_delete(event=None):
    for index in reversed(requirements_listbox.curselection()):
        text = requirements_listbox.get(index)
        requirements_statements_list_cur.remove(text)  # Remove matching string from your list
        requirements_listbox.delete(index)
        tk_statements_view()

requirements_listbox.bind("<Delete>", requirements_listbox_item_delete)


tk.Button(
    requirements_frame_left,
    text="Update Requirement",
    command=tk_requirements_update
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

# ..........................................................
# REQUIREMENTS FRAME CENTER
# ..........................................................


def on_key_release(event):
    entry_text = requirements_entry_search.get()
    sql_requirements_items = sql_requirements_get_all()
    sql_requirements_items_filter = [
        item
        for item in sql_requirements_items
        if entry_text in item['requirement_text']
    ]
    tk_requirements_view(sql_requirements_items_filter)

    print(entry_text)  # Current text
    print(sql_requirements_items)

requirements_entry_search.bind("<KeyRelease>", on_key_release)




requirements_tree.bind("<Control-Up>", lambda e: move_record("up"))
requirements_tree.bind("<Control-Down>", lambda e: move_record("down"))

"""


###########################################################
# TAB COMPILE
###########################################################

compile_tab = tk.Frame(tabs)
tabs.add(compile_tab, text="Compile")

compile_frame_left = tk.Frame(compile_tab, width=200)
compile_frame_left.pack(side="left", fill="y")
compile_frame_left.pack_propagate(False)

tk.Button(
    compile_frame_left,
    text="Compile Markdown",
    command=tk_compile_markdown
).pack(fill="x", padx=(padx, padx), pady=(10, 0))

root.mainloop()