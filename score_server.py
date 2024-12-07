from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # 启用CORS以允许前端访问

# 数据库配置
DB_PATH = 'game.db'

def init_db():
    """初始化数据库"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # 创建用户分数表
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_scores (
                username TEXT PRIMARY KEY,
                high_score INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/api/update-score', methods=['POST'])
def update_score():
    """更新用户分数"""
    data = request.json
    username = data.get('username')
    new_score = data.get('score')
    
    if not username or new_score is None:
        return jsonify({'error': '缺少必要参数'}), 400
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # 获取当前最高分
        c.execute('SELECT high_score FROM user_scores WHERE username = ?', (username,))
        result = c.fetchone()
        
        if result:
            current_high_score = result[0]
            # 只有新分数更高时才更新
            if new_score > current_high_score:
                c.execute('UPDATE user_scores SET high_score = ? WHERE username = ?',
                         (new_score, username))
                conn.commit()
                return jsonify({'message': '分数已更新', 'new_high_score': new_score})
            return jsonify({'message': '当前分数未超过最高分', 'high_score': current_high_score})
        else:
            # 新用户，插入记录
            c.execute('INSERT INTO user_scores (username, high_score) VALUES (?, ?)',
                     (username, new_score))
            conn.commit()
            return jsonify({'message': '新用户分数已记录', 'high_score': new_score})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/get-high-score/<username>', methods=['GET'])
def get_high_score(username):
    """获取用户最高分"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT high_score FROM user_scores WHERE username = ?', (username,))
        result = c.fetchone()
        
        if result:
            return jsonify({'high_score': result[0]})
        return jsonify({'high_score': 0})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取排行榜"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT username, high_score FROM user_scores ORDER BY high_score DESC LIMIT 10')
        results = c.fetchall()
        
        leaderboard = [{'username': row[0], 'high_score': row[1]} for row in results]
        return jsonify(leaderboard)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(port=3000) 