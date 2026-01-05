# Part 4: Database Migrations with Flask-Migrate

## One-Line Summary
Database migrations using Flask-Migrate (Alembic) for safe schema changes

## What You'll Learn
- Why migrations are important
- Setting up Flask-Migrate
- Creating and applying migrations
- Adding new columns without losing data

## Prerequisites
- Complete part-3 (Flask-SQLAlchemy)
- Install: `pip install flask-migrate`

## Why Migrations?

### Without Migrations (BAD):
```
1. You add a new column to your model
2. Old database doesn't have that column
3. Options:
   - Delete database and recreate (LOSE ALL DATA!)
   - Manually alter table (error-prone)
```

### With Migrations (GOOD):
```
1. You add a new column to your model
2. Run: flask db migrate -m "Add phone column"
3. Run: flask db upgrade
4. Column added! No data lost!
```

## How to Run

### First Time Setup:
```bash
cd part-4
pip install flask-migrate

# Set Flask app environment variable
# Windows:
set FLASK_APP=app.py
# Mac/Linux:
export FLASK_APP=app.py

# Initialize migrations (creates 'migrations' folder)
flask db init

# Create first migration
flask db migrate -m "Initial migration"

# Apply migration (creates tables)
flask db upgrade

# Run the app
python app.py
```

### After Changing Models:
```bash
flask db migrate -m "Describe what you changed"
flask db upgrade
```

## Migration Commands Cheatsheet

| Command | Description |
|---------|-------------|
| `flask db init` | Initialize migrations (first time only) |
| `flask db migrate -m "message"` | Create new migration |
| `flask db upgrade` | Apply pending migrations |
| `flask db downgrade` | Undo last migration |
| `flask db current` | Show current migration |
| `flask db history` | Show all migrations |

## Key Files
```
part-4/
├── app.py              <- Models with new fields
├── migrations/         <- Created by flask db init
│   └── versions/       <- Migration files stored here
├── templates/
│   ├── index.html      <- Shows new columns
│   ├── add.html
│   ├── edit.html
│   └── courses.html
└── README.md
```

## New Fields Added (via migration)
- `Student.phone` - Phone number
- `Student.enrolled_at` - Enrollment date
- `Student.is_active` - Active status
- `Course.created_at` - Creation timestamp

## Exercise
1. Add a new field `address` to Student model
2. Create and apply migration
3. Verify the field appears in database

## Next Step
→ Go to **part-5** to learn user authentication with password hashing
