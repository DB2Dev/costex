from config import db

# TODO: Fix the error below
# psycopg2.errors.BadCopyFileFormat: extra data after last expected column
# CONTEXT:  COPY employee, line 1: "Peter,N,Woods,2022-04-26,"1148 Samantha Park Apt. 624, Amberton, MI 15027""
# TODO: Fix the error below
# from app.config import db
# ModuleNotFoundError: No module named 'app'

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
