import sqlite3


DATABASE = "database/astra.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            age INTEGER,
            password TEXT,
            face_registered INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL,

    sender TEXT NOT NULL,

    message TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

    connection.commit()
    connection.close()


def owner_exists():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    count = cursor.fetchone()[0]

    connection.close()

    return count > 0


def create_owner(full_name, username, email, age, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users
        (full_name, username, email, age, password)
        VALUES (?, ?, ?, ?, ?)
    """, (full_name, username, email, age, password))

    connection.commit()
    connection.close()

def get_user(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user

def save_chat(username, sender, message):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chats(username, sender, message)
        VALUES (?, ?, ?)
    """, (username, sender, message))

    connection.commit()
    connection.close()

def get_chat_history(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sender, message
        FROM chats
        WHERE username = ?
        ORDER BY id
    """, (username,))

    chats = cursor.fetchall()

    connection.close()

    return chats

def update_user(full_name, username, email, age):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET
            full_name = ?,
            email = ?,
            age = ?
        WHERE username = ?
    """, (

        full_name,
        email,
        age,
        username

    ))

    connection.commit()
    connection.close()

def change_password(username, new_password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""

        UPDATE users

        SET password = ?

        WHERE username = ?

    """, (

        new_password,
        username

    ))

    connection.commit()
    connection.close()