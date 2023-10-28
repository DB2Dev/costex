import psycopg2

# Connect to PostgreSQL
db = psycopg2.connect(
    dbname="mydb",
    user="admin",
    password="password",
    host="localhost",
    port="5432"
)