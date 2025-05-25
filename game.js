// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Constants
const SCREEN_WIDTH = 800;
const SCREEN_HEIGHT = 600;
const PLAYER_WIDTH = 50;
const PLAYER_HEIGHT = 30;
const PLAYER_SPEED = 8;
const BALLOON_SIZE = 40;
const BULLET_SIZE = 5;
const BULLET_SPEED = 10;

// Colors
const BLACK = '#000000';
const RED = '#FF0000';
const BLUE = '#0000FF';
const GREEN = '#00FF00';
const YELLOW = '#FFFF00';
const PURPLE = '#800080';
const GOLD = '#FFD700';
const WHITE = '#FFFFFF';

// Balloon types
const NORMAL_BALLOON = 0;
const SPECIAL_BALLOON = 1;

// Game state
let player = {
    x: SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2,
    y: SCREEN_HEIGHT - PLAYER_HEIGHT - 10
};

let bullets = [];
let balloons = [];
let score = 0;
let highScore = localStorage.getItem('highScore') ? parseInt(localStorage.getItem('highScore')) : 0;
let level = 1;
let scoreToNextLevel = 100;
let levelMultiplier = 1.5;
let balloonSpawnTimer = 0;

// Available colors for normal balloons
const balloonColors = [RED, BLUE, GREEN, YELLOW, PURPLE];

// Key states
const keys = {
    ArrowLeft: false,
    ArrowRight: false,
    Space: false
};

// Level-specific settings
function getLevelSettings(currentLevel) {
    return {
        balloonSpeedMin: 1 + (currentLevel * 0.2),
        balloonSpeedMax: 3 + (currentLevel * 0.3),
        spawnDelay: Math.max(10, 60 - (currentLevel * 5)),
        specialBalloonChance: Math.min(0.5, 0.2 + (currentLevel * 0.05))
    };
}

let levelSettings = getLevelSettings(level);

// Event listeners for keyboard
window.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') keys.ArrowLeft = true;
    if (e.code === 'ArrowRight') keys.ArrowRight = true;
    if (e.code === 'Space') keys.Space = true;
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') keys.ArrowLeft = false;
    if (e.code === 'ArrowRight') keys.ArrowRight = false;
    if (e.code === 'Space') keys.Space = false;
});

// Save high score
function saveHighScore(newScore) {
    if (newScore > highScore) {
        highScore = newScore;
        localStorage.setItem('highScore', highScore);
    }
}

