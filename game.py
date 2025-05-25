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
BALLOON_SPEED_MIN = 1
BALLOON_SPEED_MAX = 3
BULLET_SIZE = 5
BULLET_SPEED = 10
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SCORE_FILE = "highscore.json"

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Shooter")

# Player properties
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10]

# Bullets
bullets = []

# Balloons
balloons = []
balloon_spawn_timer = 0
balloon_spawn_delay = 60  # frames

# Score
score = 0
font = pygame.font.SysFont(None, 36)

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
    
    # Spawn balloons
    balloon_spawn_timer += 1
    if balloon_spawn_timer >= balloon_spawn_delay:
        balloon_spawn_timer = 0
        balloon_x = random.randint(0, SCREEN_WIDTH - BALLOON_SIZE)
        balloon_speed = random.uniform(BALLOON_SPEED_MIN, BALLOON_SPEED_MAX)
        balloons.append([balloon_x, 0, balloon_speed])
    
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
                    balloons.remove(balloon)
                score += 10
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
        pygame.draw.circle(screen, RED, (int(balloon[0] + BALLOON_SIZE//2), int(balloon[1] + BALLOON_SIZE//2)), BALLOON_SIZE//2)
        pygame.draw.line(screen, BLACK, (balloon[0] + BALLOON_SIZE//2, balloon[1] + BALLOON_SIZE), 
                        (balloon[0] + BALLOON_SIZE//2, balloon[1] + BALLOON_SIZE + 10), 2)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Save high score before quitting
save_high_score(score)

# Quit Pygame
pygame.quit()
sys.exit()