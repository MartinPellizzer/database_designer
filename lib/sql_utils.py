
import sqlite3
import json

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

specifications_modbus_write_fields = [
    'specification_modbus_write_intro_text',
    'specification_modbus_write_slave_address_text',
    'specification_modbus_write_function_code_text',
    'specification_modbus_write_coil_address_hb_text',
    'specification_modbus_write_coil_address_lb_text',
    'specification_modbus_write_coil_value_hb_text',
    'specification_modbus_write_coil_value_lb_text',
]

def sql_specifications_modbus_write_drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_modbus_write_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for field in specifications_modbus_write_fields:
        fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            {fields}
        )
    '''
    cur.execute(query)
    db.commit()
    db.close()

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

def sql_specifications_modbus_write_update(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {}
    for field in specifications_modbus_write_fields:
        columns[field] = 'TEXT'
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql_specifications_modbus_write_set(
    db_filepath,
    table_name,
    specification_id,
    specification_fields,
):
    sql_specifications_modbus_write_create(db_filepath, table_name,)
    sql_specifications_modbus_write_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    
    fields_insert = []
    for field in specifications_modbus_write_fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    
    fields_update = []
    for field in specifications_modbus_write_fields:
        fields_update.append(f'{field} = excluded.{field}')
    fields_update = ',\n'.join(fields_update)
    
    fields_items = specification_fields

    query = f'''
        INSERT INTO {table_name} (
            specification_id,
            {fields_insert}
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            {fields_update}
    '''
    cur.execute(query, (
        specification_id,
        *fields_items,
    ))
    print(query)
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

# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS WRITE RESPONSE
# ----------------------------------------------------------

specifications_modbus_write_response_fields = [
    'specification_modbus_write_response_intro_text',
    'specification_modbus_write_response_slave_address_text',
    'specification_modbus_write_response_function_code_text',
    'specification_modbus_write_response_coil_address_hb_text',
    'specification_modbus_write_response_coil_address_lb_text',
    'specification_modbus_write_response_coil_value_hb_text',
    'specification_modbus_write_response_coil_value_lb_text',
]

def sql_specifications_modbus_write_response_drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_modbus_write_response_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for field in specifications_modbus_write_response_fields:
        fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            {fields}
        )
    '''
    cur.execute(query)
    db.commit()
    db.close()

def sql_specifications_modbus_write_response_get_all(
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

def sql_specifications_modbus_write_response_update(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {}
    for field in specifications_modbus_write_response_fields:
        columns[field] = 'TEXT'
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql_specifications_modbus_write_response_set(
    db_filepath,
    table_name,
    specification_id,
    specification_fields,
):
    # print(db_filepath)
    # print(table_name)
    # print(specification_id)
    # print(specification_fields)
    sql_specifications_modbus_write_response_create(db_filepath, table_name,)
    sql_specifications_modbus_write_response_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()

    # fields = [row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")]
    # for field in fields:
    #     print(field)
    # return
    
    fields_insert = []
    for field in specifications_modbus_write_response_fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    
    fields_update = []
    for field in specifications_modbus_write_response_fields:
        fields_update.append(f'{field} = excluded.{field}')
    fields_update = ',\n'.join(fields_update)
    
    fields_items = specification_fields

    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_id,
            {fields_insert}
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            {fields_update}
    ''', (
        specification_id,
        *fields_items,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_write_response_get_by_specification_id(
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


# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS READ
# ----------------------------------------------------------

def sql_specifications_modbus_read_get_all(
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

def sql_specifications_modbus_read_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            specification_modbus_read_intro_text TEXT,
            specification_modbus_read_slave_address_text TEXT,
            specification_modbus_read_function_code_text TEXT,
            specification_modbus_read_bytes_number_text TEXT,
            specification_modbus_read_register_value_text TEXT,
            specification_modbus_read_crc16_text TEXT
        )'''
    )
    db.commit()
    db.close()

def sql_specifications_modbus_read_update(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {
        "specification_modbus_read_intro_text": "TEXT",
        "specification_modbus_read_slave_address_text": "TEXT",
        "specification_modbus_read_function_code_text": "TEXT",
        "specification_modbus_read_bytes_number_text": "TEXT",
        "specification_modbus_read_register_value_text": "TEXT",
        "specification_modbus_read_crc16_text": "TEXT",
    }
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql_specifications_modbus_read_set(
    db_filepath,
    table_name,
    specification_id,
    specification_modbus_read_intro_text,
    specification_modbus_read_slave_address_text,
    specification_modbus_read_function_code_text,
    specification_modbus_read_bytes_number_text,
    specification_modbus_read_register_value_text,
    specification_modbus_read_crc16_text,
):
    sql_specifications_modbus_read_create(db_filepath, table_name,)
    sql_specifications_modbus_read_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_id,
            specification_modbus_read_intro_text,
            specification_modbus_read_slave_address_text,
            specification_modbus_read_function_code_text,
            specification_modbus_read_bytes_number_text,
            specification_modbus_read_register_value_text,
            specification_modbus_read_crc16_text
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            specification_modbus_read_intro_text = excluded.specification_modbus_read_intro_text,
            specification_modbus_read_slave_address_text = excluded.specification_modbus_read_slave_address_text,
            specification_modbus_read_function_code_text = excluded.specification_modbus_read_function_code_text,
            specification_modbus_read_bytes_number_text = excluded.specification_modbus_read_bytes_number_text,
            specification_modbus_read_register_value_text = excluded.specification_modbus_read_register_value_text,
            specification_modbus_read_crc16_text = excluded.specification_modbus_read_crc16_text
    ''', (
        specification_id,
        specification_modbus_read_intro_text,
        specification_modbus_read_slave_address_text,
        specification_modbus_read_function_code_text,
        specification_modbus_read_bytes_number_text,
        specification_modbus_read_register_value_text,
        specification_modbus_read_crc16_text,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_read_get_by_specification_id(
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






# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS READ REQUEST
# ----------------------------------------------------------

specifications_modbus_read_request_fields = [
    'specification_modbus_read_request_intro_text',
    'specification_modbus_read_request_slave_address_text',
    'specification_modbus_read_request_function_code_text',
    'specification_modbus_read_request_starting_address_hb_text',
    'specification_modbus_read_request_starting_address_lb_text',
    'specification_modbus_read_request_quantity_of_registers_hb_text',
    'specification_modbus_read_request_quantity_of_registers_lb_text',
]

def sql_specifications_modbus_read_request_drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_modbus_read_request_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for field in specifications_modbus_read_request_fields:
        fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            {fields}
        )
    '''
    cur.execute(query)
    db.commit()
    db.close()

def sql_specifications_modbus_read_request_get_all(
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

def sql_specifications_modbus_read_request_update(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {}
    for field in specifications_modbus_read_request_fields:
        columns[field] = 'TEXT'
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql_specifications_modbus_read_request_set(
    db_filepath,
    table_name,
    specification_id,
    specification_fields,
):
    sql_specifications_modbus_read_request_create(db_filepath, table_name,)
    sql_specifications_modbus_read_request_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    
    fields_insert = []
    for field in specifications_modbus_read_request_fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    
    fields_update = []
    for field in specifications_modbus_read_request_fields:
        fields_update.append(f'{field} = excluded.{field}')
    fields_update = ',\n'.join(fields_update)
    
    fields_items = specification_fields

    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_id,
            {fields_insert}
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            {fields_update}
    ''', (
        specification_id,
        *fields_items,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_read_request_get_by_specification_id(
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

# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS READ RESPONSE
# ----------------------------------------------------------

specifications_modbus_read_response_fields = [
    'specification_modbus_read_response_intro_text',
    'specification_modbus_read_response_slave_address_text',
    'specification_modbus_read_response_function_code_text',
    'specification_modbus_read_response_byte_count_text',
    'specification_modbus_read_response_register_data_hb_text',
    'specification_modbus_read_response_register_data_lb_text',
]

def sql_specifications_modbus_read_response_drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_modbus_read_response_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for field in specifications_modbus_read_response_fields:
        fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_id INTEGER PRIMARY KEY, 
            specification_id TEXT UNIQUE,
            {fields}
        )
    '''
    cur.execute(query)
    db.commit()
    db.close()

def sql_specifications_modbus_read_response_get_all(
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

def sql_specifications_modbus_read_response_update(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {}
    for field in specifications_modbus_read_response_fields:
        columns[field] = 'TEXT'
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql_specifications_modbus_read_response_set(
    db_filepath,
    table_name,
    specification_id,
    specification_fields,
):

    sql_specifications_modbus_read_response_create(db_filepath, table_name,)
    sql_specifications_modbus_read_response_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    
    fields_insert = []
    for field in specifications_modbus_read_response_fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    
    fields_update = []
    for field in specifications_modbus_read_response_fields:
        fields_update.append(f'{field} = excluded.{field}')
    fields_update = ',\n'.join(fields_update)
    
    fields_items = specification_fields

    print()
    print(fields_insert)
    print(fields_update)
    print(fields_items)
    # quit()
    query = f'''
        INSERT INTO {table_name} (
            specification_id,
            {fields_insert}
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(specification_id) DO UPDATE SET
            {fields_update}
    '''
    print(query)
    cur.execute(query, (
        specification_id,
        *fields_items,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_read_response_get_by_specification_id(
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

# ----------------------------------------------------------
# SQLITE SPECIFICATIONS MODBUS REGISTER MAP
# ----------------------------------------------------------

specifications_modbus_register_map_fields = [
    'specification_modbus_register_map_address_text',
    'specification_modbus_register_map_parameter_text',
]
    
def sql_specifications_modbus_register_map_drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql_specifications_modbus_register_map_create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for field in specifications_modbus_register_map_fields:
        fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            specification_modbus_register_map_id INTEGER PRIMARY KEY, 
            specification_id TEXT,
            {fields}
        )
    '''
    cur.execute(query)
    db.commit()
    db.close()

def sql_specifications_modbus_register_map_get_all(
    db_filepath,
    table_name,
):
    sql_specifications_modbus_register_map_create(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql_specifications_modbus_register_map_insert(
    db_filepath,
    table_name,
    specification_modbus_register_map_address_text,
    specification_modbus_register_map_parameter_text,
    sort_order_new,
    specification_id,
):
    # sql_specifications_modbus_register_map_drop(db_filepath, table_name,)
    sql_specifications_modbus_register_map_create(db_filepath, table_name,)
    # sql_specifications_modbus_register_map_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO {table_name} (
            specification_modbus_register_map_address_text,
            specification_modbus_register_map_parameter_text,
            sort_order,
            specification_id
        ) 
        VALUES (?, ?, ?, ?)
    ''', (
        specification_modbus_register_map_address_text,
        specification_modbus_register_map_parameter_text,
        sort_order_new,
        specification_id,
    ))
    db.commit()
    db.close()

def sql_specifications_modbus_register_map_delete(
    db_filepath,
    table_name,
    specification_modbus_register_map_id,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DELETE FROM {table_name} 
        WHERE specification_modbus_register_map_id = ?
    ''', (specification_modbus_register_map_id,))
    db.commit()
    db.close()

def sql_specifications_modbus_register_map_get_by_specification_id(
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

def sql__specifications__modbus_register_map__get_all_by_specification_id(
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
    db.close()
    return items


# ----------------------------------------------------------
# SQLITE GENERAL
# ----------------------------------------------------------

specifications_modbus_register_map_range_fields = [
    'specification_modbus_register_map_range_id',
    'specification_id',
    'sort_order',
    'specification_modbus_register_map_range_address_start_text',
    'specification_modbus_register_map_range_address_end_text',
    'specification_modbus_register_map_range_category_text',
]

def sql__drop(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql__create(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for i, field in enumerate(specifications_modbus_register_map_range_fields):
        if i == 0:
            fields.append(f'{field} INTEGER PRIMARY KEY')
        else:
            fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields}
        )
    '''
    # print(query)
    # quit()
    cur.execute(query)
    db.commit()
    db.close()

def sql__get_all(
    db_filepath,
    table_name,
):
    sql__create(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql__insert(
    db_filepath,
    table_name,
    fields,
):
    # sql__drop(db_filepath, table_name,)
    sql__create(db_filepath, table_name,)
    # sql_specifications_modbus_register_map_update(db_filepath, table_name,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    ###
    fields_insert = []
    for field in fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    ###
    question_marks = []
    for field in fields:
        question_marks.append('?')
    question_marks_insert = ', '.join(question_marks)
    ###
    fields_values = []
    for key, val in fields.items():
        fields_values.append(f'{val}')
    ###
    sql_query = f'''
        INSERT INTO {table_name} (
            {fields_insert}
        ) 
        VALUES ({question_marks_insert})
    '''
    # print(fields_values)
    # quit()
    cur.execute(sql_query, (*fields_values,))
    db.commit()
    db.close()

def sql__delete(
    db_filepath,
    table_name,
    fields,
):
    field_key = ''
    field_val = ''
    for key, val in fields.items():
        field_key = key
        field_val = val
        break
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    query = f'''
        DELETE FROM {table_name} 
        WHERE {field_key} = ?
    '''
    cur.execute(query, (field_val,))
    db.commit()
    db.close()

def sql__get_all__by_specification_id(
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
    db.close()
    return items

# ----------------------------------------------------------
# SQLITE MODBUS FUNCTION FC01
# ----------------------------------------------------------

specifications_modbus_function_fc01_fields = [
    'specification_modbus_function_fc01_id',
    'specification_id',
    'specification_modbus_function_fc01_request_intro_text',
    'specification_modbus_function_fc01_request_starting_address_text',
    'specification_modbus_function_fc01_request_quantity_of_coils_text',
    'specification_modbus_function_fc01_response_intro_text',
    'specification_modbus_function_fc01_response_byte_count_text',
    'specification_modbus_function_fc01_response_coil_status_text',
]

def sql__drop__new(
    db_filepath,
    table_name,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    cur.execute(f'''
        DROP TABLE IF EXISTS {table_name}
    ''')
    db.commit()
    db.close()

def sql__create__new(
    db_filepath,
    table_name,
    fields_names,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    fields = []
    for i, field in enumerate(fields_names):
        if i == 0:
            fields.append(f'{field} INTEGER PRIMARY KEY')
        else:
            fields.append(f'{field} TEXT')
    fields = ',\n'.join(fields)
    query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {fields}
        )
    '''
    # print(query)
    # quit()
    cur.execute(query)
    db.commit()
    db.close()

def sql__get_all__new(
    db_filepath,
    table_name,
    fields_names,
):
    sql__create__new(db_filepath, table_name, fields_names,)
    db = sqlite3.connect(db_filepath)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    rows = db.execute(f"SELECT * FROM {table_name}").fetchall()
    items = [dict(row) for row in rows]
    db.close()
    return items

def sql__insert__new(
    db_filepath,
    table_name,
    fields,
):
    fields_names = []
    for key, value in fields.items():
        fields_names.append(key)
    sql__drop__new(db_filepath, table_name,)
    sql__create__new(db_filepath, table_name, fields_names,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    ###
    fields_insert = []
    for field in fields:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    ###
    question_marks = []
    for field in fields:
        question_marks.append('?')
    question_marks_insert = ', '.join(question_marks)
    ###
    fields_values = []
    for key, val in fields.items():
        fields_values.append(f'{val}')
    ###
    sql_query = f'''
        INSERT INTO {table_name} (
            {fields_insert}
        ) 
        VALUES ({question_marks_insert})
    '''
    # print(fields_values)
    # quit()
    cur.execute(sql_query, (*fields_values,))
    db.commit()
    db.close()

def sql__delete__new(
    db_filepath,
    table_name,
):
    field_key = ''
    field_val = ''
    for key, val in fields.items():
        field_key = key
        field_val = val
        break
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    query = f'''
        DELETE FROM {table_name} 
        WHERE {field_key} = ?
    '''
    cur.execute(query, (field_val,))
    db.commit()
    db.close()

def sql__get_all__by_specification_id__new(
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
    db.close()
    return items

def sql__update__cols__new(
    db_filepath,
    table_name,
    specification_fields,
):
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    columns = {}
    for field in specification_fields:
        columns[field] = 'TEXT'
    existing = {row[1] for row in cur.execute(f"PRAGMA table_info({table_name})")}
    for name, definition in columns.items():
        if name not in existing:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
    db.commit()
    db.close()

def sql__set__new(
    db_filepath,
    table_name,
    specification_id,
    specification_fields,
):
    
    fields_names = []
    fields_values = []
    for key, value in specification_fields.items():
        fields_names.append(key)
        fields_values.append(value)

    sql__create__new(db_filepath, table_name, fields_names,)
    sql__update__cols__new(db_filepath, table_name, specification_fields,)
    db = sqlite3.connect(db_filepath)
    cur = db.cursor()
    
    fields_insert = []
    for field in fields_names:
        fields_insert.append(f'{field}')
    fields_insert = ',\n'.join(fields_insert)
    ###
    fields_update = []
    for field in fields_names:
        fields_update.append(f'{field} = excluded.{field}')
    fields_update = ',\n'.join(fields_update)
    ###
    question_marks = []
    for field in fields_names:
        question_marks.append('?')
    question_marks_insert = ', '.join(question_marks)

    query = f'''
        INSERT INTO {table_name} (
            {fields_insert}
        ) 
        VALUES ({question_marks_insert})
        ON CONFLICT(specification_id) DO UPDATE SET
            {fields_update}
    '''
    print(query)
    
    cur.execute(query, (
        *fields_values,
    ))
    db.commit()
    db.close()