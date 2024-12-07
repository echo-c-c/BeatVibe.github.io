class ScoreTracker {
    constructor(username) {
        this.username = username;
        this.currentHighScore = 0;
        this.sessionHighScore = 0;
    }

    async initialize() {
        try {
            const response = await fetch(`http://localhost:3000/api/get-high-score/${this.username}`);
            const data = await response.json();
            this.currentHighScore = data.high_score;
            return this.currentHighScore;
        } catch (error) {
            console.error('Error initializing score tracker:', error);
            return 0;
        }
    }

    getCurrentHighScore() {
        return this.currentHighScore;
    }

    updateSessionScore(score) {
        if (score > this.sessionHighScore) {
            this.sessionHighScore = score;
        }
    }

    async updateScore(score) {
        if (score > this.currentHighScore) {
            try {
                const response = await fetch('http://localhost:3000/api/update-score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: this.username,
                        score: score
                    })
                });
                
                const data = await response.json();
                if (data.new_high_score) {
                    this.currentHighScore = data.new_high_score;
                    return true;
                }
                return false;
            } catch (error) {
                console.error('Error updating score:', error);
                return false;
            }
        }
        return false;
    }

    async submitFinalScore() {
        if (this.sessionHighScore > 0) {
            return this.updateScore(this.sessionHighScore);
        }
        return false;
    }
} 