from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
def get_db_connection():
    conn = sqlite3.connect('travel.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    destinations = conn.execute('SELECT * FROM destinations').fetchall()
    conn.close()
    return render_template('base.html', destinations=destinations)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            flash('Login Successful!')
            return redirect(url_for('destinations'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Signup Successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()
    return render_template('signup.html')

# Destinations
@app.route('/destinations')
def destinations():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    destinations = conn.execute('SELECT * FROM destinations').fetchall()
    conn.close()
    return render_template('destinations.html', destinations=destinations)

# Book
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        destination = request.form['destination']
        # Add booking logic here (e.g., save to database)
        flash('Booking Successful!', 'success')
        return render_template('booking.html', destinations=destinations, booking_success=True)

    # For GET requests, show the form
    return render_template('booking.html', destinations=destinations, booking_success=False)



# My Bookings
@app.route('/my_bookings')
def my_bookings():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.booking_date, d.name, d.description, d.price 
        FROM bookings b 
        JOIN destinations d ON b.destination_id = d.id 
        WHERE b.user_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save contact data to the database or send an email (logic depends on your setup)
        print(f"Received contact request from {name} ({email}): {message}")

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')



@app.route('/logout')
def logout():
    session.clear()  # Clear user session
    return redirect(url_for('login'))  # Redirect to login page


if __name__ == "__main__":
    app.run(debug=True)
