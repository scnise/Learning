import sqlite3 
DB = "portfolio.db"
def init():
    c = sqlite3.connect(DB)
    cursor = c.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER           
                   )
    """)    
    c.commit()
    c.close()
def adding(username, id):
    c = sqlite3.connect(DB)
    cursor = c.cursor()
    cursor.execute("SELECT name FROM users WHERE name = ?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (name,age) VALUES (?,?)", (username,id))
        c.commit()
        c.close()
        return True
    c.close()
    return False
def show():
    c = sqlite3.connect(DB)
    cursor = c.cursor()
    cursor.execute("SELECT * FROM users")
    b = cursor.fetchall()
    c.close()
    return b
def delete(username):
    c = sqlite3.connect(DB)
    cursor = c.cursor()
    cursor.execute("DELETE FROM users WHERE name = ?", (username,))
    c.commit()
    c.close()
def find(username):
    c = sqlite3.connect(DB)
    cursor = c.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (username,))
    b = cursor.fetchall()
    return b