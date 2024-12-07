let score = 0;
let isPlaying = false;
const hitButton = document.getElementById('hitButton');
const startButton = document.getElementById('startButton');
const gameArea = document.getElementById('gameArea');
const bgMusic = document.getElementById('bgMusic');
const scoreDisplay = document.getElementById('score');

// 节奏点的时间（毫秒）
const beatTimes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000];
let currentBeatIndex = 0;

startButton.addEventListener('click', () => {
    if (!isPlaying) {
        startGame();
    }
});

hitButton.addEventListener('click', () => {
    if (isPlaying) {
        checkHit();
    }
});

function startGame() {
    isPlaying = true;
    score = 0;
    currentBeatIndex = 0;
    scoreDisplay.textContent = `得分: ${score}`;
    startButton.style.display = 'none';
    gameArea.style.display = 'block';
    
    bgMusic.currentTime = 0;
    bgMusic.play();
    
    scheduleBeat();
}

function scheduleBeat() {
    if (currentBeatIndex < beatTimes.length) {
        setTimeout(() => {
            hitButton.classList.add('hit');
            setTimeout(() => {
                hitButton.classList.remove('hit');
            }, 200);
            currentBeatIndex++;
            scheduleBeat();
        }, beatTimes[currentBeatIndex]);
    } else {
        endGame();
    }
}

function checkHit() {
    const currentTime = bgMusic.currentTime * 1000;
    const expectedTime = beatTimes[currentBeatIndex - 1];
    const timeDiff = Math.abs(currentTime - expectedTime);
    
    if (timeDiff < 300) { // 允许300毫秒的误差
        score += 100;
        hitButton.classList.add('hit');
    } else {
        score -= 50;
        hitButton.classList.add('miss');
    }
    
    scoreDisplay.textContent = `得分: ${score}`;
    
    setTimeout(() => {
        hitButton.classList.remove('hit');
        hitButton.classList.remove('miss');
    }, 100);
}

function endGame() {
    isPlaying = false;
    gameArea.style.display = 'none';
    startButton.style.display = 'block';
    alert(`游戏结束！最终得分：${score}`);
} 