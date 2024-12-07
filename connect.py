import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    try:
        # 创建连接
        connection = mysql.connector.connect(
            host='localhost',  # 数据库主机地址
            user='root',       # 数据库用户名
            password='123456', # 数据库密码
            database='demo'    # 数据库名称
        )

        if connection.is_connected():
            print("Successfully connected to the database")

            # 创建游标对象
            cursor = connection.cursor()

            # 执行查询
            cursor.execute("SELECT * FROM base")

            # 获取查询结果
            result = cursor.fetchall()

            for row in result:
                print(row)

    except Error as e:
        print(f"Error: {e}")

    finally:
        # 关闭连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    connect_to_mysql()
