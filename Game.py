import pygame
import random
from pygame import mixer


pygame.init()
#Main screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

##Background music and Image
mixer.music.load("./Sound/background.wav")
mixer.music.play(-1)
backimage = pygame.image.load("./Image/bg.png")

##Player
pimage = pygame.image.load("./Image/space-invaders.png")
px = 300
py = 510
pxchange = 0

def Player(x,y):
    screen.blit(pimage, (x,y))

##Enemy
eimage = [] 
ex = []
ey = []
exchange = []
numberofen = 6

for i in range(6):
    eimage.append(pygame.image.load("./Image/enemy.png"))
    ex.append(random.randint(40, 700))
    ey.append(random.randint(40, 100))
    exchange.append(2.5)

def Enemy(x,y, i):
    screen.blit(eimage[i], (x,y))

def Collision(ex,ey,bx,by):
    x = abs(ex - bx)
    y = abs(ey - by)
    if y < 16 and x < 16:
        return True
    else:
        return False

##Bullot
bulletImg = pygame.image.load("./Image/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

##Game info 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

life = 1
lifex = 660
lifey = 10

def show_life(x, y):
    LIFE = font.render("Life : " + str(life), True, (255, 255, 255))
    screen.blit(LIFE, (x, y))

game_over_font = pygame.font.Font('freesansbold.ttf', 65)
def game_over_text():
    over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))




play = True
while play:
    screen.blit(backimage, (0,0))    
    if life == 0:
        game_over_text()
        mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mixer.music.play(-1)
                    life = 3
                    eimage = [] 
                    ex = []
                    ey = []
                    exchange = []
                    numberofen = 6
                    score_value = 0
                    for i in range(6):
                        eimage.append(pygame.image.load("./Image/enemy.png"))
                        ex.append(random.randint(40, 700))
                        ey.append(random.randint(40, 100))
                        exchange.append(2.5)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pxchange = -3.5
                if event.key == pygame.K_RIGHT:
                    pxchange = 3.5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("./Sound/laser.wav")
                        bulletSound.play()
                        bulletX = px
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pxchange = 0
                if event.key == pygame.K_RIGHT:
                    pxchange = 0
        

        if px < 0:
            px = 0

        if px > 736:
            px = 736
        
        for i in range(numberofen):
            
            if ex[i] < 0:
                exchange[i] = 3
                ey[i] += 50
            if ex[i] > 736:
                exchange[i] = -3
                ey[i] += 50

            if ey[i] > py:
                ey[i] = random.randint(40, 100)
                life -= 1

            ex[i] += exchange[i]

            collide = Collision(ex[i], ey[i], bulletX, bulletY)
            if collide:
                score_value += 1
                ex[i] = random.randint(40, 700)
                ey[i] = random.randint(40, 100)
                bulletY = 480
                bullet_state = "ready"
                CollSound = mixer.Sound("./Sound/explosion.wav")
                CollSound.play()

            Enemy(ex[i], ey[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        
        px += pxchange

        Player(px,py)
        show_score(textX, testY)
        show_life(lifex, lifey)
    pygame.display.update()