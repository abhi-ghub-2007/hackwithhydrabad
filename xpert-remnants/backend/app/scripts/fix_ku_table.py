import sqlite3

conn = sqlite3.connect('xpert_remnants.db')
c = conn.cursor()
cols = [col[1] for col in c.execute('PRAGMA table_info(knowledge_updates)').fetchall()]
print('Existing cols in knowledge_updates:', cols)
if 'update_type' not in cols:
    c.execute("ALTER TABLE knowledge_updates ADD COLUMN update_type TEXT DEFAULT 'DECISION_CHANGE'")
    print('Added update_type column.')
conn.commit()
conn.close()
print('Migration complete!')
