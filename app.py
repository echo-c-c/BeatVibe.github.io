from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 添加文件检测函数
def check_user_point_file():
    file_path = os.path.join(os.path.dirname(__file__), 'user_point.txt')
    if os.path.exists(file_path):
        print("文件已检测")
        return True
    else:
        # 如果文件不存在，创建一个空文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
            print("文件不存在，已创建新文件")
            return True
        except Exception as e:
            print(f"创建文件失败: {e}")
            return False

# 在应用启动时检测文件
check_user_point_file()

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
            cursor.execute("""
                DELETE FROM base
                WHERE id NOT IN (
                    SELECT MIN(id)
                    FROM base
                    GROUP BY name
                );
            """)
            connection.commit()
    finally:
        connection.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['name']
    password = request.form['password']
    role = request.form['role']
    
    if role == 'admin':
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM root WHERE name=%s AND password=%s", (username, password))
                admin = cursor.fetchone()
        finally:
            connection.close()
        
        if admin:
            return jsonify({"success": True, "message": "Admin login successful"})
        else:
            return jsonify({"success": False, "message": "管理员登录失败，请重试"})
    else:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, maxpoint FROM base WHERE name=%s AND password=%s", (username, password))
                user = cursor.fetchone()
        finally:
            connection.close()
        
        if user:
            return jsonify({
                "success": True, 
                "message": "Login successful",
                "username": user[1],
                "score": user[2] or 0  # 返回用户最高分
            })
        else:
            return jsonify({"success": False, "message": "登录失败，请重试"})

@app.route('/register', methods=['POST'])
def register():
    username = request.form['name']
    password = request.form['password']
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    users = 'default_value'
    initial_score = 0   # 设置初始分数为0
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM base WHERE name=%s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return render_template('login.html', error="用户名已存在，请选择其他用户名")
            
            # 插入新用户，包括初始分数
            cursor.execute(
                "INSERT INTO base (name, password, time, users, maxpoint) VALUES (%s, %s, %s, %s, %s)", 
                (username, password, time, users, initial_score)
            )
            connection.commit()
    finally:
        connection.close()
    
    return jsonify({
        'success': True,
        'message': '注册成功'
    })

