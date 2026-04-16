import psycopg2

def get_connection():
    return psycopg2.connect(
        host="64.227.171.26",
        database="Attendance_tracking",
        user="postgres",
        password="pro@123"
    )
