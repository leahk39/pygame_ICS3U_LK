import pygame
import math
import random
from pygame import mixer
import os

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# background
background = pygame.image.load(os.path.join(BASE_DIR, "spaceBack.png"))

# background sound
mixer.music.load(os.path.join(BASE_DIR, 'backgroundMusic.mp3'))
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.path.join(BASE_DIR, 'ufo1.png'))
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(os.path.join(BASE_DIR, 'spaceship 1.png'))
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
NUM_ENEMIES_MAX = 6
num_enemies_alive = NUM_ENEMIES_MAX
enemy_alive = [True for i in range(NUM_ENEMIES_MAX)]
enemy_alive = [True, True, True, True, True, True]
print(enemy_alive)



for i in range(NUM_ENEMIES_MAX):
    enemyImg.append(pygame.image.load(os.path.join(BASE_DIR, 'enemy.png')))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# final boss
finalBossImg = pygame.image.load(os.path.join(BASE_DIR, 'finalBoss.png'))

finalBossX = 333
finalBossY = -150      # start off-screen
finalBossY_change = 0.3

boss_active = False
boss_hp = 11
boss_alive = True

# lives
lives_num = 3

life1Img = pygame.image.load(os.path.join(BASE_DIR, 'lives.png'))
life1X = 735
life1Y = 30
life2Img = pygame.image.load(os.path.join(BASE_DIR, 'lives.png'))
life2X = 695
life2Y = 30
life3Img = pygame.image.load(os.path.join(BASE_DIR, 'lives.png'))
life3X = 655
life3Y = 30


# laser

# ready - you can't see the laser on the screen
# fire - the laser is currently moving

laserImg = pygame.image.load(os.path.join(BASE_DIR, 'laser.png'))
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"

explosion_sound = mixer.Sound(os.path.join(BASE_DIR, 'explode.mp3'))

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


def blit_enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def finalBoss(x, y):
    screen.blit(finalBossImg, (x, y))

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

def bossCollision(bossX, bossY, laserX, laserY):
    distance = math.sqrt((bossX - laserX)**2 + (bossY - laserY)**2)
    return distance < 60


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
                    laser_sound = mixer.Sound(os.path.join(BASE_DIR, 'laserShoot.mp3'))
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
    for i in range(NUM_ENEMIES_MAX):
        # lives in game

        if enemy_alive[i] == True:
            if enemyY[i] > 440:
                lives_num -= 1
                print("life lost")

            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            if enemy_alive[i] == True:
                blit_enemy(enemyX[i], enemyY[i], i)

            # collision
            collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
            if enemy_alive[i] == True and collision == True:
                print(f"hit{i}")

                explosion_sound.play()
                laserY = 480
                laser_state = "ready"
                score_value += 1
                enemy_alive[i] = False
                if num_enemies_alive > 0:
                    num_enemies_alive -= 1
                    print(f"one enemy removed, so {num_enemies_alive}")
                    break


    if num_enemies_alive == 0 and not boss_active and boss_alive:
        boss_active = True

    if boss_active and boss_alive:
        finalBossY += finalBossY_change

        finalBoss(finalBossX, finalBossY)

    if boss_active and boss_alive:
        if finalBossY < 50:
            finalBossY += finalBossY_change

        finalBoss(finalBossX, finalBossY)

    if boss_active and boss_alive:
        collision = bossCollision(finalBossX, finalBossY, laserX, laserY)
        print(finalBossImg.get_width(), finalBossImg.get_height())
        print("collision =", collision)

        if collision and laser_state == "fire":
            explosion_sound.play()

            laserY = 480
            laser_state = "ready"

            boss_hp -= 1

            print("Boss HP:", boss_hp)

            if boss_hp <= 0:
                boss_alive = False
                boss_active = False
                score_value += 10  # optional bonus points


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

    if boss_active and boss_alive:
        hp_text = font.render("Boss HP: " + str(boss_hp), True, (204, 204, 255))
        screen.blit(hp_text, (300, 10))

    # game over
    if lives_num <= 0 or boss_alive == False:
        for j in range(NUM_ENEMIES_MAX):
            enemyY[j] = 2000
        game_over_text()

    pygame.display.update()