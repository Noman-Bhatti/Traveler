import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('users.db')

# Create a table for storing user data
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USERNAME TEXT NOT NULL,
             PASSWORD TEXT NOT NULL);''')


# Function to register a new user
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Insert user data into the database
    conn.execute("INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))
    conn.commit()

    print("Registration successful!")


# Function to authenticate user login
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Retrieve user data from the database
    cursor = conn.execute("SELECT * FROM users WHERE USERNAME = ? AND PASSWORD = ?", (username, password))

    # Check if user exists and password matches
    if len(cursor.fetchall()) > 0:
        print("Login successful!")
    else:
        print("Invalid username or password")


# Ask user for registration or login
while True:
    choice = input("Press 1 to register, 2 to login, or 0 to exit: ")

    if choice == '1':
        register()
    elif choice == '2':
        login()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")

# Close database connection
conn.close()
