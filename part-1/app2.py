from flask import Flask, render_template
import sqlite3  # Built-in Python library for SQLite database

app = Flask(__name__)

DATABASE = 'teachers.db'  # Database file name (will be created automatically)


# =============================================================================
# DATABASE HELPER FUNCTIONS
# =============================================================================

def get_db_connection():
    """Create a connection to the database"""
    conn = sqlite3.connect(DATABASE)  # Connect to database file
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name (like dict)
    return conn


def init_db():
    """Create the table if it doesn't exist"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')  # SQL command to create table with 4 columns
    conn.commit()  # Save changes to database
    conn.close()  # Close connection


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def teach():
    """Home page - Display all students from database"""
    conn = get_db_connection()  # Step 1: Connect to database
    teachers = conn.execute('SELECT * FROM teachers').fetchall()  # Step 2: Get all rows
    conn.close()  # Step 3: Close connection
    return render_template('teach.html', teachers=teachers)


@app.route('/add')
def add_sample_teacher():
    """Add a sample Teachers to database (for testing)"""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO teachers (name, email, course) VALUES (?, ?, ?)',
        ('Mr. John', 'john@154gmail.com', 'BE Comp')  # ? are placeholders (safe from SQL injection)
    )
    conn.commit()  # Don't forget to commit!
    conn.close()
    return 'Teacher added! <a href="/">Go back to home</a>'


if __name__ == '__main__':
    init_db()  # Create table when app starts
    app.run(debug=True)
