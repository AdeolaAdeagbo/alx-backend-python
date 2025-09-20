import sqlite3
import functools

# ==================================
# Task 1: Decorator to handle DB connection
# ==================================
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# ==================================
# Task 2: Transaction management decorator
# ==================================
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the function
            conn.commit()  # Commit if no errors
            print("[TRANSACTION]: COMMITTED")
        except Exception as e:
            conn.rollback()  # Rollback if there’s an error
            print("[TRANSACTION]: ROLLED BACK")
            raise e  # Re-raise the exception for visibility
        return result
    return wrapper

# ==================================
# Example function using both decorators
# ==================================
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?", 
        (new_email, user_id)
    )

# ==================================
# Test the decorator
# ==================================
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
