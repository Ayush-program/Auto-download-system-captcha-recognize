import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",        # 🔥 force IPv4 (NOT localhost)
        port=3306,
        user="root",
        password="Ayush@2005",
        database="tender_db",
        connection_timeout=5,
        use_pure=True            # 🔥 prevents socket hang
    )
