import pygame
import random

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('spaceBack.png')

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo1.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship 1.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 3
enemyY_change = 40

# laser

# ready - you can't see the laser on the screen
# fire - the laser is currently moving

laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


# game loop
running = True
while running:

    # RGB - red, green, blue
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = - 4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    # get the current x coordinate of the spaceship
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5.4 = 5 - 0.1
    # 5 = 5 + 0.1

    # checking boundaries of spaceship, so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -3
        enemyY += enemyY_change

    # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
