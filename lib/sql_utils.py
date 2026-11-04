
import sqlite3

# ----------------------------------------------------------
# SQLITE SPECIFICATIONS RS485
# ----------------------------------------------------------

def sql_specifications_modbus_drop():
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {specifications_modbus_table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_rs485_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            specification_rs485_wires_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_specifications_rs485_get_all(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql_specifications_modbus_insert(
    specification_id,
    specification_modbus_mode_text, 
    specification_modbus_role_text, 
    specification_modbus_baud_rate_text, 
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {specifications_modbus_table_name} (
            specification_id,
            specification_modbus_mode_text,
            specification_modbus_role_text,
            specification_modbus_baud_rate_text
        ) 
        VALUES (?, ?, ?, ?)
    ''', (
        specification_id,
        specification_modbus_mode_text,
        specification_modbus_role_text,
        specification_modbus_baud_rate_text,
    ))
    db.commit()
    db.close()

def sql_specifications_rs485_set(
    db_filepath,
    table_name,
    specification_id,
    specification_rs485_wires_text, 
):
    sql_specifications_rs485_create(db_filepath, table_name)

    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_id,
            specification_rs485_wires_text
        ) 
        VALUES (?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            specification_rs485_wires_text = excluded.specification_rs485_wires_text
    ''', (
        specification_id,
        specification_rs485_wires_text,
    ))
    db.commit()
    db.close()

def sql_specifications_rs485_delete(
    db_filepath,
    table_name,
    specification_id,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {table_name} 
        WHERE specification_id = ?
    ''', (specification_id,))
    db.commit()
    db.close()

def sql_specifications_modbus_get_by_id(id):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {specifications_modbus_table_name}
        WHERE specification_modbus_id = ?
    ''', (id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item

def sql_specifications_rs485_get_by_specification_id(
    db_filepath,
    table_name,
    specification_id,
):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {table_name}
        WHERE specification_id = ?
    ''', (specification_id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item
    
# sql_specifications_modbus_drop()
# sql_specifications_modbus_create()

# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS WRITE
# ----------------------------------------------------------

def sql_specifications_modbus_write_get_all(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql_specifications_modbus_write_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            specification_modbus_write_function_code_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_specifications_modbus_write_set(
    db_filepath,
    table_name,
    specification_id,
    specification_modbus_write_function_code_text, 
):
    sql_specifications_modbus_write_create(db_filepath, table_name)

    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_id,
            specification_modbus_write_function_code_text
        ) 
        VALUES (?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            specification_modbus_write_function_code_text = excluded.specification_modbus_write_function_code_text
    ''', (
        specification_id,
        specification_modbus_write_function_code_text,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_write_get_by_specification_id(
    db_filepath,
    table_name,
    specification_id,
):
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    records = db.execute(f'''
        SELECT * 
        FROM {table_name}
        WHERE specification_id = ?
    ''', (specification_id,))
    rows = records.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    db.close()
    return item
