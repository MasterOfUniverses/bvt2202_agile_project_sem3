import sqlite3

# with open('create_script.sql', 'r') as sql_file:
#     create_script = sql_file.read()
#
# with open('insert_script.sql', 'r') as sql_file:
#     insert1 = sql_file.read()
#
# with open('insert_script_2.sql', 'r') as sql_file:
#     insert2 = sql_file.read()

db = sqlite3.connect('testDB.db')
cur = db.cursor()
cur.execute("SELECT * FROM times WHERE id=1;")

print(cur.fetchall())
#
# cur.executescript(create_script)
# db.commit()
#
# cur.executescript(insert1)
# db.commit()
#
# cur.executescript(insert2)
# db.commit()
#
db.close()