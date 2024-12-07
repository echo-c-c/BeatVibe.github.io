# 节奏律动 (BeatVibe)

一个基于Web的音乐节奏游戏，玩家可以随着音乐节奏点击音符，获得分数并与其他玩家竞争排名。

## 功能特点

- 用户系统
  - 用户注册和登录
  - 个人最高分记录
  - 排行榜系统
  - 管理员后台管理

- 游戏特性
  - 多首预设音乐曲目
  - 实时音频分析和音符生成
  - 精确的判定系统（Perfect/Great/Good/Miss）
  - 连击计数系统
  - 实时分数统计
  - 暂停/继续功能
  - 进度条显示

- 创意工坊
  - 支持自定义音乐上传
  - 自定义背景图片
  - 难度设置

## 技术栈

### 前端
- HTML5
- CSS3
- JavaScript
- Web Audio API
- Canvas动画

### 后端
- Python
- Flask框架
- MySQL数据库
- RESTful API

## 安装说明

1. 克隆项目到本地：

```bash
git clone [项目地址]
```

2. 安装所需的Python包：

```bash
pip install flask
pip install flask-cors
pip install mysql-connector-python
```

3. 配置MySQL数据库：

```sql
CREATE DATABASE demo;
USE demo;

CREATE TABLE base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    time DATETIME,
    users VARCHAR(255),
    maxpoint INT
);

CREATE TABLE root (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

4. 配置数据库连接：
   - 打开 `app.py`
   - 修改数据库连接参数：

```python
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='demo'
    )
```

## 运行说明

1. 启动Flask服务器：

```bash
python app.py
```

2. 访问游戏：
   - 打开浏览器访问：`http://127.0.0.1:5000`
   - 登录或注册新账号
   - 开始游戏！

## 游戏操作

- **空格键**: 点击音符
- **ESC键**: 暂停游戏
- **左右方向键**: 切换音乐选择
- **点击判定线**: 击打音符

## 评分系统

- Perfect: +100分
- Great: +80分
- Good: +50分
- Miss: -50分

## 项目结构
```
rhythm-game/
├── app.py                # Flask后端服务
├── user_point.txt        # 用户分数记录
├── templates/
│   ├── login.html       # 登录页面
│   ├── admin.html       # 管理员界面
│   └── success.html     # 成功页面
├── static/
│   ├── music/          # 音乐文件
│   │   ├── Memories.mp3
│   │   ├── FallingDown.mp3
│   │   └── ...
│   └── images/         # 图片资源
└── index.html           # 游戏主页面
```

## 管理员功能

1. 访问管理员面板：
   - 使用管理员账号登录
   - 查看用户统计信息
   - 管理用户数据
   - 删除用户账号

2. 管理员账号创建：

```sql
INSERT INTO root (name, password) VALUES ('admin', 'your_admin_password');
```

## 开发说明

### 添加新音乐

1. 将音乐文件(.mp3)放入 `static/music` 目录
2. 在 `index.html` 中添加音乐选项：

```html
<div class="music-option" data-music="your_music.mp3">
    <div class="music-preview" style="background-image: url('your_image.jpg')"></div>
    <div class="music-option-title">音乐标题</div>
    <div class="music-option-details">
        <div>时长: mm:ss</div>
        <div class="music-difficulty">
            难度: <span class="difficulty-star">★★★</span>
        </div>
    </div>
</div>
```

### API 接口

- POST `/login`: 用户登录
- POST `/register`: 用户注册
- GET `/leaderboard`: 获取排行榜
- POST `/api/update-score`: 更新用户分数
- GET `/api/user-score/<username>`: 获取用户分数

## 常见问题解决

1. 数据库连接失败
   - 检查MySQL服务是否运行
   - 验证数据库连接参数是否正确
   - 确保数据库用户有适当的权限

2. 音频无法播放
   - 确保音频文件格式为MP3
   - 检查浏览器是否允许音频自动播放
   - 验证音频文件路径是否正确

3. 分数未能保存
   - 检查数据库连接
   - 确保用户已登录
   - 验证user_point.txt文件权限

## 更新日志

### v1.0.0 (2024-03)
- 初始版本发布
- 实现基本游戏功能
- 添加用户系统和排行榜
- 创意工坊功能

## 许可证

MIT License

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件至 [2012997697@qq.com]

## 致谢

感谢所有为项目做出贡献的开发者和提供音乐资源的艺术家们。
```

</rewritten_file>
