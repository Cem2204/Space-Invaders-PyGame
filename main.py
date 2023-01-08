import pygame
import random
import math
from pygame import mixer


clock = pygame.time.Clock()
countdown = 60
countX = 530
countY = 10
last_count = pygame.time.get_ticks()
game = True

# pygame açılış
pygame.init()

# Başlık ve ikon
pygame.display.set_caption("Cem'in İlk Python Oyunu")
icon = pygame.image.load("game-console-2.png")
pygame.display.set_icon(icon)

# ekranı oluşturma
screen = pygame.display.set_mode((800, 600))

# arkaplan
background = pygame.image.load("backgroung.jpg")

# arkaplan müzik
mixer.music.load("backMusic.wav")
mixer.music.play(-1)

# kapama için oluşturduğumuz değişken - skor - bitiş
running = True
score = 0
font = pygame.font.Font("SugarSnow.ttf", 32)
textX = 10
testY = 10
over_font = pygame.font.Font("SugarSnow.ttf",64)
overX = 320
overY = 275

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(1)

# Bullet
bulletImg = pygame.image.load("bullets.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 9
bullet_state = "ready"

def gameOverText(x,y):
    over_text = font.render("GAME OVER" , True, (0,0,0))
    screen.blit(over_text , (x,y))
    scorev = font.render("Your Score : " + str(score), True, (0, 0, 0))
    screen.blit(scorev, (x-20, y+50))

def show_score(x, y):
    scorev = font.render("Score : " + str(score), True, (0, 0, 0))
    screen.blit(scorev, (x, y))




def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def stopGame():
    global game
    game = False


#Game Loop
while running:
    # Arkaplan
    screen.blit(background, (0, 0))


    if countdown == 0:

        gameOverText(overX,overY)
        stopGame()
    if countdown > 0:
        countT = font.render("Kalan zaman : " + str(countdown), True, (0, 0, 0))
        screen.blit(countT, (countX, countY))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -=1
            last_count = count_timer

    show_score(testY, textX)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game == True:
            # Klavyeden girdi girilmesi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3
                if event.key == pygame.K_RIGHT:
                    playerX_change = +3
                if event.key == pygame.K_SPACE:
                    bullet_Sound = mixer.Sound("fireMusic.wav")
                    bullet_Sound.play()
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_r and countdown == 0 :
                    countdown = 60
                    score = 0


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0


    # Ekran sınırlarının ayarlanması
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Düşman hareketi
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 1
        elif enemyY[i] >= 236:
            enemyY_change[i] = -1

            # Hedefi Vurma
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            exp_Sound = mixer.Sound("exp.mp3")
            exp_Sound.play()
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Merminin hareketi
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    pygame.display.update()
