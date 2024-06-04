# import block
import pygame, sys, random
from pygame.locals import *

# setup pygame
pygame.init()
mainClock = pygame.time.Clock()

# setup window
WINDOWWIDTH, WINDOWHEIGHT = 1000, 770
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption("RetroFighters")

# setup colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# text setup
FONT = pygame.font.Font(None, 36)  
score = 0

#load sounds
pickUpSound = pygame.mixer.Sound('pacChomp.wav')
blasterSound = pygame.mixer.Sound('blasterShot.wav')
alienPainSound = pygame.mixer.Sound('enemyDeath.wav')
fruitDropSound = pygame.mixer.Sound('fruitDrop.wav')
playerDeathSound = pygame.mixer.Sound('deathSound.wav')
gameStartSound = pygame.mixer.Sound('gameStart.wav')
victorySound = pygame.mixer.Sound('victorySound.wav')
selectSound = pygame.mixer.Sound('menuSelect.wav')

def welcomeScreen():
    gameLoop = True
    musicPlaying = True
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, 0.0)#LOAD BACKGROUND MUSIC
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                gameLoop = False

        # load menu image
        startMenuImg = pygame.image.load('startMenu.jpg')
        startMenuImg = pygame.transform.scale(startMenuImg, (WINDOWWIDTH, WINDOWHEIGHT))
    
        # widnow fill
        windowSurface.fill(BLACK)
        windowSurface.blit(startMenuImg, (0, 0))

        pygame.display.update()
        mainClock.tick(40)

def lvl1(score):
    #SETUP GAME
    gameClock = 0
    timeSwitch = False # flips at a certain time to increase game difficulty
    gameLoop = True
    win = False # win switch
    gameStartSound.play()
    pygame.mixer.music.stop()
    musicPlaying = True

    # set up music

    #SETUP PLAYER
    playerSize = 25
    player = pygame.Rect(300, WINDOWHEIGHT-75, playerSize, playerSize+28)

    #SETUP FRUITS
    fruits = []
    fruitPoints = 5

    #SETUP BULLETS
    bulletSize = 10
    maxBullets = 7
    bullSpeed = 12
    bullets = []

    #DRAW b(BASE) ENEMIES
    bEnemies = []
    bEnemySize = 25
    bXSwitches = [] 
    bEnemyXSpeed = 5
    bEnemyYSpeed = 0.45
    #enemy spacing
    bx = [950/16+1]
    by = [150, 250]
    for i in range(14):
        bx.append(bx[i]+bx[0])
    for i in range(15):
        bEnemies.append(pygame.Rect(bx[i], by[0], bEnemySize, bEnemySize))
        bEnemies.append(pygame.Rect(bx[i], by[1], bEnemySize, bEnemySize))
        bXSwitches.append(False)
        bXSwitches.append(False)

    #DRAW h(HARD) ENEMIES
    hEnemySize = 20
    hEnemies = []
    hEnemyHealth = []
    hEnemyXSpeed = 8
    hEnemyYSpeed = 0.45
    hXSwitches = [] 
    for i in range(15):
        hEnemies.append(pygame.Rect(bx[i], 50, hEnemySize, hEnemySize))
        hEnemyHealth.append(3)
        hXSwitches.append(False)

    # setup movement
    moveLeft, moveRight, moveUp, moveDown = False, False, False, False
    MOVESPEED = 6

    # load images
    foodImg = pygame.image.load('cherries.png')
    bEnemyImg = pygame.image.load('greenInvader.png')
    hEnemyImg = pygame.image.load('redInvader.png')
    marioLeft = pygame.image.load('marioLeft.png')
    marioRight = pygame.image.load('marioRight.png')
    bulletImg = pygame.image.load('bulletBill.png')
    starsImg = pygame.image.load('stars.png')
    playerFaceRight = True
    starsYPos = -10000

    # scale up images
    foodImg = pygame.transform.scale(foodImg, (playerSize*2, playerSize*2))
    bEnemyImg = pygame.transform.scale(bEnemyImg, (bEnemySize*3, bEnemySize*3))
    hEnemyImg = pygame.transform.scale(hEnemyImg, (hEnemySize*3.2, hEnemySize*3.2))
    marioLeft = pygame.transform.scale(marioLeft, (playerSize*3.5, playerSize*3.5 ))
    marioRight = pygame.transform.scale(marioRight, (playerSize*3.5, playerSize*3.5))
    bulletImg = pygame.transform.scale(bulletImg, (bulletSize*5, bulletSize*5))


    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            '''if event.type == QUIT:
                pygame.quit()
                sys.exit()'''
            
            # player move event
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a: moveRight, moveLeft = False, True
                if event.key == K_RIGHT or event.key == K_d: moveRight, moveLeft = True, False
                if event.key == K_UP or event.key == K_w: moveDown, moveUp = False, True
                if event.key == K_DOWN or event.key == K_s: moveDown, moveUp = True, False
                # more exit logic
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # player shoots
                if event.key == K_SPACE and len(bullets) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    if playerFaceRight:
                        bullets.append(pygame.Rect(player.x+playerSize*2, player.y, bulletSize, bulletSize))
                    else: bullets.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                # mute sound
                if event.key == K_m:
                    if musicPlaying:
                        musicPlaying = False
                        pygame.mixer.music.stop()
                    else:
                        musicPlaying = True
                        pygame.mixer.music.play(-1, 0.0)

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a: moveLeft = False
                if event.key == K_RIGHT or event.key == K_d: moveRight = False
                if event.key == K_UP or event.key == K_w: moveUp = False
                if event.key == K_DOWN or event.key == K_s: moveDown = False
            
        # draw background
        windowSurface.fill(BLACK)
        windowSurface.blit(starsImg, (0, starsYPos))
        starsYPos += 0.1

        # move the player
        '''if moveDown and player.bottom < WINDOWHEIGHT: # y-movement code
            player.top += MOVESPEED
        if moveUp and player.top > 0:
            player.top -= MOVESPEED'''
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
            playerFaceRight = False
        if moveRight and player.right < WINDOWWIDTH:
            player.right += MOVESPEED
            playerFaceRight = True

        # bullet benemy collision detection
        for enemy in bEnemies[:]:
            #ENEMY MOVEMENT
            idx = bEnemies.index(enemy)
            if bXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                bEnemies[idx].left += bEnemyXSpeed
            else: bEnemies[idx].left -= bEnemyXSpeed
            if bEnemies[idx].x >= WINDOWWIDTH - bEnemySize: bXSwitches[idx] = True
            elif bEnemies[idx].x <= 0: bXSwitches[idx] = False
            enemy.top += bEnemyYSpeed # slowly drop from screen
            if enemy.y >= WINDOWHEIGHT:
                enemy.top -= WINDOWHEIGHT+bEnemySize
                bEnemyYSpeed += 0.1
            #BULLET COLLISION
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                        fruitDropSound.play()
            # player bEnemy player collision check
            if enemy.colliderect(player):
                playerDeathSound.play()
                gameLoop = False
                return score, win


        # bullet henemy collision detection
        for enemy in hEnemies[:]:
            idx = hEnemies.index(enemy)
            if hXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                hEnemies[idx].left += hEnemyXSpeed
            else: hEnemies[idx].left -= hEnemyXSpeed
            if hEnemies[idx].x >= WINDOWWIDTH - hEnemySize: hXSwitches[idx] = True
            elif hEnemies[idx].x <= 0: hXSwitches[idx] = False
            enemy.top += hEnemyYSpeed # slowly drop from screen
            #hEnemy bulet collision check
            if enemy.y >= WINDOWHEIGHT:
                enemy.top -= WINDOWHEIGHT+hEnemySize
                hEnemyYSpeed += 0.1
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bullets.remove(bullet)
                    
            # player hEnemy player collision check
            if enemy.colliderect(player):
                playerDeathSound.play()
                gameLoop = False
                return score, win

        # mid game enemy speed up
        if gameClock >= 15 and timeSwitch == False: 
                hEnemyYSpeed += 0.55
                bEnemyYSpeed += 0.75
                # load & play rush music
                pygame.mixer.music.load('pacmanBackgroundLoop.wav') 
                pygame.mixer.music.play(-1, 0.0)#LOAD BACKGROUND MUSIC
                timeSwitch = True


        # move bullets up the screen and draw
        for bullet in bullets[:]:
            bullet.top -= bullSpeed
            if bullet.y < 0:
                bullets.remove(bullet)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletImg, (bullet.x-20,  bullet.y-20))

        # draw player
        #pygame.draw.rect(windowSurface, WHITE, player)
        if playerFaceRight:
            windowSurface.blit(marioRight, (player.x-40, player.y-17))
        else: windowSurface.blit(marioLeft, (player.x-40, player.y-17)) #centering img

        # draw the bEnemies
        for enemy in bEnemies[:]:
            #pygame.draw.rect(windowSurface, GREEN, enemy)
            windowSurface.blit(bEnemyImg, (enemy.x-25, enemy.y-20))

        # draw the hEnemies
        for enemy in hEnemies[:]:
            #pygame.draw.rect(windowSurface, RED, enemy)
            windowSurface.blit(hEnemyImg, (enemy.x-20, enemy.y-20))

        # draw the fruits and move down screen
        for fruit in fruits[:]:
            fruit.top += MOVESPEED/2
            if fruit.y > WINDOWHEIGHT:
                fruits.remove(fruit)
            #pygame.draw.rect(windowSurface, WHITE, fruit)
            windowSurface.blit(foodImg, (fruit.x-15, fruit.y-10))

            #player fruit collision check
            if player.colliderect(fruit):
                score += fruitPoints
                fruits.remove(fruit)
                if musicPlaying:
                    pickUpSound.play()

        # display text 
        pointsDisplay = FONT.render(f'Points: {score}', True, WHITE)
        windowSurface.blit(pointsDisplay, (50, WINDOWHEIGHT-50))

        # draw the window on the screen
        pygame.display.update()
        mainClock.tick(40)
        gameClock += 1/40

        # end game loop when no more enemies or fruits
        if not fruits and not bEnemies and not hEnemies: 
            gameLoop = False
            win = True
            victorySound.play()
            return score, win