@app.route('/admin')
def admin_dashboard():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 获取用户列表
            cursor.execute("SELECT id, name, password, time, maxpoint FROM base")
            users = cursor.fetchall()
            
            # 获取用户总数
            cursor.execute("SELECT COUNT(*) FROM base")
            total_users = cursor.fetchone()[0]
            
            # 获取今日注册用户数
            cursor.execute("""
                SELECT COUNT(*) FROM base 
                WHERE DATE(time) = CURDATE()
            """)
            today_users = cursor.fetchone()[0]
            
            return render_template('admin.html', 
                                users=users,
                                total_users=total_users,
                                today_users=today_users)
                                
    except Error as e:
        print(f"Database error: {e}")
        return str(e), 500
    finally:
        if connection.is_connected():
            connection.close()

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            # 构建更新语句
            update_parts = []
            values = []
            
            # 检查并添加各个字段的更新
            if 'username' in data:
                update_parts.append('name = %s')
                values.append(data['username'])
            
            if 'password' in data and data['password']:
                update_parts.append('password = %s')
                values.append(data['password'])
            
            if 'register_date' in data:
                update_parts.append('time = %s')
                values.append(data['register_date'])
            
            if 'high_score' in data:
                update_parts.append('maxpoint = %s')
                values.append(int(data['high_score']))

            if update_parts:
                # 构建SQL语句
                sql = f"UPDATE base SET {', '.join(update_parts)} WHERE id = %s"
                values.append(user_id)

                # 执行更新
                cursor.execute(sql, values)
                connection.commit()
                
                return jsonify({'success': True, 'message': '用户信息更新成功'}), 200
            else:
                return jsonify({'error': '没有提供需要更新的段'}), 400

    except Error as e:
        print(f"Error updating user: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM base WHERE id = %s", (user_id,))
            connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'success': True, 'message': '用户删除成功'}), 200
            else:
                return jsonify({'error': '未找到用户'}), 404
                
    except Error as e:
        print(f"Error deleting user: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

# 添加新的路由来更新用户分数
@app.route('/api/update-high-score', methods=['POST'])
def update_high_score():
    try:
        data = request.get_json()
        username = data.get('username')
        new_score = data.get('high_score')
        
        if not username or new_score is None:
            return jsonify({'error': '缺少必要参数'}), 400
            
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 先获取当前最高分
            cursor.execute("SELECT maxpoint FROM base WHERE name = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                current_high_score = result[0] or 0
                # 只有新分数更高时才更新
                if new_score > current_high_score:
                    cursor.execute(
                        "UPDATE base SET maxpoint = %s WHERE name = %s",
                        (new_score, username)
                    )
                    connection.commit()
                    return jsonify({
                        'success': True,
                        'message': '最高分更新成功',
                        'new_high_score': new_score
                    })
                else:
                    return jsonify({
                        'success': True,
                        'message': '当前分数未超过最高分',
                        'high_score': current_high_score
                    })
            else:
                return jsonify({'error': '用户不存在'}), 404
                
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

# 添加获取用户分数的路由
@app.route('/api/user-score/<username>', methods=['GET'])
def get_user_score(username):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT maxpoint FROM base WHERE name = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                return jsonify({
                    'success': True,
                    'high_score': result[0] or 0
                })
            else:
                return jsonify({'error': '用户不存在'}), 404
                
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

# Add more routes for modifying the base database as needed

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 获取所有有分数的用户，按分数降序排序，限制前10名
            cursor.execute("""
                SELECT name, maxpoint 
                FROM base 
                WHERE maxpoint IS NOT NULL 
                ORDER BY maxpoint DESC 
                LIMIT 10
            """)
            results = cursor.fetchall()
            
            # 将结果转换为列表字典格式
            leaderboard = [
                {
                    'username': row[0],
                    'score': row[1] or 0  # 如果分数为 NULL，则返回0
                }
                for row in results
            ]
            
            return jsonify(leaderboard)
                
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

# 添加新的路由来处理分数更新
@app.route('/api/update-score', methods=['POST'])
def update_score():
    print("收到请求方法:", request.method)
    print("请求头:", request.headers)
    print("请求数据:", request.get_json())
    
    try:
        data = request.get_json()
        username = data.get('username')
        current_score = data.get('score')
        
        print(f"收到更新请求 - 用户: {username}, 分数: {current_score}")
        
        if not username or current_score is None:
            print("缺少必要参数")
            return jsonify({'success': False, 'message': '缺少必要参数'})
        
        # 指定完整的文件路径
        file_path = os.path.join(os.path.dirname(__file__), 'user_point.txt')
        print(f"文件路径: {file_path}")
        
        # 始终写入当前分数，而不是最高分
        try:
            # 确保文件存在
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass
                print("创建新文件")
            
            # 读取现有内容
            lines = []
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"读取到 {len(lines)} 行数据")
            except Exception as read_error:
                print(f"读取文件失败: {read_error}")
            
            # 更新或添加新记录，始终写入当前分数
            user_found = False
            new_lines = []
            for line in lines:
                if line.strip():
                    stored_username, _ = line.strip().split(',')
                    if stored_username == username:
                        new_lines.append(f"{username},{current_score}\n")
                        user_found = True
                        print(f"更新用户记录为当前分数: {current_score}")
                    else:
                        new_lines.append(line)
            
            if not user_found:
                new_lines.append(f"{username},{current_score}\n")
                print(f"添加新用户记录，分数: {current_score}")
            
            # 写入更新后的内容
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"文件写入成功")
            except Exception as write_error:
                print(f"写��文件失败: {write_error}")
            
            # 数据库操作保持不变，仍然只在超过最高分时更新
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT maxpoint FROM base WHERE name = %s", (username,))
                    result = cursor.fetchone()
                    current_high_score = result[0] if result else 0
                    
                    print(f"当前最高分: {current_high_score}")
                    
                    # 只有在超过最高分时才更新数据库
                    if current_score > current_high_score:
                        cursor.execute(
                            "UPDATE base SET maxpoint = %s WHERE name = %s",
                            (current_score, username)
                        )
                        connection.commit()
                        print(f"数据库更新成功，新最高分: {current_score}")
                        return jsonify({
                            'success': True,
                            'message': '分数更新成功',
                            'new_high_score': current_score
                        })
            finally:
                connection.close()
            
            return jsonify({
                'success': True,
                'message': '当前分数已记录',
                'high_score': current_high_score
            })
            
        except Exception as file_error:
            print(f"文件操作失败: {file_error}")
            return jsonify({
                'success': False,
                'message': f'文件操作失败: {str(file_error)}'
            })
            
    except Exception as e:
        print(f"更新分数时出错: {e}")
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 