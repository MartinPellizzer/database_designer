# import sqlite3

# conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
# conn.execute("ALTER TABLE requirements RENAME TO statements")
# conn.commit()
# conn.close()

# import sqlite3

# conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
# conn = sqlite3.connect("test.db")
# conn.execute("ALTER TABLE categories RENAME COLUMN category_text TO category_lvl1_text")
# conn.execute("ALTER TABLE statements RENAME COLUMN requirement_text TO statement_text")
# conn.execute("ALTER TABLE categories ADD COLUMN category_lvl1_text TEXT")
# conn.execute("ALTER TABLE categories ADD COLUMN sort_order INTEGER")
# conn.execute("UPDATE categories SET sort_order = rowid")
# conn.execute("ALTER TABLE specifications ADD COLUMN template TEXT")
# conn.execute("ALTER TABLE specifications RENAME COLUMN template TO specification_template_text")
# conn.execute("ALTER TABLE specifications_modbus ADD COLUMN specification_modbus_device_id_text TEXT")
# conn.execute("ALTER TABLE specifications_modbus ADD COLUMN specification_modbus_data_bits_text TEXT")
# conn.execute("ALTER TABLE specifications_modbus ADD COLUMN specification_modbus_stop_bits_text TEXT")
# conn.execute("ALTER TABLE specifications_modbus ADD COLUMN specification_modbus_parity_text TEXT")
# conn.execute("ALTER TABLE specifications_modbus_report RENAME TO specifications_modbus_read;")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_intro_text TO specification_modbus_read_intro_text")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_module_id_text TO specification_modbus_read_module_id_text")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_function_code_text TO specification_modbus_read_function_code_text")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_bytes_number_text TO specification_modbus_read_bytes_number_text")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_register_value_text TO specification_modbus_read_register_value_text")
# conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_crc16_text TO specification_modbus_read_crc16_text")
            
# conn.commit()
# conn.close()

import sqlite3
import json
from lib import sql_utils

conn = sqlite3.connect("mydb.sqlite")
fields = [row[1] for row in conn.execute("PRAGMA table_info(mytable)")]

db_filepath = 'requirements_projects/modulo_relay_x8.db'
table_name = 'specifications_modbus_write_table_name'
# table_name = 'specifications_modbus_write_response_table_name'

# sql_utils.sql_specifications_modbus_write_create(db_filepath, table_name,)
# conn = sqlite3.connect(db_filepath)
# fields = [row[1] for row in conn.execute(f"PRAGMA table_info({table_name})")]
# for field in fields:
#     print(field)
# quit()

# table specifications_modbus_write_response has no column named specification_modbus_write_response_slave_id_text

sql_utils.sql_specifications_modbus_write_drop(db_filepath, table_name)
sql_utils.sql_specifications_modbus_write_create(db_filepath, table_name)
sql_utils.sql_specifications_modbus_write_update(db_filepath, table_name)
print(sql_utils.sql_specifications_modbus_write_get_all(db_filepath, table_name))

specification_fields = [
    '01',
    '05',
    '00',
    '00',
    'FF',
    '00',
]

sql_utils.sql_specifications_modbus_write_set(
    db_filepath,
    table_name,
    '0',
    specification_fields,
)

print(json.dumps(sql_utils.sql_specifications_modbus_write_get_all(db_filepath, table_name), indent=4))


# sql_utils.sql_specifications_modbus_write_response_drop(db_filepath, table_name,)