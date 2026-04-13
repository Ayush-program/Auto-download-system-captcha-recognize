from database.db_connection import get_connection

def tender_exists(tender_id,table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT 1 FROM {table_name} WHERE tender_id = %s LIMIT 1",
        (tender_id,)
    )

    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists
