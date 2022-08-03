import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '21232f297a57a5a743894a0e4a801fc3'))
    cur.execute("INSERT INTO posts (title, content, username) VALUES (?, ?, ?)", ('Test', 'Test content for the test post', 'admin'))
    connection.commit()
    connection.close()
