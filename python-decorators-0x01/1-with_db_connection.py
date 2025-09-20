import sqlite3
import functools

# ===============================
# Decorator to handle DB connection
# ===============================
def with_db_connection(func):
    @functools.wraps(func)  # preserves original function metadata
    def wrapper(*args, **kwargs):
        # Open the database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function and pass the connection as the first argument
            result = func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is always closed
            conn.close()
        return result
    return wrapper

# ===============================
# Example function using the decorator
# ===============================
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ===============================
# Test the decorator
# ===============================
user = get_user_by_id(user_id=1)
print(user)
