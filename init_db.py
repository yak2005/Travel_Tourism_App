import sqlite3

# Connect to SQLite (creates 'travel.db' if it doesn't exist)
conn = sqlite3.connect('travel.db')

# Create 'users' table
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Create 'destinations' table
conn.execute('''
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL
)
''')

# Create 'bookings' table
conn.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (destination_id) REFERENCES destinations (id)
)
''')

# Insert sample data into 'destinations' table
conn.execute('INSERT INTO destinations (name, description, price, image) VALUES ("Paris", "City of Light", 2000, "paris.jpeg")')
conn.execute('INSERT INTO destinations (name, description, price, image) VALUES ("London", "Historic Charm", 1800, "london.jpeg")')
conn.execute('INSERT INTO destinations (name, description, price, image) VALUES ("New York", "The Big Apple", 2200, "newyork.jpeg")')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully!")
