import sqlite3
import functools

# ===============================
# Decorator to log SQL queries
# ===============================
def log_queries(func):
    @functools.wraps(func)  # preserves original function name & docstring
    def wrapper(*args, **kwargs):
        # Try to get the query from keyword arguments
        query = kwargs.get('query')
        # If not found, assume the first positional argument is the query
        if not query and len(args) > 0:
            query = args[0]
        
        # Log the SQL query
        print(f"[SQL QUERY]: {query}")
        
        # Call the original function
        return func(*args, **kwargs)
    
    return wrapper

# ===============================
# Example function using the decorator
# ===============================
@log_queries
def fetch_all_users(query):
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Execute the SQL query
    cursor.execute(query)
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# ===============================
# Test the decorator
# ===============================
users = fetch_all_users(query="SELECT * FROM users")
print(users)
