import time
import sqlite3
import functools

# ==================================
# Reuse Task 1: Handle DB Connection
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
# Task 3: Retry decorator
# ==================================
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)  # Try to run the function
                except Exception as e:
                    attempt += 1
                    print(f"[RETRY]: Attempt {attempt} failed with error: {e}")
                    if attempt < retries:
                        time.sleep(delay)  # Wait before retrying
                    else:
                        print("[RETRY]: All attempts failed.")
                        raise  # Raise exception if all retries fail
        return wrapper
    return decorator

# ==================================
# Example function using both decorators
# ==================================
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ==================================
# Test the decorator
# ==================================
users = fetch_users_with_retry()
print(users)
