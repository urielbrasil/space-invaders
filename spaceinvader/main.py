import pygame
import random
import math
import time
from pygame import mixer

import matplotlib.pyplot

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

"""
# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

"""

# Title and Icon
pygame.display.set_caption("Space Invaders")

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemy_bulletImg = []
enemy_bulletX = []
enemy_bulletY = []
enemy_bulletX_change = []
enemy_bulletY_change = []
enemy_bullet_state = []

enemy_bullet_distance = []


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

    enemy_bulletImg.append(pygame.image.load("enemy_bullet.png"))
    enemy_bulletX.append(0)
    enemy_bulletY.append(0)
    enemy_bulletX_change.append(3)
    enemy_bulletY_change.append(2)
    enemy_bullet_state.append("ready")

    enemy_bullet_distance.append(0.1)

# Explosion
explosionImg = pygame.image.load("explosion.png")
explosionX = 0
explosionY = 0

# Bullet
# Ready -  You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Level
level_value = 1
level_change = 0
level_font = pygame.font.Font("freesansbold.ttf", 32)
levelX = 300
levelY = 10
level_up = False

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def show_level(x, y):
    level = level_font.render("LEVEL: " + str(level_value), True, (0, 0, 0))
    screen.blit(level, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit basically means draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit basically means draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def enemy_fire_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bullet_state[i] = "fire"
    screen.blit(enemy_bulletImg[i], (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def is_player_collision(enemyX, enemyY, playerX, playerY):
    distance_player = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance_player < 50:
        return True
    else:
        return False


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


def game_over():
    explosion_sound = mixer.Sound("explosion.wav")
    explosion_sound.play()
    explosion(playerX, playerY)
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # If Keystroke is pressed check whether its right, left, top or down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_UP:
                playerY_change -= 5
            if event.key == pygame.K_DOWN:
                playerY_change += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_LEFT or \
                    event.key == pygame.K_UP or \
                    event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Player Collision
        player_collision = is_player_collision(enemyX[i], enemyY[i], playerX, playerY)
        if player_collision:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        # Enemy Bullet Collision

        enemy_bullet_distance[i] = math.sqrt((math.pow(enemy_bulletX[i] - playerX, 2)) + (math.pow(enemy_bulletY[i] - playerY, 2)))
        if enemy_bullet_distance[i] < 27:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        # Enemy Boundary
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 1
            bullet_state = "ready"
            score_value += 10
            level_change += 10
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            explosion(enemyX[i], enemyY[i])
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Increasing Level and Difficulty on Enemy
        if level_change >= 50:
            level_up = True
            level_value += 1
            level_change = 0

        if level_up:
            enemy_bulletY_change[i] += 1
            level_up = False

        enemy(enemyX[i], enemyY[i], i)


        # Enemy Bullet
        if enemy_bullet_state[i] == "ready":
            enemy_bulletX[i] = enemyX[i]
            enemy_bulletY[i] = enemyY[i]
            enemy_fire_bullet(enemy_bulletX[i], enemy_bulletY[i], i)

        if enemy_bulletY[i] >= 600:
            enemy_bullet_state[i] = "ready"

        if enemy_bullet_state[i] == "fire":
            enemy_fire_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
            enemy_bulletY[i] += enemy_bulletY_change[i]
            # Enemy Bullet
            if enemy_bullet_state[i] == "ready":
                enemy_bulletX[i] = enemyX[i]
                enemy_bulletY[i] = enemyY[i]
                enemy_fire_bullet(enemy_bulletX[i], enemy_bulletY[i], i)

            if enemy_bulletY[i] >= 600:
                enemy_bullet_state[i] = "ready"

            if enemy_bullet_state[i] == "fire":
                enemy_fire_bullet(enemy_bulletX[i], enemy_bulletY[i], i)
                enemy_bulletY[i] += enemy_bulletY_change[i]

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Creating boundaries to X - Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Creating boundaries to Y - Player
    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    player(playerX, playerY)
    show_score(textX, textY)
    show_level(levelX, levelY)
    pygame.display.update()
