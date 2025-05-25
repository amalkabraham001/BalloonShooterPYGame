import pygame
import sys
import random
import json
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 8
BALLOON_SIZE = 40
BULLET_SIZE = 5
BULLET_SPEED = 10
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
SCORE_FILE = "highscore.json"

# Balloon types
NORMAL_BALLOON = 0
SPECIAL_BALLOON = 1

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Shooter")

# Player properties
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10]

# Bullets
bullets = []

# Balloons - [x, y, speed, color, type, points]
balloons = []

# Available colors for normal balloons
balloon_colors = [RED, BLUE, GREEN, YELLOW, PURPLE]

# Score
score = 0
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Level system
level = 1
score_to_next_level = 100
level_multiplier = 1.5  # Each level increases the required score by this factor

# Level-specific settings
def get_level_settings(current_level):
    return {
        "balloon_speed_min": 1 + (current_level * 0.2),
        "balloon_speed_max": 3 + (current_level * 0.3),
        "spawn_delay": max(10, 60 - (current_level * 5)),  # Faster spawning at higher levels
        "special_balloon_chance": min(0.5, 0.2 + (current_level * 0.05))  # More special balloons at higher levels
    }

level_settings = get_level_settings(level)

# Load high score
def load_high_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0
    return 0

# Save high score
def save_high_score(new_score):
    high_score = max(load_high_score(), new_score)
    with open(SCORE_FILE, 'w') as f:
        json.dump({'high_score': high_score}, f)
    return high_score

high_score = load_high_score()

# Game loop
clock = pygame.time.Clock()
running = True
balloon_spawn_timer = 0

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(score)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet
                bullet_x = player_pos[0] + PLAYER_WIDTH // 2 - BULLET_SIZE // 2
                bullets.append([bullet_x, player_pos[1]])
    
    # Handle player movement with keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - PLAYER_WIDTH:
        player_pos[0] += PLAYER_SPEED
    
    # Update bullets
    for bullet in bullets[:]:
        bullet[1] -= BULLET_SPEED
        if bullet[1] < 0:
            bullets.remove(bullet)
    
    # Check for level up
    if score >= score_to_next_level:
        level += 1
        score_to_next_level = int(score_to_next_level * level_multiplier)
        level_settings = get_level_settings(level)
    
    # Spawn balloons
    balloon_spawn_timer += 1
    if balloon_spawn_timer >= level_settings["spawn_delay"]:
        balloon_spawn_timer = 0
        balloon_x = random.randint(0, SCREEN_WIDTH - BALLOON_SIZE)
        balloon_speed = random.uniform(level_settings["balloon_speed_min"], level_settings["balloon_speed_max"])
        
        # Determine if this is a special balloon
        if random.random() < level_settings["special_balloon_chance"]:
            balloon_type = SPECIAL_BALLOON
            balloon_color = GOLD
            points = 30  # Special balloons are worth more
        else:
            balloon_type = NORMAL_BALLOON
            balloon_color = random.choice(balloon_colors)
            points = 10
            
        balloons.append([balloon_x, 0, balloon_speed, balloon_color, balloon_type, points])
    
    # Update balloons
    for balloon in balloons[:]:
        balloon[1] += balloon[2]
        if balloon[1] > SCREEN_HEIGHT:
            balloons.remove(balloon)
    
    # Check for collisions
    for bullet in bullets[:]:
        for balloon in balloons[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE)
            balloon_rect = pygame.Rect(balloon[0], balloon[1], BALLOON_SIZE, BALLOON_SIZE)
            
            if bullet_rect.colliderect(balloon_rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                if balloon in balloons:
                    score += balloon[5]  # Add points based on balloon type
                    balloons.remove(balloon)
                    if score > high_score:
                        high_score = score
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the player (as a cannon)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))
    pygame.draw.rect(screen, BLACK, (player_pos[0] + PLAYER_WIDTH//2 - 5, player_pos[1] - 15, 10, 20))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], BULLET_SIZE, BULLET_SIZE))
    
    # Draw balloons
    for balloon in balloons:
        balloon_x, balloon_y, _, balloon_color, balloon_type, _ = balloon
        
        # Draw the balloon with its color
        pygame.draw.circle(screen, balloon_color, (int(balloon_x + BALLOON_SIZE//2), int(balloon_y + BALLOON_SIZE//2)), BALLOON_SIZE//2)
        
        # Draw string
        pygame.draw.line(screen, BLACK, (balloon_x + BALLOON_SIZE//2, balloon_y + BALLOON_SIZE), 
                        (balloon_x + BALLOON_SIZE//2, balloon_y + BALLOON_SIZE + 10), 2)
        
        # For special balloons, add a small star or indicator
        if balloon_type == SPECIAL_BALLOON:
            # Draw a small star (simplified as a small circle)
            pygame.draw.circle(screen, WHITE, (int(balloon_x + BALLOON_SIZE//2), int(balloon_y + BALLOON_SIZE//2)), BALLOON_SIZE//4)
    
    # Draw score and level information
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    next_level_text = small_font.render(f"Next level at: {score_to_next_level}", True, BLACK)
    
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    screen.blit(level_text, (10, 90))
    screen.blit(next_level_text, (10, 130))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Save high score before quitting
save_high_score(score)

# Quit Pygame
pygame.quit()
sys.exit()