from config import db

def copy_csv_to_db():
    # Get the connection from db.py
    conn = db.get_connection()
    cur = conn.cursor()

    # Copy data from CSV to the Employee table
    with open('data/employees.csv', 'r') as f:
        next(f)  # Skip the header
        cur.copy_from(f, 'Employee', sep=',')

    # Copy data from CSV to the Project table
    with open('data/projects.csv', 'r') as f:
        next(f)  # Skip the header
        cur.copy_from(f, 'Project', sep=',')

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    copy_csv_to_db()
