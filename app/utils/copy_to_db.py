from app.config import db

# TODO: Fix the error below
# from app.config import db
# ModuleNotFoundError: No module named 'app'

def copy_csv_to_db():
    # Get the connection from db.py
    conn = db.get_connection()
    cur = conn.cursor()

    # Copy data from CSV to the Employee table
    with open('data/employees.csv', 'r', encoding='utf-8') as f:
        next(f)  # Skip the header
        cur.copy_from(f, 'employee', sep=',')

    # Copy data from CSV to the Project table
    with open('data/projects.csv', 'r', encoding='utf-8') as f:
        next(f)  # Skip the header
        cur.copy_from(f, 'project', sep=',')

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    copy_csv_to_db()
