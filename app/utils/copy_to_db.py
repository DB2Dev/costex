from app.config.db import db

cur = db.cursor()

# Copy data from CSV to tables
with open('data/employees.csv', 'r') as f:
    next(f)  # Skip the header
    cur.copy_from(f, 'Employee', sep=',')

# Commit and close
db.commit()
cur.close()
db.close()