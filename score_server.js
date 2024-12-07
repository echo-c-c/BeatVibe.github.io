const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();

// 启用 CORS 和请求体解析
app.use(cors());
app.use(express.text());

const SCORE_FILE = 'user_point.txt';

// 确保文件存在
if (!fs.existsSync(SCORE_FILE)) {
    fs.writeFileSync(SCORE_FILE, '', 'utf8');
}

// 获取分数记录
app.get('/user_point.txt', (req, res) => {
    try {
        const data = fs.readFileSync(SCORE_FILE, 'utf8');
        res.send(data);
    } catch (error) {
        console.error('读取文件错误:', error);
        res.status(500).send('读取分数文件失败');
    }
});

// 更新分数记录
app.post('/update-score', (req, res) => {
    try {
        fs.writeFileSync(SCORE_FILE, req.body, 'utf8');
        console.log('更新分数:', req.body);
        res.send('分数更新成功');
    } catch (error) {
        console.error('写入文件错误:', error);
        res.status(500).send('更新分数失败');
    }
});

// 启动服务器
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`分数记录服务器运行在端口 ${PORT}`);
});