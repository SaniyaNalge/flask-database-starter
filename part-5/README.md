# Part 5: User Authentication with Password Hashing

## One-Line Summary
User authentication with password hashing and sessions

## What You'll Learn
- User registration with hashed passwords
- Login/Logout functionality
- Session management with Flask-Login
- Protecting routes with `@login_required`

## Prerequisites
- Complete part-3 and part-4
- Install: `pip install flask-login werkzeug`

## How to Run
```bash
cd part-5
pip install flask-login werkzeug
python app.py
```
Open: http://localhost:5000

## Authentication Flow

```
REGISTRATION:
User enters password → generate_password_hash() → Store hash in DB

LOGIN:
User enters password → check_password_hash() → If match → Create session

PROTECTED ROUTE:
Request → Check session → User logged in? → Yes: Allow / No: Redirect to login

LOGOUT:
Clear session → Redirect to home
```

## Key Concepts

### 1. Password Hashing (NEVER store plain passwords!)
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When registering
password_hash = generate_password_hash('mypassword')
# Result: 'pbkdf2:sha256:260000$...'

# When logging in
check_password_hash(password_hash, 'mypassword')  # Returns True
check_password_hash(password_hash, 'wrongpass')   # Returns False
```

### 2. Flask-Login Essentials
```python
from flask_login import login_user, logout_user, current_user, login_required

login_user(user)      # Create session
logout_user()         # Clear session
current_user          # Access logged-in user
@login_required       # Protect route decorator
```

### 3. UserMixin
```python
class User(UserMixin, db.Model):
    # UserMixin adds these methods automatically:
    # - is_authenticated
    # - is_active
    # - is_anonymous
    # - get_id()
```

## Key Files
```
part-5/
├── app.py              <- Auth routes and User model
├── templates/
│   ├── home.html       <- Public landing page
│   ├── register.html   <- Registration form
│   ├── login.html      <- Login form
│   ├── dashboard.html  <- Protected page
│   └── profile.html    <- User profile (protected)
└── README.md
```

## Security Best Practices
1. NEVER store plain text passwords
2. Use strong `secret_key` (generate with `secrets.token_hex(16)`)
3. Use HTTPS in production
4. Add rate limiting to prevent brute force attacks
5. Validate password strength

## Exercise
1. Add a "Change Password" feature
2. Add "Remember Me" checkbox using `login_user(user, remember=True)`
3. Add password strength validation (min length, special chars)

## Next Step
→ Go to **part-6** to learn REST API for database operations
