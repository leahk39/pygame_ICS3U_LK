import pygame

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo1.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('spaceship 1.png')
playerX = 370
playerY = 480

def player(x,y):
    screen.blit(playerImg, (x, y))

# game loop
running = True
while running:

    # RGB - red, green, blue
    screen.fill((0,0,0))
    playerY -=0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(playerX,playerY)
    pygame.display.update()