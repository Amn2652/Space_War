import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
backgroundImage = pygame.image.load('Background.jpg')
background = pygame.transform.scale(backgroundImage, (800, 600))

background_music = mixer.music.load('background_music.mp3')
mixer.music.play(-1)
# Set the title and icon
pygame.display.set_caption("Traffic Control")
icon = pygame.image.load('traffic-light.png')
pygame.display.set_icon(icon)

# Load and resize the bullet image
bulletImage = pygame.image.load('bullet.png')
bullet = pygame.transform.scale(bulletImage, (32, 32))

# Load and resize the player image
loadedPlayer = pygame.image.load('spaceship.png')
player = pygame.transform.scale(loadedPlayer, (64, 64))
playerX = 370
playerY = 480

# Load and resize the enemy image
loadedEnemy = pygame.image.load('monster.png')
enemy = pygame.transform.scale(loadedEnemy, (32, 32))
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)

# Bullet variables
bulletX = 0
bulletY = 480
bullet_state = "ready"
bulletY_change = 5

# Movement variables
playerX_Change = 0
enemyX_Change = 0.3  # Set the initial speed of the enemy
enemyY_Change = 32

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX =10
textY =10
over_font = pygame.font.Font('freesansbold.ttf',64)


# Function to draw the player
def playerfn(x, y):
    screen.blit(player, (x, y))

# Function to draw the enemy
def Enemyfn(x, y):
    screen.blit(enemy, (x, y))

# Function to fire the bullet
def fire_Bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))

def Collision(x1,y1,x2,y2):
    Collision = math.sqrt((math.pow(x1-x2,2)) + math.pow(y1-y2,2))
    if Collision <27:
        return True
    else:
        return False

def Display_Score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255),None)
    screen.blit(score,(x,y))
    
def display_gameover():
    gameover = over_font.render("Game Over",True,(255,255,255),None)
    screen.blit(gameover,(200,250))
# Main game loop
run = True
while run:
    screen.fill((0, 255, 0))
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('fire.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_Bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
    
    # Update player position
    playerX += playerX_Change

    # Boundary check for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64 = 736
        playerX = 736

    # Update enemy position
    enemyX += enemyX_Change
    
    # Boundary check for enemy
    if enemyX <= 0:
        enemyX_Change = 0.3
        enemyY += enemyY_Change
    elif enemyX >= 768:  # 800 - 32 = 768
        enemyX_Change = -0.3
        enemyY += enemyY_Change

    if enemyY > 200:
        enemyY =2000
        display_gameover()
        #break

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state == "fire":
        fire_Bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # Draw the player and enemy
    playerfn(playerX, playerY)
    Enemyfn(enemyX, enemyY)
    Display_Score(textX,textY)

    collision = Collision(enemyX,enemyY,bulletX,bulletY)
    if collision:
        collision_sound = mixer.Sound('blast.wav')
        collision_sound.play()
        bulletY = 480
        bullet_state= "ready"
        score_value +=1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
