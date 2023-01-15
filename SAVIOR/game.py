import pygame
import sys
import random
import math
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 30)


pygame.display.set_caption("SAVIOR")
icon = pygame.image.load("static/logo.png")
pygame.display.set_icon(icon)

pygame.mixer.music.load('audio/theme.mp3')
pygame.mixer.music.play(-1)

size = width, height = 800, 600
screen = pygame.display.set_mode((size))

# MESSAGE TO SCREEN
def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color)
    textRect.center = (width / 2), (height / 2 + y_displace)
    screen.blit(textSurf, textRect)


# SPLASH SCREEN
def splash_intro():
    # intro =True
    # while intro:
    screen.fill((0,0,0))
    message_to_screen("WELCOME", "white", 0, "large")
    message_to_screen("Protect planet earth from alien invaders", 'yellow', 40)
    message_to_screen("-"*80, 'white',70)
    message_to_screen("Made by Ankit Jha", 'red',100)
    message_to_screen("CAPS - To fire | ARROW KEYS - To move", 'white', 130)
    pygame.display.update()
    pygame.time.wait(9600)
# BACKGROUND IMAGE
background = pygame.image.load('static/background.jpg')

# PLAYER
player_img = pygame.image.load('static/spaceship.png')
playerX = 380   #default position
playerY = 480   #default position
playerX_change = 0

# ENEMY
enemy_img =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load('static/alien.png'))
    enemyX.append(random.randint(0,800))   #default position
    enemyY.append(random.randint(50,150))   #default position
    enemyX_change.append(2)
    enemyY_change.append(40)

# BULLETS
bullet_img = pygame.image.load('static/bullet.png')
bulletX = 0   #default position # will change in while loop
bulletY = 480   #default position # To start the bullet from tip of spaceship
bulletX_change = 0
bulletY_change = 4 #Speed of bullet
bullet_state = 'ready'  # Ready - bullet will not appear but ready #Fire- Bullet is in action and visible

score = 0

def player(x, y):
    screen.blit(player_img, (x, y)) #blit() takes 2 args image itself and its (x,y) coordinates #blit() is used to draw the image in the given coordinate

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y)) #blit() takes 2 args image itself and its (x,y) coordinates #blit() is used to draw the image in the given coordinate
#enemy_img[i] denote which image we are talking about from the for loop of i in range(num_of_enemy)
def bullet_fire(x, y):
    global bullet_state # TO access the var outside the function
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10)) #To put bullet in the center of spaceship on its nose and prevent overlap
def isCollision(enemyX, enemyY, bulletX, bulletY): 
#Formula for distance between 2 coordinates D = sqrt(sq(x2-x1)-sq(y2-y1))
# When D = 0 , collison happens
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27: #27 pixel a little before hitting enemy
        return True
    else:
        return False


splash_intro()

running = True
while running:

    screen_color = 0,0,0 #(RGB)
    
    screen.fill(screen_color)
    screen.blit(background, (0,0))
    #Closing the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running =False
    #Spaceship movement
    if event.type == pygame.KEYDOWN:    #When key is pressed
        if event.key == pygame.K_LEFT:
            playerX_change = -1
        if event.key == pygame.K_RIGHT:
            playerX_change = 1
        if event.key == pygame.K_CAPSLOCK:
            if bullet_state is "ready":
                # print("fire")
                bulletX = playerX   # To avoid bullet following the spaceship after firing
                bullet_fire(bulletX, bulletY)
    if event.type == pygame.KEYUP:      #When we release the key
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    playerX += playerX_change
    #spaceship restriction in screen
    if playerX <=0:
        playerX = 0
    elif playerX>=736:  #(800-64) because spaceship is 64bit - w=64, h=64
        playerX = 736



    for i in range(num_of_enemy):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=736:  #for acceing the loop above - i denotes anything
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: #if collion is occured
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0,800)   #default position
            enemyY[i] = random.randint(50,150)   #default position
        enemy(enemyX[i], enemyY[i], i)

    
    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
    


    # calling the final function
    player(playerX, playerY)

    pygame.display.update()
