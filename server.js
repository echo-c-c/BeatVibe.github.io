const express = require('express');
const fs = require('fs');
const app = express();
const cors = require('cors');

app.use(cors());
app.use(express.text());

const SCORE_FILE = 'user_point.txt';

// 确保文件存在
if (!fs.existsSync(SCORE_FILE)) {
    fs.writeFileSync(SCORE_FILE, '', 'utf8');
}

// 处理读取分数文件的请求
app.get('/user_point.txt', (req, res) => {
    try {
        const data = fs.readFileSync(SCORE_FILE, 'utf8');
        res.send(data);
    } catch (error) {
        console.error('Error reading file:', error);
        res.status(500).send('Error reading score file');
    }
});

// 处理更新分数的请求
app.post('/update-score', (req, res) => {
    try {
        // 直接将请求体写入文件
        fs.writeFileSync(SCORE_FILE, req.body, 'utf8');
        console.log('Score updated:', req.body);
        res.send('Score updated successfully');
    } catch (error) {
        console.error('Error writing file:', error);
        res.status(500).send('Error updating score');
    }
});

// 启动服务器
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});