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
# Task 4: Cache query decorator
# ==================================
query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query string (assumes keyword or positional argument)
        query = kwargs.get('query')
        if not query and len(args) > 0:
            query = args[0]
        
        # Check if the query is already cached
        if query in query_cache:
            print("[CACHE]: Returning cached result")
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("[CACHE]: Result cached")
        return result
    return wrapper

# ==================================
# Example function using both decorators
# ==================================
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ==================================
# Test the decorator
# ==================================
# First call → executes query and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call → uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
