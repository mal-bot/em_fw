import sqlite3

con = sqlite3.connect('patterns.sqlite')
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)

print(cur.execute('SELECT * FROM student;').fetchall())
print(cur.execute('SELECT * FROM category;').fetchall())
print(cur.execute('SELECT name, category_id FROM category WHERE id=1;').fetchone())
print(cur.execute('SELECT * FROM course;').fetchall())
cur.close()
con.close()