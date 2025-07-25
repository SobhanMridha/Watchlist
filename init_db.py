import sqlite3

def create_db():
    connect = sqlite3.connect("database.db")
    cursor = connect.cursor()

    # users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    # watchlist table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # watched table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watched (
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        UNIQUE(user_id, movie_id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    connect.commit()
    connect.close()


if __name__ == "__main__":
    create_db()
