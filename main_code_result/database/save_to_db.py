import mysql.connector
from database.db_connection import get_connection

def save_pdf_data(tender_id, pdf_path,state,table_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = f"""
        INSERT IGNORE INTO {table_name} (tender_id, pdf_path,state)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (tender_id, pdf_path,state))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"⏭ Duplicate ignored by DB | {tender_id}")
        else:
            print(f"✅ save the : {tender_id} into database")

    except mysql.connector.Error as err:
        print("❌ MySQL ERROR:")
        print(err)

    except Exception as e:
        print("❌ Python ERROR:")
        print(e)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
