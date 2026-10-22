# import sqlite3

# conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
# conn.execute("ALTER TABLE requirements RENAME TO statements")
# conn.commit()
# conn.close()

# import sqlite3

# conn = sqlite3.connect("requirements_projects/modulo_relay_x8.db")
# conn.execute("ALTER TABLE statements RENAME COLUMN requirement_id TO statement_id")
# conn.execute("ALTER TABLE statements RENAME COLUMN requirement_text TO statement_text")
# conn.execute("ALTER TABLE requirements ADD COLUMN sort_order INTEGER")
# conn.execute("UPDATE requirements SET sort_order = rowid")
# conn.commit()
# conn.close()