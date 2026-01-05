"""
Part 5: User Authentication with Password Hashing
==================================================
Secure user registration and login system.

What You'll Learn:
- User registration with hashed passwords
- Login/Logout functionality
- Session management
- Protecting routes (login required)
- Flask-Login extension

Prerequisites: Complete part-3 and part-4
Install: pip install flask-login werkzeug
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this'  # IMPORTANT: Change in production!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =============================================================================
# FLASK-LOGIN SETUP
# =============================================================================
login_manager = LoginManager(app)  # Initialize Flask-Login
login_manager.login_view = 'login'  # Redirect here if not logged in
login_manager.login_message = 'Please login to access this page.'  # Flash message


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login needs this to reload user from session"""
    return User.query.get(int(user_id))


# =============================================================================
# USER MODEL
# =============================================================================

class User(UserMixin, db.Model):  # UserMixin adds required methods for Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Store hash, NOT plain password!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash the password before storing"""
        self.password_hash = generate_password_hash(password)  # Creates secure hash

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)  # Returns True/False

    def __repr__(self):
        return f'<User {self.username}>'


# =============================================================================
# PUBLIC ROUTES (No login required)
# =============================================================================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Already logged in
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)  # Hash the password!

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Check hashed password
            login_user(user)  # Create session
            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect to 'next' page if exists (for login_required redirect)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required  # Must be logged in to logout
def logout():
    logout_user()  # Clear session
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# =============================================================================
# PROTECTED ROUTES (Login required)
# =============================================================================

@app.route('/dashboard')
@login_required  # This decorator protects the route!
def dashboard():
    return render_template('dashboard.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# =============================================================================
# INITIALIZE DATABASE
# =============================================================================

def init_db():
    with app.app_context():
        db.create_all()
        print('Database created!')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# =============================================================================
# KEY CONCEPTS:
# =============================================================================
#
# 1. Password Hashing (NEVER store plain passwords!)
#    - generate_password_hash('password') → Creates hash like 'pbkdf2:sha256:...'
#    - check_password_hash(hash, 'password') → Returns True if match
#
# 2. Flask-Login
#    - UserMixin: Adds is_authenticated, is_active, get_id() methods
#    - login_user(user): Creates session, user is now logged in
#    - logout_user(): Clears session
#    - current_user: Access logged-in user anywhere
#    - @login_required: Protects routes
#
# 3. Session Flow:
#    Register → Hash password → Store in DB
#    Login → Check hash → Create session → Redirect
#    Access protected page → Check session → Allow or redirect
#    Logout → Clear session
#
# =============================================================================
# SECURITY BEST PRACTICES:
# =============================================================================
#
# - NEVER store plain text passwords
# - Use strong secret_key (generate with: python -c "import secrets; print(secrets.token_hex(16))")
# - Use HTTPS in production
# - Add rate limiting to prevent brute force
# - Validate input (email format, password strength)
#
# =============================================================================