// Update game elements
function update() {
    // Handle player movement
    if (keys.ArrowLeft && player.x > 0) {
        player.x -= PLAYER_SPEED;
    }
    if (keys.ArrowRight && player.x < SCREEN_WIDTH - PLAYER_WIDTH) {
        player.x += PLAYER_SPEED;
    }
    
    // Shoot bullets
    if (keys.Space) {
        // Limit firing rate
        if (frameCount % 10 === 0) {
            const bulletX = player.x + PLAYER_WIDTH / 2 - BULLET_SIZE / 2;
            bullets.push({ x: bulletX, y: player.y });
        }
    }
    
    // Update bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        bullets[i].y -= BULLET_SPEED;
        if (bullets[i].y < 0) {
            bullets.splice(i, 1);
        }
    }
    
    // Check for level up
    if (score >= scoreToNextLevel) {
        level++;
        scoreToNextLevel = Math.floor(scoreToNextLevel * levelMultiplier);
        levelSettings = getLevelSettings(level);
        
        // Update UI
        document.getElementById('level').textContent = `Level: ${level}`;
        document.getElementById('nextLevel').textContent = `Next level at: ${scoreToNextLevel}`;
    }
    
    // Spawn balloons
    balloonSpawnTimer++;
    if (balloonSpawnTimer >= levelSettings.spawnDelay) {
        balloonSpawnTimer = 0;
        const balloonX = Math.random() * (SCREEN_WIDTH - BALLOON_SIZE);
        const balloonSpeed = levelSettings.balloonSpeedMin + 
                            Math.random() * (levelSettings.balloonSpeedMax - levelSettings.balloonSpeedMin);
        
        // Determine if this is a special balloon
        let balloonType, balloonColor, points;
        if (Math.random() < levelSettings.specialBalloonChance) {
            balloonType = SPECIAL_BALLOON;
            balloonColor = GOLD;
            points = 30;
        } else {
            balloonType = NORMAL_BALLOON;
            balloonColor = balloonColors[Math.floor(Math.random() * balloonColors.length)];
            points = 10;
        }
        
        balloons.push({
            x: balloonX,
            y: 0,
            speed: balloonSpeed,
            color: balloonColor,
            type: balloonType,
            points: points
        });
    }
    
    // Update balloons
    for (let i = balloons.length - 1; i >= 0; i--) {
        balloons[i].y += balloons[i].speed;
        if (balloons[i].y > SCREEN_HEIGHT) {
            balloons.splice(i, 1);
        }
    }
    
    // Check for collisions
    for (let i = bullets.length - 1; i >= 0; i--) {
        for (let j = balloons.length - 1; j >= 0; j--) {
            const bullet = bullets[i];
            const balloon = balloons[j];
            
            if (!bullet || !balloon) continue;
            
            const bulletRect = {
                x: bullet.x,
                y: bullet.y,
                width: BULLET_SIZE,
                height: BULLET_SIZE
            };
            
            const balloonRect = {
                x: balloon.x,
                y: balloon.y,
                width: BALLOON_SIZE,
                height: BALLOON_SIZE
            };
            
            if (checkCollision(bulletRect, balloonRect)) {
                score += balloon.points;
                saveHighScore(score);
                
                // Update UI
                document.getElementById('score').textContent = `Score: ${score}`;
                document.getElementById('highScore').textContent = `High Score: ${highScore}`;
                
                bullets.splice(i, 1);
                balloons.splice(j, 1);
                break;
            }
        }
    }
}

// Check collision between two rectangles
function checkCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

// Draw game elements
function draw() {
    // Clear the canvas
    ctx.fillStyle = WHITE;
    ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    
    // Draw player (cannon)
    ctx.fillStyle = BLACK;
    ctx.fillRect(player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT);
    ctx.fillRect(player.x + PLAYER_WIDTH/2 - 5, player.y - 15, 10, 20);
    
    // Draw bullets
    ctx.fillStyle = BLACK;
    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, BULLET_SIZE, BULLET_SIZE);
    });
    
    // Draw balloons
    balloons.forEach(balloon => {
        // Draw the balloon with its color
        ctx.fillStyle = balloon.color;
        ctx.beginPath();
        ctx.arc(balloon.x + BALLOON_SIZE/2, balloon.y + BALLOON_SIZE/2, BALLOON_SIZE/2, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw string
        ctx.strokeStyle = BLACK;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(balloon.x + BALLOON_SIZE/2, balloon.y + BALLOON_SIZE);
        ctx.lineTo(balloon.x + BALLOON_SIZE/2, balloon.y + BALLOON_SIZE + 10);
        ctx.stroke();
        
        // For special balloons, add a small indicator
        if (balloon.type === SPECIAL_BALLOON) {
            ctx.fillStyle = WHITE;
            ctx.beginPath();
            ctx.arc(balloon.x + BALLOON_SIZE/2, balloon.y + BALLOON_SIZE/2, BALLOON_SIZE/4, 0, Math.PI * 2);
            ctx.fill();
        }
    });
}

// Game loop
let frameCount = 0;
function gameLoop() {
    frameCount++;
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Initialize game
document.getElementById('score').textContent = `Score: ${score}`;
document.getElementById('highScore').textContent = `High Score: ${highScore}`;
document.getElementById('level').textContent = `Level: ${level}`;
document.getElementById('nextLevel').textContent = `Next level at: ${scoreToNextLevel}`;

// Start the game
gameLoop();