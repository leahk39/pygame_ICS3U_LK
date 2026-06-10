import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('spaceBack.png')

# background sound
mixer.music.load('backgroundMusic.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo1.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship 1.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 2
enemy_alive = [True for i in range(num_of_enemies)]
enemy_alive = [True, True, True, True, True, True]
print(enemy_alive)



for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# final boss
finalBoss = pygame.image.load('finalBoss.png')
finalBossX = 370
finalBossY = 50
playerX_change = 0

# lives
lives_num = 3

life1Img = pygame.image.load('lives.png')
life1X = 735
life1Y = 30
life2Img = pygame.image.load('lives.png')
life2X = 695
life2Y = 30
life3Img = pygame.image.load('lives.png')
life3X = 655
life3Y = 30


# laser

# ready - you can't see the laser on the screen
# fire - the laser is currently moving

laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"

explosion_sound = mixer.Sound('explode.mp3')

# font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (204, 204, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (204, 204, 255))
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def life1(x, y):
    screen.blit(life1Img, (x, y))

def life2(x, y):
    screen.blit(life2Img, (x, y))

def life3(x, y):
    screen.blit(life3Img, (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,laserX,laserY):
    distance = math.sqrt((math.pow(enemyX-laserX,2)) + (math.pow(enemyY-laserY,2)))
    if distance < 27:
        return True
    else:
        return False

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
                    laser_sound = mixer.Sound('laserShoot.mp3')
                    laser_sound.play()
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
    for i in range(num_of_enemies):
        # lives in game

        if enemyY[i] > 440:
            lives_num -= 1
            print("life lost")
            # enemyX[i] = random.randint(0, 735)
            # enemyY[i] = random.randint(50, 150)

            # game over
            if lives_num <= 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        if enemy_alive[i] == True:
            enemy(enemyX[i], enemyY[i], i)

        # collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if enemy_alive[i] == True and collision:
            print(f"hit{i}")

            explosion_sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            enemy_alive[i] = False
            if num_of_enemies > 0:
                num_of_enemies -= 1
                print(f"one enemy removed, so {num_of_enemies}")
                break

            # enemyX[i] = random.randint(0, 735)
            # enemyY[i] = random.randint(50, 150)




    # laser movement
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)

    # lost lives
    if lives_num >= 1:
        life1(life1X, life1Y)

    if lives_num >= 2:
        life2(life2X, life2Y)

    if lives_num >= 3:
        life3(life3X, life3Y)

    show_score(textX, textY)
    pygame.display.update()



