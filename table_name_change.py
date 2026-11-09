# import sqlite3

# conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
# conn.execute("ALTER TABLE requirements RENAME TO statements")
# conn.commit()
# conn.close()

import sqlite3

conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
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
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_intro_text TO specification_modbus_read_intro_text")
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_module_id_text TO specification_modbus_read_module_id_text")
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_function_code_text TO specification_modbus_read_function_code_text")
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_bytes_number_text TO specification_modbus_read_bytes_number_text")
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_register_value_text TO specification_modbus_read_register_value_text")
conn.execute("ALTER TABLE specifications_modbus_read RENAME COLUMN specification_modbus_report_crc16_text TO specification_modbus_read_crc16_text")
            
conn.commit()
conn.close()