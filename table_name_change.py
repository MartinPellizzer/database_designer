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
conn.execute("ALTER TABLE specifications RENAME COLUMN template TO specification_template_text")
conn.commit()
conn.close()