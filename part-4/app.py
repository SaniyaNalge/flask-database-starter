"""
Part 4: Database Migrations with Flask-Migrate
===============================================
Learn to evolve your database schema without losing data!

What You'll Learn:
- Why migrations are important
- Setting up Flask-Migrate
- Creating and applying migrations
- Adding new columns to existing tables

Prerequisites: Complete part-3
Install: pip install flask-migrate
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Flask-Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate


# =============================================================================
# MODELS - Now with more fields (imagine adding these later)
# =============================================================================

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # NEW: Track creation time

    students = db.relationship('Student', backref='course', lazy=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))  # NEW: Added phone field
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)  # NEW: Enrollment date
    is_active = db.Column(db.Boolean, default=True)  # NEW: Active status

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    students = Student.query.order_by(Student.enrolled_at.desc()).all()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_student = Student(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form.get('phone', ''),  # Optional field
            course_id=request.form['course_id']
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('add.html', courses=courses)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.phone = request.form.get('phone', '')
        student.course_id = request.form['course_id']
        student.is_active = 'is_active' in request.form  # Checkbox handling

        db.session.commit()
        flash('Student updated!', 'success')
        return redirect(url_for('index'))

    courses = Course.query.all()
    return render_template('edit.html', student=student, courses=courses)


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted!', 'danger')
    return redirect(url_for('index'))


@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)


if __name__ == '__main__':
    app.run(debug=True)


# =============================================================================
# MIGRATION COMMANDS (Run in terminal):
# =============================================================================
#
# STEP 1: Initialize migrations (only once per project)
#   flask db init
#   → Creates 'migrations' folder
#
# STEP 2: Create a migration (after changing models)
#   flask db migrate -m "Add phone and enrolled_at to Student"
#   → Creates a migration file in migrations/versions/
#
# STEP 3: Apply the migration
#   flask db upgrade
#   → Updates the database schema
#
# =============================================================================
# WHY MIGRATIONS?
# =============================================================================
#
# Problem without migrations:
#   - You add a new column to your model
#   - Old database doesn't have that column
#   - App crashes! Or you lose all data by recreating DB
#
# Solution with migrations:
#   - Migrations track all schema changes
#   - Apply changes incrementally without losing data
#   - Can rollback if something goes wrong
#
# =============================================================================
# COMMON MIGRATION COMMANDS:
# =============================================================================
#
# flask db init          - Initialize (first time only)
# flask db migrate -m "" - Create new migration
# flask db upgrade       - Apply migrations
# flask db downgrade     - Undo last migration
# flask db current       - Show current migration
# flask db history       - Show migration history
#
# =============================================================================