def Lvl1WinScreen(score):
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=26)#LOAD BACKGROUND MUSIC
    currentKart = 0
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_s:
                    gameLoop = False
                    return currentKart
                if event.key == K_LEFT and currentKart > 0: currentKart -= 1; selectSound.play()
                if event.key == K_RIGHT and currentKart < 2: currentKart += 1; selectSound.play()
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load menu image
        lvl1Img = pygame.image.load('level1complete.png')
        lvl1Img = pygame.transform.scale(lvl1Img, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(lvl1Img, (0, 0))

        # load kart images
        marioKart = pygame.image.load('marioKartPngs/marioKart.png')
        peachKart = pygame.image.load('marioKartPngs/abbyKart.png')
        lugiKart = pygame.image.load('marioKartPngs/luigiKart.png')
        # scale up images
        kartSize = 200
        marioKart = pygame.transform.scale(marioKart, (kartSize, kartSize)) 
        peachKart = pygame.transform.scale(peachKart, (kartSize, kartSize))
        lugiKart = pygame.transform.scale(lugiKart, (kartSize, kartSize))
        # space out and print images
        imgSpace = WINDOWWIDTH/5
        windowSurface.blit(marioKart, (imgSpace, WINDOWHEIGHT/2+25))
        windowSurface.blit(peachKart, (imgSpace*2, WINDOWHEIGHT/2+25))
        windowSurface.blit(lugiKart, (imgSpace*3, WINDOWHEIGHT/2+25))

        # text display
        if win:
            line1 = FONT.render(f'Well done! You killed all the enemies and got {score} points', True, WHITE)
        line2 = FONT.render(f'It\'s only gonna get harder from here. Up next, level 2.', True, WHITE)
        line3 = FONT.render(f'New feature: Mario kart! Drift around the enemies.', True, WHITE)
        line4 = FONT.render(f'New controls: Mario kart! WASD shoot ARROW_KEYS move', True, WHITE)
        line5 = FONT.render(f'Pick a Kart and presss \'s\' to continue', True, WHITE)
        line6 = FONT.render(f'New feature 2: Bonus health! Now you can take 3 hits', True, WHITE)
        windowSurface.blit(line1, (100, 220))
        windowSurface.blit(line2, (100, 270))
        windowSurface.blit(line3, (100, 320))
        windowSurface.blit(line6, (100, 370))
        windowSurface.blit(line4, (100, 420))
        windowSurface.blit(line5, (100, 470))

        #kart selection
        if currentKart == 0:
            pygame.draw.rect(windowSurface, YELLOW, pygame.Rect(imgSpace-10, WINDOWHEIGHT/2+108, kartSize+13, kartSize/2+25), 5)
        if currentKart == 1:
            pygame.draw.rect(windowSurface, YELLOW, pygame.Rect(imgSpace*2-10, WINDOWHEIGHT/2+108, kartSize+13, kartSize/2+25), 5)
        if currentKart == 2:
            pygame.draw.rect(windowSurface, YELLOW, pygame.Rect(imgSpace*3-10, WINDOWHEIGHT/2+108, kartSize+13, kartSize/2+25), 5)
        

        pygame.display.update()
        mainClock.tick(40)

def gameOverScreen():
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=185)#LOAD BACKGROUND MUSIC
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                gameLoop = False
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load gameover image
        goImg = pygame.image.load('gameover.png')
        goImg = pygame.transform.scale(goImg, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(goImg, (0, 0))

        pygame.display.update()
        mainClock.tick(40)

def lvl2(score, currentKart):
    #SETUP GAME
    gameClock = 0
    timeSwitch = False # flips at a certain time to increase game difficulty
    gameLoop = True
    win = False # win switch
    gameStartSound.play()
    pygame.mixer.music.stop()
    musicPlaying = True

    # set up music

    #SETUP PLAYER
    playerSize = 25
    player = pygame.Rect(300, WINDOWHEIGHT-75, playerSize, playerSize+28)
    playerHealth = 3 # had to give the player health cuz this level is way too hard
    prevPlayerHealth = 3
    invulnerabilityClock = 0

    #SETUP FRUITS
    fruits = []
    fruitPoints = 5

    #SETUP BULLETS
    bulletSize = 10
    maxBullets = 7
    bullSpeed = 12
    bullets = []
    bulletsRight = []
    bulletsLeft = []
    bulletsDown = []
    #bullet directionality   

    #DRAW b(BASE) ENEMIES
    bEnemies = []
    bEnemySize = 25
    bXSwitches = [] 
    bEnemyXSpeed = 5
    bEnemyYSpeed = 0.3
    #enemy spacing
    bx = [950/16+1]
    by = [150, 250]
    for i in range(14):
        bx.append(bx[i]+bx[0])
    for i in range(13):
        bEnemies.append(pygame.Rect(bx[i], by[0], bEnemySize, bEnemySize))
        bEnemies.append(pygame.Rect(bx[i], by[1], bEnemySize, bEnemySize))
        bXSwitches.append(False)
        bXSwitches.append(False)

    #DRAW h(HARD) ENEMIES
    hEnemySize = 20
    hEnemies = []
    hEnemyHealth = []
    hEnemyXSpeed = 8
    hEnemyYSpeed = 0.3
    hXSwitches = [] 
    for i in range(10):
        hEnemies.append(pygame.Rect(bx[i], 50, hEnemySize, hEnemySize))
        hEnemies.append(pygame.Rect(bx[i], WINDOWHEIGHT + hEnemySize, hEnemySize, hEnemySize))
        hEnemyHealth.append(3)
        hXSwitches.append(False)
        hEnemyHealth.append(3)
        hXSwitches.append(False)

    # setup movement
    moveLeft, moveRight, moveUp, moveDown = False, False, False, False
    MOVESPEED = 6

    # load images
    foodImg = pygame.image.load('cherries.png')
    bEnemyImg = pygame.image.load('greenInvader.png')
    hEnemyImg = pygame.image.load('redInvader.png')
    if currentKart == 0: 
        marioLeft = pygame.image.load('marioKartPngs/marioMariKartLeft.png')
        marioRight = pygame.image.load('marioKartPngs/marioMariKartRight.png')
    elif currentKart == 1: 
        marioLeft = pygame.image.load('marioKartPngs/marioPeachKartLeft.png')
        marioRight = pygame.image.load('marioKartPngs/marioPeachKartRight.png')
    else: 
        marioLeft = pygame.image.load('marioKartPngs/marioLugiKartLeft.png')
        marioRight = pygame.image.load('marioKartPngs/marioLugiKartRight.png')
    bulletImg = pygame.image.load('bulletBill.png')
    starsImg = pygame.image.load('stars.png')
    playerFaceRight = True
    starsYPos = -10000
    # scale up images
    foodImg = pygame.transform.scale(foodImg, (playerSize*2, playerSize*2))
    bEnemyImg = pygame.transform.scale(bEnemyImg, (bEnemySize*3, bEnemySize*3))
    hEnemyImg = pygame.transform.scale(hEnemyImg, (hEnemySize*3.2, hEnemySize*3.2))
    marioLeft = pygame.transform.scale(marioLeft, (playerSize*3.5, playerSize*3.5))
    marioRight = pygame.transform.scale(marioRight, (playerSize*3.5, playerSize*3.5))
    bulletImg = pygame.transform.scale(bulletImg, (bulletSize*5, bulletSize*5))
    #rotate bullet images
    bulletRightImg = pygame.transform.rotate(bulletImg, 270)
    bulletDownImg = pygame.transform.rotate(bulletImg, 180)
    bulletLeftImg = pygame.transform.rotate(bulletImg, 90)
    # flip bullet left image
    bulletLeftImg = pygame.transform.flip(bulletLeftImg, False, True)
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            '''if event.type == QUIT:
                pygame.quit()
                sys.exit()'''
            
            # player move event
            if event.type == KEYDOWN:
                if event.key == K_LEFT: moveRight, moveLeft = False, True
                if event.key == K_RIGHT: moveRight, moveLeft = True, False
                if event.key == K_UP: moveDown, moveUp = False, True
                if event.key == K_DOWN: moveDown, moveUp = True, False
                # more exit logic
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # player shoots
                if event.key == K_w and len(bullets) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    if playerFaceRight:
                        bullets.append(pygame.Rect(player.x+playerSize//2, player.y, bulletSize, bulletSize))
                    else: bullets.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                if event.key == K_d and len(bulletsRight) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    bulletsRight.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                if event.key == K_a and len(bulletsLeft) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    bulletsLeft.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                if event.key == K_s and len(bulletsDown) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    if playerFaceRight:
                        bulletsDown.append(pygame.Rect(player.x+playerSize//2, player.y, bulletSize, bulletSize))
                    else: bulletsDown.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                # mute sound
                if event.key == K_m:
                    if musicPlaying:
                        musicPlaying = False
                        pygame.mixer.music.stop()
                    else:
                        musicPlaying = True
                        pygame.mixer.music.play(-1, 0.0)

            if event.type == KEYUP:
                if event.key == K_LEFT: moveLeft = False
                if event.key == K_RIGHT: moveRight = False
                if event.key == K_UP: moveUp = False
                if event.key == K_DOWN: moveDown = False
            
        # draw background
        windowSurface.fill(BLACK)
        windowSurface.blit(starsImg, (0, starsYPos))
        starsYPos += 0.1

        # move the player
        if moveDown and player.bottom < WINDOWHEIGHT: # y-movement code
            player.top += MOVESPEED
        if moveUp and player.top > 0:
            player.top -= MOVESPEED
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
            playerFaceRight = False
        if moveRight and player.right < WINDOWWIDTH:
            player.right += MOVESPEED
            playerFaceRight = True

        # bullet benemy collision detection
        for enemy in bEnemies[:]:
            #ENEMY MOVEMENT
            idx = bEnemies.index(enemy)
            if bXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                bEnemies[idx].left += bEnemyXSpeed
            else: bEnemies[idx].left -= bEnemyXSpeed
            if bEnemies[idx].x >= WINDOWWIDTH - bEnemySize: bXSwitches[idx] = True
            elif bEnemies[idx].x <= 0: bXSwitches[idx] = False
            enemy.top += bEnemyYSpeed # slowly drop from screen
            if enemy.y >= WINDOWHEIGHT:
                enemy.top -= WINDOWHEIGHT+bEnemySize
                bEnemyYSpeed += 0.1
            #BULLET COLLISION
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                        fruitDropSound.play()
            for bulletR in bulletsRight[:]:
                if bulletR.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bulletsRight.remove(bulletR)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                        fruitDropSound.play()
            for bulletA in bulletsLeft[:]:
                if bulletA.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bulletsLeft.remove(bulletA)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                        fruitDropSound.play()
            for bulletS in bulletsDown[:]:
                if bulletS.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bulletsDown.remove(bulletS)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                        fruitDropSound.play()
            # player bEnemy player collision check
            if enemy.colliderect(player) and invulnerabilityClock < 0:
                playerHealth -= 1
                invulnerabilityClock = 3
                if playerHealth <= 0:
                    playerDeathSound.play()
                    gameLoop = False
                    return score, win

        # bullet henemy collision detection
        for enemy in hEnemies[:]:
            idx = hEnemies.index(enemy)
            if hXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                hEnemies[idx].left += hEnemyXSpeed
            else: hEnemies[idx].left -= hEnemyXSpeed
            if hEnemies[idx].x >= WINDOWWIDTH - hEnemySize: hXSwitches[idx] = True
            elif hEnemies[idx].x <= 0: hXSwitches[idx] = False
            if idx % 2 == 0:
                enemy.top += hEnemyYSpeed # slowly drop from screen
            else: enemy.top -= hEnemyYSpeed # slowly rise from screen
            #hEnemy bulet collision check
            if gameClock > 7:
                if enemy.y > WINDOWHEIGHT:
                    enemy.top -= WINDOWHEIGHT
                    #hEnemyYSpeed += 0.1
            if enemy.y < 0:
                enemy.top += WINDOWHEIGHT
                #hEnemyYSpeed += 0.1
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bullets.remove(bullet)
            for bulletR in bulletsRight[:]:
                if bulletR.colliderect(enemy):
                    hEnemyHealth[idx] -= 1.5
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bulletsRight.remove(bulletR)
            for bulletA in bulletsLeft[:]:
                if bulletA.colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bulletsLeft.remove(bulletA)
            for bulletS in bulletsDown[:]:
                if bulletS.colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bulletsDown.remove(bulletS)
                    
            # player hEnemy player collision check
            if enemy.colliderect(player) and invulnerabilityClock < 0:
                playerHealth -= 1
                invulnerabilityClock = 3
                if playerHealth <= 0:
                    playerDeathSound.play()
                    gameLoop = False
                    return score, win

        # mid game enemy speed up
        if gameClock >= 5 and timeSwitch == False: 
                hEnemyYSpeed += 0.21
                bEnemyYSpeed += 0.21
                # load & play rush music
                pygame.mixer.music.load('pacmanBackgroundLoop.wav') 
                pygame.mixer.music.play(-1, 0.0)#LOAD BACKGROUND MUSIC
                timeSwitch = True

        # move bullets up the screen and draw
        for bullet in bullets[:]:
            bullet.top -= bullSpeed
            if bullet.y < 0:
                bullets.remove(bullet)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletImg, (bullet.x-20,  bullet.y-20))
        for bulletR in bulletsRight[:]:
            bulletR.left += bullSpeed
            if bulletR.x > WINDOWWIDTH:
                bulletsRight.remove(bulletR)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletRightImg, (bulletR.x-20,  bulletR.y-20))
        for bulletL in bulletsLeft[:]:
            bulletL.left -= bullSpeed
            if bulletL.x < 0:
                bulletsLeft.remove(bulletL)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletLeftImg, (bulletL.x-20,  bulletL.y-20))
        for bulletD in bulletsDown[:]:
            bulletD.top += bullSpeed
            if bulletD.y > WINDOWHEIGHT:
                bulletsDown.remove(bulletD)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletDownImg, (bulletD.x-20,  bulletD.y-20))


        # draw player and invulnerability frames
        if invulnerabilityClock > 0:
            if invulnerabilityClock < 3:
                pygame.draw.rect(windowSurface, WHITE, player)
            if invulnerabilityClock < 2.5:
                if playerFaceRight:
                    windowSurface.blit(marioRight, (player.x-40, player.y-17))
                else: windowSurface.blit(marioLeft, (player.x-40, player.y-17)) #centering img
            if invulnerabilityClock < 2:
                pygame.draw.rect(windowSurface, WHITE, player)
            if invulnerabilityClock < 1.5:
                if playerFaceRight:
                    windowSurface.blit(marioRight, (player.x-40, player.y-17))
                else: windowSurface.blit(marioLeft, (player.x-40, player.y-17)) #centering img
            if invulnerabilityClock < 1:
                pygame.draw.rect(windowSurface, WHITE, player)
            if invulnerabilityClock < 0.5:
                if playerFaceRight:
                    windowSurface.blit(marioRight, (player.x-40, player.y-17))
                else: windowSurface.blit(marioLeft, (player.x-40, player.y-17)) #centering img
        else:
            if playerFaceRight:
                windowSurface.blit(marioRight, (player.x-40, player.y-17))
            else: windowSurface.blit(marioLeft, (player.x-40, player.y-17)) #centering img
            prevPlayerHealth = playerHealth
        invulnerabilityClock -= 1/40

        # draw the bEnemies
        for enemy in bEnemies[:]:
            #pygame.draw.rect(windowSurface, GREEN, enemy)
            windowSurface.blit(bEnemyImg, (enemy.x-25, enemy.y-20))

        # draw the hEnemies
        for enemy in hEnemies[:]:
            #pygame.draw.rect(windowSurface, RED, enemy)
            windowSurface.blit(hEnemyImg, (enemy.x-20, enemy.y-20))

        # draw the fruits and move down screen
        for fruit in fruits[:]:
            if gameClock < 20:
                if moveUp: fruit.top -= MOVESPEED/2
                if moveRight: fruit.right += MOVESPEED//3
                if moveLeft: fruit.right -= MOVESPEED//3
                if moveDown: fruit.top += MOVESPEED/2
            fruit.top += MOVESPEED/2
            if fruit.y > WINDOWHEIGHT:
                fruits.remove(fruit)
            #pygame.draw.rect(windowSurface, WHITE, fruit)
            windowSurface.blit(foodImg, (fruit.x-15, fruit.y-10))

            #player fruit collision check
            if player.colliderect(fruit):
                score += fruitPoints
                fruits.remove(fruit)
                if musicPlaying:
                    pickUpSound.play()

        # display text 
        pointsDisplay = FONT.render(f'Points: {score}', True, WHITE)
        windowSurface.blit(pointsDisplay, (50, WINDOWHEIGHT-50))
        healthDisplay = FONT.render(f'Player health: {playerHealth}', True, WHITE)
        windowSurface.blit(healthDisplay, (50, WINDOWHEIGHT-80))

        # draw the window on the screen
        pygame.display.update()
        mainClock.tick(40)
        gameClock += 1/40

        # end game loop when no more enemies or fruits
        if not fruits and not bEnemies and not hEnemies: 
            gameLoop = False
            win = True
            victorySound.play()
            return score, win
        
def Lvl2WinScreen(score):
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=26)#LOAD BACKGROUND MUSIC
    currentKart = 0
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_s:
                    gameLoop = False
                    return currentKart
                if event.key == K_LEFT and currentKart > 0: currentKart -= 1; selectSound.play()
                if event.key == K_RIGHT and currentKart < 2: currentKart += 1; selectSound.play()
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load menu image
        lvl2Img = pygame.image.load('level2complete.png')
        lvl2Img = pygame.transform.scale(lvl2Img, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(lvl2Img, (0, 0))
 
        # text display
        if win:
            line1 = FONT.render(f'Well done! You killed all the enemies and have {score} points', True, WHITE)
        line2 = FONT.render(f'It\'s only gonna get harder from here. Up next, level 4.', True, WHITE)
        line4 = FONT.render(f'New feature: Koopa Shells! Catch and throw shells!', True, WHITE)
        line5 = FONT.render(f'New controls: Press C to shoot green shells left and M to shoot right', True, WHITE)
        line6 = FONT.render(f'At 20 points catch the red shell, and press v to shoot it', True, WHITE)
        line7 = FONT.render(f'At 40 points catch the blue shell, and press b to shoot it', True, WHITE)
        line8 = FONT.render(f'Presss \'s\' to continue', True, WHITE)
        windowSurface.blit(line1, (100, 220))
        windowSurface.blit(line2, (100, 270))
        windowSurface.blit(line4, (100, 320))
        windowSurface.blit(line5, (100, 370))
        windowSurface.blit(line6, (100, 420))
        windowSurface.blit(line7, (100, 470))
        windowSurface.blit(line8, (100, 520))
        
        pygame.display.update()
        mainClock.tick(40)

def lvl3(score):
    # SETUP GAME
    gameClock = 0
    timeSwitch = False # flips at a certain time to increase game difficulty
    gameLoop = True
    win = False # win switch
    gameStartSound.play()
    pygame.mixer.music.stop()

    # set up music
    musicPlaying = True
    pickUpSound = pygame.mixer.Sound('pickup.wav')
    blasterSound = pygame.mixer.Sound('blaster.wav')
    alienPainSound = pygame.mixer.Sound('alienPain.wav')
    '''pygame.mixer.music.load('returbFromBreak/apr1/background.mid')pygame.mixer.music.play(-1,0.0)'''

    # SETUP PLAYER
    playerSize = 25
    player = pygame.Rect(300, WINDOWHEIGHT-75, playerSize, playerSize)

    # SETUP FRUITS
    fruits = []
    fruitPoints = 5

    # SETUP BULLETS
    bulletSize = 10
    maxBullets = 7
    bullSpeed = 12
    bullets = []

    # DRAW b(BASE) ENEMIES
    bEnemies = []
    bEnemySize = 25
    bXSwitches = []
    bEnemyXSpeed = 5
    bEnemyYSpeed = 0.4
    bx = [950/16+1]
    by = [150, 250]
    for i in range(14):
        bx.append(bx[i]+bx[0])
    for i in range(12):
        bEnemies.append(pygame.Rect(bx[i], by[0], bEnemySize, bEnemySize))
        bEnemies.append(pygame.Rect(bx[i], by[1], bEnemySize, bEnemySize))
        bXSwitches.append(False)
        bXSwitches.append(False)

    # DRAW h(HARD) ENEMIES
    hEnemySize = 20
    hEnemies = []
    hEnemyHealth = []
    hEnemyXSpeed = 8
    hEnemyYSpeed = 0.45
    hXSwitches = []
    for i in range(10):
        hEnemies.append(pygame.Rect(bx[i], 50, hEnemySize, hEnemySize))
        hEnemyHealth.append(3)
        hXSwitches.append(False)

    # setup movement
    moveLeft, moveRight, moveUp, moveDown = False, False, False, False
    MOVESPEED = 6

    # load images
    foodImg = pygame.image.load('cherries.png')
    bEnemyImg = pygame.image.load('greenInvader.png')
    hEnemyImg = pygame.image.load('redInvader.png')
    racketLeft = pygame.image.load('racket_left.png')
    racketRight = pygame.image.load('racket_right.png')
    pongImg = pygame.image.load('pong_ball.png')
    starsImg = pygame.image.load('stars.png')
    playerFaceRight = True
    starsYPos = -10000

    # scale down images
    foodImg = pygame.transform.scale(foodImg, (playerSize*2, playerSize*2))
    bEnemyImg = pygame.transform.scale(bEnemyImg, (bEnemySize*3, bEnemySize*3))
    hEnemyImg = pygame.transform.scale(hEnemyImg, (hEnemySize*3.2, hEnemySize*3.2))
    racketLeft = pygame.transform.scale(racketLeft, (playerSize*3.5, playerSize*3.5 ))
    racketRight = pygame.transform.scale(racketRight, (playerSize*3.5, playerSize*3.5))
    pongImg = pygame.transform.scale(pongImg, (bulletSize*5, bulletSize*5))


    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            '''if event.type == QUIT:
                pygame.quit()
                sys.exit()'''

            # player move event
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a: moveRight, moveLeft = False, True
                if event.key == K_RIGHT or event.key == K_d: moveRight, moveLeft = True, False
                if event.key == K_UP or event.key == K_w: moveDown, moveUp = False, True
                if event.key == K_DOWN or event.key == K_s: moveDown, moveUp = True, False
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE and len(bullets) < maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    if playerFaceRight:
                        bullets.append({"rect": pygame.Rect(player.x+playerSize*2, player.y, bulletSize, bulletSize), "direction": "up"})
                    else:
                        bullets.append({"rect": pygame.Rect(player.x, player.y, bulletSize, bulletSize), "direction": "up"})

            '''if event.key == K_m:
                    if musicPlaying:
                        musicPlaying = False
                        pygame.mixer.music.stop()
                    else:
                        musicPlaying = True
                        pygame.mixer.music.play(-1, 0.0)'''#add after background music is found

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a: moveLeft = False
                if event.key == K_RIGHT or event.key == K_d: moveRight = False
                if event.key == K_UP or event.key == K_w: moveUp = False
                if event.key == K_DOWN or event.key == K_s: moveDown = False

        # draw background
        windowSurface.fill(BLACK)
        windowSurface.blit(starsImg, (0, starsYPos))
        starsYPos += 0.1

        # move the player
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
            playerFaceRight = False
        if moveRight and player.right < WINDOWWIDTH:
            player.right += MOVESPEED
            playerFaceRight = True

        # bullet benemy collision detection
        for enemy in bEnemies[:]:
            #ENEMY MOVEMENT
            idx = bEnemies.index(enemy)
            if bXSwitches[idx] == False:
                enemy.left += bEnemyXSpeed
            else:
                enemy.left -= bEnemyXSpeed
            if enemy.x >= WINDOWWIDTH - bEnemySize:
                bXSwitches[idx] = True
            elif enemy.x <= 0:
                bXSwitches[idx] = False
            if enemy.y > player.y:
                enemy.top += bEnemyYSpeed
            #BULLET COLLISION
            for bullet in bullets[:]:
                if bullet["rect"].colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
            # player bEnemy player collision check
            if enemy.colliderect(player):
                gameLoop = False
                return score, win


        # bullet henemy collision detection
        for enemy in hEnemies[:]:
            idx = hEnemies.index(enemy)
            if hXSwitches[idx] == False:
                enemy.left += hEnemyXSpeed
            else:
                enemy.left -= hEnemyXSpeed
            if enemy.x >= WINDOWWIDTH - hEnemySize:
                hXSwitches[idx] = True
            elif enemy.x <= 0:
                hXSwitches[idx] = False
            enemy.top += hEnemyYSpeed
            #hEnemy bullet collision check
            for bullet in bullets[:]:
                if bullet["rect"].colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bullets.remove(bullet)
                    
            # player hEnemy player collision check
            if enemy.colliderect(player):
                gameLoop = False
                return score, win

        # mid game enemy speed up
        if gameClock >= 15 and timeSwitch == False:
                hEnemyYSpeed += 0.55
                bEnemyYSpeed += 0.50
                timeSwitch = True

        # move bullets up and down the screen and draw
        for bullet in bullets:
            if bullet["direction"] == "up":
                bullet["rect"].top -= bullSpeed
                if bullet["rect"].top <= 0:
                    bullet["direction"] = "down"
            elif bullet["direction"] == "down":
                bullet["rect"].top += bullSpeed
                if bullet["rect"].top >= WINDOWHEIGHT:
                    bullets.remove(bullet)
            windowSurface.blit(pongImg, (bullet["rect"].x-20, bullet["rect"].y-20))

        # draw player
        if playerFaceRight:
            windowSurface.blit(racketRight, (player.x-40, player.y-20))
        else:
            windowSurface.blit(racketLeft, (player.x-40, player.y-20)) #centering img

        # draw the bEnemies
        for enemy in bEnemies:
            windowSurface.blit(bEnemyImg, (enemy.x-30, enemy.y-20))

        # draw the hEnemies
        for enemy in hEnemies:
            windowSurface.blit(hEnemyImg, (enemy.x-20, enemy.y-20))

        # draw the fruits and move down screen
        for fruit in fruits:
            fruit.top += MOVESPEED/2
            if fruit.y > WINDOWHEIGHT:
                fruits.remove(fruit)
            windowSurface.blit(foodImg, (fruit.x-playerSize//2, fruit.y))

            #player fruit collision check
            if player.colliderect(fruit):
                score += fruitPoints
                fruits.remove(fruit)
                pickUpSound.play()

        # display text 
        pointsDisplay = FONT.render(f'Points: {score}', True, WHITE)
        windowSurface.blit(pointsDisplay, (50, WINDOWHEIGHT-50))

        # draw the window on the screen
        pygame.display.update()
        mainClock.tick(40)
        gameClock += 1/40

        # end game loop when no more enemies or fruits
        if not fruits and not bEnemies and not hEnemies: 
            gameLoop = False
            win = True
            return score, win
        
def Lvl3WinScreen(score):
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=26)#LOAD BACKGROUND MUSIC
    currentKart = 0
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_s:
                    gameLoop = False
                    return currentKart
                if event.key == K_LEFT and currentKart > 0: currentKart -= 1; selectSound.play()
                if event.key == K_RIGHT and currentKart < 2: currentKart += 1; selectSound.play()
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load menu image
        lvl1Img = pygame.image.load('level3complete.png')
        lvl1Img = pygame.transform.scale(lvl1Img, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(lvl1Img, (0, 0))

        # text display
        if win:
            line1 = FONT.render(f'Well done! You killed all the enemies and got {score} points', True, WHITE)
        line2 = FONT.render(f'It\'s only gonna get harder from here. Up next, level 3.', True, WHITE)
        line3 = FONT.render(f'New feature: Pong! Bounce balls to kill enemies', True, WHITE)
        line4 = FONT.render(f'New controls: Space shoot ARROW_KEYS move', True, WHITE)
        line5 = FONT.render(f'Press \'s\' to continue', True, WHITE)
        windowSurface.blit(line1, (100, 220))
        windowSurface.blit(line2, (100, 270))
        windowSurface.blit(line3, (100, 320))
        windowSurface.blit(line4, (100, 370))
        windowSurface.blit(line5, (100, 420))

        pygame.display.update()
        mainClock.tick(40)

def Lvl4WinScreen(score):
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=26)#LOAD BACKGROUND MUSIC
    currentKart = 0
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_s:
                    gameLoop = False
                    return currentKart
                if event.key == K_LEFT and currentKart > 0: currentKart -= 1; selectSound.play()
                if event.key == K_RIGHT and currentKart < 2: currentKart += 1; selectSound.play()
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load menu image
        lvl1Img = pygame.image.load('level3complete.png')
        lvl1Img = pygame.transform.scale(lvl1Img, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(lvl1Img, (0, 0))

        # text display
        if win:
            line1 = FONT.render(f'Well done! You killed all the enemies and got {score} points', True, WHITE)
        line2 = FONT.render(f'It\'s only gonna get harder from here. Up next, level 3.', True, WHITE)
        line3 = FONT.render(f'New feature: Pong! Bounce balls to kill enemies', True, WHITE)
        line4 = FONT.render(f'New controls: Space shoot ARROW_KEYS move', True, WHITE)
        windowSurface.blit(line1, (100, 220))
        windowSurface.blit(line2, (100, 270))
        windowSurface.blit(line3, (100, 320))
        windowSurface.blit(line4, (100, 420))

        pygame.display.update()
        mainClock.tick(40)

def lvl4(score):
    #SETUP GAME
    gameClock = 0
    timeSwitch = False # flips at a certain time to increase game difficulty
    gameLoop = True
    win = False # win switch
    gameStartSound.play()
    pygame.mixer.music.stop()
    redScore = score+20
    blueScore = score+40

    # set up music
    musicPlaying = True
    pickUpSound = pygame.mixer.Sound('pickup.wav')
    blasterSound = pygame.mixer.Sound('blaster.wav')
    alienPainSound = pygame.mixer.Sound('alienPain.wav')
    greenShellSound = pygame.mixer.Sound('greenshellsound.wav')
    redShellSound = pygame.mixer.Sound('redShellSound.wav')
    blueShellSound = pygame.mixer.Sound('blueShellSound.wav')
    '''pygame.mixer.music.load('returnFromBreak/apr1/background.mid') 
    pygame.mixer.music.play(-1, 0.0)'''#LOAD BACKGROUND MUSIC

    #SETUP PLAYER
    playerSize = 25
    player = pygame.Rect(300, WINDOWHEIGHT-75, playerSize, playerSize)

    #SETUP FRUITS
    fruits = []
    fruitPoints = 5

    #SETUP BULLETS
    bulletSize = 10
    maxBullets = 7
    bullSpeed = 12
    bullets = []

    #SETUP GREEN SHELLS
    greenShellSize = 10
    greenShellSpeed = 12 
    MaxGreenShell = 2
    greenShells = [] 

    #SETUP RED SHELLS
    redShellSize = 10
    redShellSpeed = 12 
    MaxRedShell = 1
    redShells = []

    #SETUP BLUE SHELLS
    blueShellSize = 10
    blueShellSpeed = 12 
    MaxBlueShell = 1
    blueShells = []
    explosionRadius = 100

    #SETUP FALLING SHELLS
    hasRedShell = False
    hasBlueShell = False
    redShellUnlocked = False
    blueShellUnlocked = False
    powerUpSize = 30
    powerUpFallSpeed = 5
    powerUpShells = []
    def dropPowerUpShell(type, x, y, powerUpShells, powerUpSize):
        powerUpShells.append({'type': type, 'rect': pygame.Rect(x, y, powerUpSize, powerUpSize)})

    #DRAW b(BASE) ENEMIES
    bEnemies = []
    bEnemySize = 25
    bXSwitches = [] 
    bEnemyXSpeed = 5
    bEnemyYSpeed = 0.4
    #enemy spacing
    bx = [950/16+1]
    by = [200, 250, 300]
    for i in range(14):
        bx.append(bx[i]+bx[0])
    for i in range(15):
        bEnemies.append(pygame.Rect(bx[i], by[0], bEnemySize, bEnemySize))
        bEnemies.append(pygame.Rect(bx[i], by[1], bEnemySize, bEnemySize))
        bEnemies.append(pygame.Rect(bx[i], by[2], bEnemySize, bEnemySize))
        bXSwitches.append(False)
        bXSwitches.append(False)
        bXSwitches.append(False)

    #DRAW h(HARD) ENEMIES
    hEnemySize = 20
    hEnemies = []
    hEnemyHealth = []
    hEnemyXSpeed = 8
    hEnemyYSpeed = 0.45
    hXSwitches = [] 
    for i in range(15):
        hEnemies.append(pygame.Rect(bx[i], 50, hEnemySize, hEnemySize))
        hEnemyHealth.append(3)
        hXSwitches.append(False)

    # setup movement
    moveLeft, moveRight, moveUp, moveDown = False, False, False, False
    MOVESPEED = 6

    # load images
    foodImg = pygame.image.load('cherries.png')
    bEnemyImg = pygame.image.load('greenInvader.png')
    hEnemyImg = pygame.image.load('redInvader.png')
    marioLeft = pygame.image.load('marioLeft.png')
    marioRight = pygame.image.load('marioRight.png')
    bulletImg = pygame.image.load('bulletBill.png')
    starsImg = pygame.image.load('stars.png')
    greenShellImg = pygame.image.load('greenShell.png')
    redShellImg = pygame.image.load('redShell.png')
    blueShellImg = pygame.image.load('blueShell.png')
    playerFaceRight = True
    starsYPos = -10000

    # scale down images
    foodImg = pygame.transform.scale(foodImg, (playerSize*2, playerSize*2))
    bEnemyImg = pygame.transform.scale(bEnemyImg, (bEnemySize*3, bEnemySize*3))
    hEnemyImg = pygame.transform.scale(hEnemyImg, (hEnemySize*3.2, hEnemySize*3.2))
    marioLeft = pygame.transform.scale(marioLeft, (playerSize*3.5, playerSize*3.5 ))
    marioRight = pygame.transform.scale(marioRight, (playerSize*3.5, playerSize*3.5))
    bulletImg = pygame.transform.scale(bulletImg, (bulletSize*5, bulletSize*5))
    greenShellImg = pygame.transform.scale(greenShellImg, (greenShellSize*8, greenShellSize*8))
    redShellImg = pygame.transform.scale(redShellImg, (redShellSize*8, redShellSize*8))
    blueShellImg = pygame.transform.scale(blueShellImg, (blueShellSize*8, blueShellSize*8))

    powerUpImages = {
    'red': redShellImg,
    'blue': blueShellImg
}

    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # player move event
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a: moveRight, moveLeft = False, True
                if event.key == K_RIGHT or event.key == K_d: moveRight, moveLeft = True, False
                if event.key == K_UP or event.key == K_w: moveDown, moveUp = False, True
                if event.key == K_DOWN or event.key == K_s: moveDown, moveUp = True, False
                # more exit logic
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # player shoots
                if event.key == K_SPACE and len(bullets) <= maxBullets:
                    if musicPlaying:
                        blasterSound.play()
                    if playerFaceRight:
                        bullets.append(pygame.Rect(player.x+playerSize*2, player.y, bulletSize, bulletSize))
                    else: bullets.append(pygame.Rect(player.x, player.y, bulletSize, bulletSize))
                if event.key == K_c and len(greenShells) <= MaxGreenShell:  
                    greenShells.append({'rect': pygame.Rect(player.centerx, player.centery, greenShellSize, greenShellSize), 'dir': 'left'})
                    if musicPlaying:
                        greenShellSound.play()
                if event.key == K_m and len(greenShells) <= MaxGreenShell: 
                    greenShells.append({'rect': pygame.Rect(player.centerx, player.centery, greenShellSize, greenShellSize), 'dir': 'right'})
                    if musicPlaying:
                        greenShellSound.play()
                if event.key == K_v and hasRedShell and len(redShells) < MaxRedShell: 
                    if hEnemies: 
                        target = hEnemies[0] 
                        redShells.append({'rect': pygame.Rect(player.centerx, player.centery, redShellSize, redShellSize), 'target': target})
                    if musicPlaying:
                        redShellSound.play()
                if event.key == K_b and hasBlueShell and len(blueShells) < MaxBlueShell:
                    if bEnemies or hEnemies:
                        target = min(bEnemies + hEnemies, key=lambda e: (player.centerx - e.centerx)**2 + (player.centery - e.centery)**2)
                        blueShells.append({'rect': pygame.Rect(player.centerx, player.centery, blueShellSize, blueShellSize), 'target': target})
                    if musicPlaying:
                        blueShellSound.play()



                # mute sound
                '''if event.key == K_m:
                    if musicPlaying:
                        musicPlaying = False
                        pygame.mixer.music.stop()
                    else:
                        musicPlaying = True
                        pygame.mixer.music.play(-1, 0.0)'''#add after background music is found

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a: moveLeft = False
                if event.key == K_RIGHT or event.key == K_d: moveRight = False
                if event.key == K_UP or event.key == K_w: moveUp = False
                if event.key == K_DOWN or event.key == K_s: moveDown = False
            
        # draw background
        windowSurface.fill(BLACK)
        windowSurface.blit(starsImg, (0, starsYPos))
        starsYPos += 0.1

        # move the player
        '''if moveDown and player.bottom < WINDOWHEIGHT: # y-movement code
            player.top += MOVESPEED
        if moveUp and player.top > 0:
            player.top -= MOVESPEED'''
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
            playerFaceRight = False
        if moveRight and player.right < WINDOWWIDTH:
            player.right += MOVESPEED
            playerFaceRight = True

        # bullet benemy collision detection
        for enemy in bEnemies[:]:
            #ENEMY MOVEMENT
            idx = bEnemies.index(enemy)
            if bXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                bEnemies[idx].left += bEnemyXSpeed
            else: bEnemies[idx].left -= bEnemyXSpeed
            if bEnemies[idx].x >= WINDOWWIDTH - bEnemySize: bXSwitches[idx] = True
            elif bEnemies[idx].x <= 0: bXSwitches[idx] = False
            if enemy.y > player.y:
                enemy.top += bEnemyYSpeed # slowly drop from screen
            #BULLET COLLISION
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    if musicPlaying:
                        alienPainSound.play()
                    bEnemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
            #GREEN SHELL COLLISION
        for shell in greenShells[:]:
            for enemy in bEnemies[:]:
                if shell['rect'].colliderect(enemy):
                    bEnemies.remove(enemy)
                    greenShells.remove(shell)
                    score += 1 
                    break

                # fruit drop chance
                    if random.randint(1, 8) == 1:
                        fruits.append(pygame.Rect(enemy.x+bEnemySize//2, enemy.y, hEnemySize, hEnemySize))
            # player bEnemy player collision check
            if enemy.colliderect(player):
                gameLoop = False
                return score, win


        # bullet henemy collision detection
        for enemy in hEnemies[:]:
            idx = hEnemies.index(enemy)
            if hXSwitches[idx] == False: # if enemy switch is false move right otherwise left
                hEnemies[idx].left += hEnemyXSpeed
            else: hEnemies[idx].left -= hEnemyXSpeed
            if hEnemies[idx].x >= WINDOWWIDTH - hEnemySize: hXSwitches[idx] = True
            elif hEnemies[idx].x <= 0: hXSwitches[idx] = False
            if enemy.y <= WINDOWHEIGHT-75: enemy.top += hEnemyYSpeed # slowly drop from screen
            #hEnemy bulet collision check
            for bullet in bullets[:]:
                if bullet.colliderect(enemy):
                    hEnemyHealth[idx] -= 1
                    if musicPlaying:
                        alienPainSound.play()
                    if hEnemyHealth[idx] <= 0:
                        hEnemies.remove(enemy)
                        score += 2
                        # fruit drop chance
                        if random.randint(1, 3) == 1:
                            fruits.append(pygame.Rect(enemy.x+hEnemySize//2, enemy.y, hEnemySize, hEnemySize))
                    bullets.remove(bullet)
            # player hEnemy player collision check
            if enemy.colliderect(player):
                gameLoop = False
                return score, win
        
            #GREEN SHELL COLLISION
        for shell in greenShells[:]:
            for enemy in hEnemies[:]:
                if shell['rect'].colliderect(enemy):
                    hEnemies.remove(enemy)
                    greenShells.remove(shell)
                    score += 2
                    break  
        
        for shell in redShells:
            target_center = shell['target'].center
            shell_center = shell['rect'].center
            direction = pygame.math.Vector2(target_center[0] - shell_center[0], target_center[1] - shell_center[1])
            if direction.length() > 0:
                direction = direction.normalize()
            shell['rect'].x += int(direction.x * redShellSpeed)
            shell['rect'].y += int(direction.y * redShellSpeed)

            for enemy in hEnemies[:]:
                if shell['rect'].colliderect(enemy):
                    hEnemies.remove(enemy)
                    redShells.remove(shell)
                    score += 2

            windowSurface.blit(redShellImg, (shell['rect'].x, shell['rect'].y))

        
        for shell in blueShells[:]:
            target_center = shell['target'].center
            shell_center = shell['rect'].center

            direction = pygame.math.Vector2(target_center[0] - shell_center[0], target_center[1] - shell_center[1])
            if direction.length() > 0:
                direction = direction.normalize()

            shell['rect'].x += int(direction.x * blueShellSpeed)
            shell['rect'].y += int(direction.y * blueShellSpeed)

            if shell['rect'].colliderect(shell['target']):
                explosion_center = shell['target'].center
                for enemy in bEnemies + hEnemies:
                    if pygame.math.Vector2(enemy.centerx - explosion_center[0], enemy.centery - explosion_center[1]).length() <= explosionRadius:
                        if enemy in bEnemies:
                            bEnemies.remove(enemy)
                        elif enemy in hEnemies:
                            hEnemies.remove(enemy)
                blueShells.remove(shell)
                score += 1

            windowSurface.blit(blueShellImg, (shell['rect'].x, shell['rect'].y))

        if score >= redScore and not redShellUnlocked:
            dropPowerUpShell('red', random.randint(0, WINDOWWIDTH), 0, powerUpShells, powerUpSize)
            redShellUnlocked = True

        # Check if the player should unlock the blue shell
        if score >= blueScore and not blueShellUnlocked:
            dropPowerUpShell('blue', random.randint(0, WINDOWWIDTH), 0, powerUpShells, powerUpSize)
            blueShellUnlocked = True

        for powerUp in powerUpShells[:]:
            windowSurface.blit(powerUpImages[powerUp['type']], (powerUp['rect'].x, powerUp['rect'].y))
            powerUp['rect'].y += powerUpFallSpeed

            if powerUp['rect'].y > WINDOWHEIGHT:
                powerUpShells.remove(powerUp)

            if player.colliderect(powerUp['rect']):
                if powerUp['type'] == 'red':
                    hasRedShell = True
                elif powerUp['type'] == 'blue':
                    hasBlueShell = True
                powerUpShells.remove(powerUp)



        # mid game enemy speed up
        if gameClock >= 15 and timeSwitch == False: 
                hEnemyYSpeed += 0.55
                bEnemyYSpeed += 0.50
                timeSwitch = True

        # move bullets up the screen and draw
        for bullet in bullets[:]:
            bullet.top -= bullSpeed
            if bullet.y < 0:
                bullets.remove(bullet)
            #pygame.draw.rect(windowSurface, WHITE, bullet)
            windowSurface.blit(bulletImg, (bullet.x-20,  bullet.y-20))

        # Code for moving and drawing green shells
        for shell in greenShells[:]:
            # Moving the shell based on direction
            if shell['dir'] == 'left':
                shell['rect'].x -= greenShellSpeed * 0.7071  # cos(45°)
                shell['rect'].y -= greenShellSpeed * 0.7071  # sin(45°)
            elif shell['dir'] == 'right':
                shell['rect'].x += greenShellSpeed * 0.7071  # cos(45°)
                shell['rect'].y -= greenShellSpeed * 0.7071  # sin(45°)

            # Check for wall collisions to make shells bounce
            if shell['rect'].x <= 0:
                shell['rect'].x = 0  
                shell['dir'] = 'right'  # Reverse direction
            elif shell['rect'].x >= WINDOWWIDTH - greenShellSize:
                shell['rect'].x = WINDOWWIDTH - greenShellSize 
                shell['dir'] = 'left'  # Reverse direction

            # Drawing the shell
            windowSurface.blit(greenShellImg, (shell['rect'].x, shell['rect'].y))

            # Remove shells that go off screen
            if shell['rect'].y < 0 or shell['rect'].x < 0 or shell['rect'].x > WINDOWWIDTH:
                greenShells.remove(shell)

        # draw player
        #pygame.draw.rect(windowSurface, WHITE, player)
        if playerFaceRight:
            windowSurface.blit(marioRight, (player.x-40, player.y-20))
        else: windowSurface.blit(marioLeft, (player.x-40, player.y-20)) #centering img

        # draw the bEnemies
        for enemy in bEnemies[:]:
            #pygame.draw.rect(windowSurface, GREEN, enemy)
            windowSurface.blit(bEnemyImg, (enemy.x-30, enemy.y-20))

        # draw the hEnemies
        for enemy in hEnemies[:]:
            #pygame.draw.rect(windowSurface, RED, enemy)
            windowSurface.blit(hEnemyImg, (enemy.x-20, enemy.y-20))

        # draw the fruits and move down screen
        for fruit in fruits[:]:
            fruit.top += MOVESPEED/2
            if fruit.y > WINDOWHEIGHT:
                fruits.remove(fruit)
            #pygame.draw.rect(windowSurface, WHITE, fruit)
            windowSurface.blit(foodImg, (fruit.x-playerSize//2, fruit.y))

            #player fruit collision check
            if player.colliderect(fruit):
                score += fruitPoints
                fruits.remove(fruit)
                if musicPlaying:
                    pickUpSound.play()

        # display text 
        pointsDisplay = FONT.render(f'Points: {score}', True, WHITE)
        windowSurface.blit(pointsDisplay, (50, WINDOWHEIGHT-50))

        # draw the window on the screen
        pygame.display.update()
        mainClock.tick(40)
        gameClock += 1/40

        # end game loop when no more enemies or fruits
        if not fruits and not bEnemies and not hEnemies: 
            gameLoop = False
            win = True
            return score, win
        
def Lvl5WinScreen(score):
    gameLoop = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('menu.wav') 
    pygame.mixer.music.play(-1, start=26)#LOAD BACKGROUND MUSIC
    currentKart = 0
    # GAME LOOP
    while gameLoop:
        # EVENT CHECKS
        for event in pygame.event.get():
            # quit event
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_s:
                    gameLoop = False
                    return currentKart
                if event.key == K_LEFT and currentKart > 0: currentKart -= 1; selectSound.play()
                if event.key == K_RIGHT and currentKart < 2: currentKart += 1; selectSound.play()
            
        # widnow fill
        windowSurface.fill(BLACK)

        # load menu image
        lvl1Img = pygame.image.load('gameComplete.png')
        lvl1Img = pygame.transform.scale(lvl1Img, (WINDOWWIDTH, WINDOWHEIGHT))
        windowSurface.blit(lvl1Img, (0, 0))

        # text display
        if win:
            line1 = FONT.render(f'Well done! You killed all the enemies and got {score} points', True, WHITE)
        line2 = FONT.render(f'The world is saved, thank you hero!', True, WHITE)
        line3 = FONT.render(f'Now you can spend your time racing carts', True, WHITE)
        line4 = FONT.render(f'Thanks for playing!', True, WHITE)
        line5 = FONT.render(f'Credits', True, WHITE)
        line6 = FONT.render(f'-------', True, WHITE)
        line7 = FONT.render(f'Game Dev: Aidan Lynch, Mac Padilla, Quentin Wingard', True, WHITE)
        line8 = FONT.render(f'Playtesting: Abigail Trautman, Dylan Moore, Geran Benson', True, WHITE)
        windowSurface.blit(line1, (100, 220))
        windowSurface.blit(line2, (100, 270))
        windowSurface.blit(line3, (100, 320))
        windowSurface.blit(line4, (100, 370))
        windowSurface.blit(line5, (100, 420))
        windowSurface.blit(line6, (100, 470))
        windowSurface.blit(line7, (100, 520))
        windowSurface.blit(line8, (100, 570))

        pygame.display.update()
        mainClock.tick(40)

welcomeScreen()
score, win = lvl1(score)
win = True
if win == True:
    currentKart = Lvl1WinScreen(score)
else:
    gameOverScreen()
score, win = lvl2(score, currentKart)
if win == True:
    Lvl3WinScreen(score)
else:
    gameOverScreen()
score, win = lvl3(score)
if win == True:
    Lvl2WinScreen(score)
else:
    gameOverScreen()
score, win = lvl4(score)
if win == True:
    Lvl5WinScreen(score)
else:
    gameOverScreen()