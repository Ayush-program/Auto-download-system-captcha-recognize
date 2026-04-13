from database.db_connection import get_connection

def create_state_table(table_name):
    conn = get_connection()
    cur = conn.cursor()

    sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tender_id VARCHAR(100) UNIQUE,
        pdf_path VARCHAR(255),
        state varchar(50),
        downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def table_exists(table_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        AND table_name = %s
    """, (table_name,))

    exists = cur.fetchone()[0] == 1

    cur.close()
    conn.close()
    return exists


def ensure_state_table(state):

    table_name = state

    if not table_exists(table_name):
        print(f"🆕 Creating table for state: {state}")
        create_state_table(table_name)
    else:
        print(f"✅ Table already exists for state: {state}")

    return table_name
