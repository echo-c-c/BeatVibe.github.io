import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='demo'
    )

def remove_duplicate_usernames():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 删除重复的用户名，保留每个用户名的第一条记录
            cursor.execute("""
                DELETE FROM base
                WHERE id NOT IN (
                    SELECT * FROM (
                        SELECT MIN(id) as id
                        FROM base
                        GROUP BY name
                    ) as temp
                );
            """)
            connection.commit()
            print("Duplicate usernames removed successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    remove_duplicate_usernames()