# Pong
# Gamers
# March 30, 2020
# Python is wack

# Imports
import pygame
import sys
import random
import datetime
import time
from random import randrange, randint

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # start the hell

########## CONSTS ##########
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_PADDLE_SIZE = 100
DEFAULT_BALL_SIZE = 50
MIN_HEIGHT = 300
MAX_HEIGHT = 1080
BALL_SPEED_INCREASE = 240000

BLACK = (0, 0, 0)

ONE_SECOND = 1000
THREE_SECONDS = 3000

SLIDER_LENGTH = 200
SLIDER_HEIGHT = 2
############################

screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))

########## INITIALIZATION FUNCTIONS ##########
def loadImage(imageName):
    return pygame.image.load("./assets/pictures/"+imageName).convert()

def loadTransparentImage(imageName):
    return pygame.image.load("./assets/pictures/"+imageName).convert_alpha()

def loadSFX(soundEffectName): #load a sfx from the folder
    sound = pygame.mixer.Sound("./assets/sfx/"+soundEffectName)
    sound.set_volume(0.5)
    return sound

def createFont(font, size):
    return pygame.font.SysFont(font, int(size))
##############################################

########## VARIABLES ##########

height = DEFAULT_HEIGHT
width = DEFAULT_WIDTH

comicSans = createFont("Comic Sans MS", height/30)
buttonComicSans = createFont("Comic Sans MS", height/20)
titleComicSans = createFont("Comic Sans MS", height/10)

pauseBackground = loadTransparentImage("pauseScreenBack.png")
gameLogo = loadTransparentImage("gameLogo.png")

paddleSize1 = DEFAULT_PADDLE_SIZE
paddleSize2 = DEFAULT_PADDLE_SIZE
ballSize = DEFAULT_BALL_SIZE

player1Pos = (height/2) - (DEFAULT_PADDLE_SIZE/2)
player2Pos = (height/2) - (DEFAULT_PADDLE_SIZE/2)
player1Direction = 0
player2Direction = 0

ballDirY = randrange(-1, 2, 2)
ballDirX = randrange(-1, 2, 2)

cheatUsed = False
cheatInEffect = False

r = 255
g = 0
b = 0
dr = 0
dg = 1
db = 0

rules = ["Welcome to Pong!", "Player 1 uses W and S to move the paddle up and down", 
        "Player 2 uses I and K to move the paddle up and down", "Player 1 can also use Q as a cheat key", 
        "Press the escape key in game to pause game", "First to 7 wins the game", "Good luck!"]

month, day = datetime.datetime.now().month, datetime.datetime.now().day
lastTime = 0
curTime = 0

player1Score = 0
player2Score = 0

rgbMod = 1

soundEffects = True
playMusic = True

ballImage, paddleImage, iceImage = None, None, None
hitSound, pointSound = None, None
bgMusic = None
ballX, ballY, ballSpeed, angle = 0, 0, 0, 0

onSlider = False

grigorovMode = False

pygame.display.set_caption("Pong")
pygame.display.set_icon(gameLogo)
###############################

#create the theme
theme = ""
if month == 4 and day == 1:
    theme = "aprfools"
    bgMusic = "Blursed Kahoot.ogg"
elif month == 9 and day == 20:
    theme = "joseph"
    ballImage = loadTransparentImage("thonk.gif")
    paddleImage = loadImage("creeper.png")
    bgMusic = "Kahoot.ogg"
elif month == 10 and day == 31:
    theme = "halloween"
    ballImage = loadTransparentImage("halloweenBall.png")
    paddleImage = loadTransparentImage("bone.png")
    bgMusic = "Spooky Scary Skeletons (DRYPAPER Remix).ogg"
elif month == 12 and day == 25:
    theme = "christmas"
    ballImage = loadTransparentImage("christmasBall.png")
    paddleImage = loadTransparentImage("christmasPaddle.png")
    iceImage = loadTransparentImage("ice.png")
    bgMusic = "Carol of the Bells.ogg"
elif grigorovMode:
    theme = "grigorov"
    ballImage = loadTransparentImage("basketball.png")
    paddleImage = loadTransparentImage("resistor.png")
    bgMusic = "Tetris 99 - Main Theme.ogg"
else:
    theme = "default"
########## FUNCTIONS ##########

# startGame
# @param ballX, reset x position of the ball back to the middle
# @param ballY, resets y position of the ball back to the middle
# @param ballSpeed, puts the ball's speed back to 1
# @param angle, generates a random angle for the ball
# @return returns all the values back to be reassigned because global variables are bad
def resetGame():
    newBallX = (height*2/3) - (ballSize/2)
    newBallY = (height/2) - (ballSize/2)
    newBallSpeed = float(height)/600
    newAngle = random.random()*(height/200)

    return newBallX, newBallY, newBallSpeed, newAngle

def drawFakeLoadScreen(screen, r, g, b):
    if playMusic:
        pygame.mixer.music.set_volume(0.1)

    pygame.draw.rect(screen, (r, g, b), (height/2, height/3, height/3, height/20), 1)
    for i in range(2000):
        pygame.draw.rect(screen, (r, g, b), (height/2, height/3, height*i/6000, height/20), 0)
        pygame.display.update()

def determineSFX(theme): 
    # You can use this to determine whawt the sfx should be according to the theme
    # for now it just returns the default
    newHitSound = loadSFX("defaultHit1.wav")
    newPointSound = loadSFX("defaultPoint1.wav")
    return newHitSound, newPointSound

### thanks Despongoncito 3 and Kevin for this code
def generateCenteredText(x, y, text, font, colour):
    textSize = font.size(text)
    renderedText = font.render(text, 1, colour)
    textX = x-textSize[0]/2
    textY = y-textSize[1]/2
    return renderedText, (textX, textY)
###

def generateText(x, y, text, font, colour):
    #make drawing precise text neater and nicer
    return font.render(text, 1, colour), (x, y)

def mouseIsIn(mousePos, topLeftPoint, bottomRightPoint):
    #those all have to be tuples, determines if the mouse is within a range of points.
    if ((mousePos[0] >= topLeftPoint[0]) and (mousePos[0] <= bottomRightPoint[0]) 
    and (mousePos[1] >= topLeftPoint[1]) and (mousePos[1] <= bottomRightPoint[1])):
        return True
    
    return False

def clampValue(val, minimum, maximum):
    if val < minimum:
        val = minimum
    if val > maximum:
        val = maximum

    return val

def cycleRGB(dr, dg, db, r, g, b, mod):
    r += (dr * mod)
    g += (dg * mod)
    b += (db * mod)

    r = clampValue(r, 0, 255)
    g = clampValue(g, 0, 255)
    b = clampValue(b, 0, 255)
    
    if r >= 255 and g >= 255:
        dr = -1
        dg = 0
        db = 0
    elif r >= 255 and b >= 255:
        dr = 0
        dg = 0
        db = -1
    elif r >= 255 and b == 0:
        dr = 0
        dg = 1
        db = 0
    elif g >= 255 and b >= 255:
        dr = 0
        dg = -1
        db = 0
    elif g >= 255 and r== 0:
        dr = 0
        dg = 0
        db = 1
    elif b >= 255 and g == 0:
        dr = 1
        dg = 0
        db = 0

    return dr, dg, db, r, g, b


def loadMusic(music):
    pygame.mixer.music.load("assets/music/" + music)
    pygame.mixer.music.play(-1)

########## FUNCTIONS ##########

########## GAME ##########
#start the game
gameMode = "menu"
hitSound, pointSound = determineSFX(theme)
ballX, ballY, ballSpeed, angle = resetGame()
inPlay = True

if bgMusic:
    loadMusic(bgMusic)

pygame.mixer.music.set_volume(0.7)

while inPlay:
    #fill screen based on theme
    if not cheatInEffect:
        if theme == "default" or theme == "joseph" or theme == "halloween":
            screen.fill((0, 0, 0))
        elif theme == "aprfools":
            screen.fill((255 - r, 255 - g, 255 -b))
        elif theme == "christmas":
            screen.fill((200, 230, 255))
        elif theme == "grigorov":
            screen.fill((255, 255, 255))
    
    else:
        screen.fill((255 - r, 255 - g, 255 -b))
        cr = clampValue(r, 1, 200)
        cg = clampValue(r, 1, 200)
        cb = clampValue(r, 1, 200)
        for i in range(8):
            pygame.draw.rect(screen, (200 - cr, 200 - cg, 200 - cb), (randint(50, width), randint(1, height), randint(25, 500), randint(25, 500)), 1)
        screen.blit(*generateCenteredText(width/2, height/2, "CHEAT ACTIVATED", titleComicSans, (r, g, b)))

    #handle i/o, different i/o based on mode
    for event in pygame.event.get():
        if gameMode != "game":
            mouse = pygame.mouse.get_pos()
            mouseX, mouseY = mouse

        if event.type == pygame.QUIT:
            inPlay = False
        if gameMode == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseIsIn(mouse, (height/2, height/3), 
                                    (height*5/6, height*5/12)):
                    player1Direction, player2Direction = 0, 0
                    player1Score, player2Score = 0, 0
                    cheatUsed, cheatInEffect = False, False
                    drawFakeLoadScreen(screen, r, g, b)
                    gameMode = "game"
                elif mouseIsIn(mouse, (height/2, height*9/20), 
                                      (height*5/6, height*8/15)):
                    gameMode = "instructions"
                elif mouseIsIn(mouse, (height/2, height*17/30), 
                                      (height*5/6, height*13/20)):
                    gameMode = "settings"
                elif mouseIsIn(mouse, (height/2,height*41/60), 
                                      (height*5/6, height*23/30)):
                    gameMode = "credits"

        elif gameMode == "instructions":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseIsIn(mouse, (0, 0), (height/10, height/15)):
                    gameMode = "menu"
                elif mouseIsIn(mouse, (height, height*7/8), (height*13/10, (height*7/8) + (height/15))):
                    drawFakeLoadScreen(screen, r, g, b)
                    gameMode = "game"

        elif gameMode == "settings":
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if mouseIsIn(mouse, (0, 0), (height/10, height/15)):
                    gameMode = "menu"
                elif mouseIsIn(mouse, (height/5, height*3/5),
                                      (height/5 + height/7, height*3/5 + height/20)):
                    soundEffects = not soundEffects
                elif mouseIsIn(mouse, (height/5, height*7/10),
                                      (height/5 + height/7, height*7/10 + height/20)):
                    playMusic = not playMusic
                elif mouseIsIn(mouse, (height/10, (height/3) - (SLIDER_HEIGHT*5)), (height/10 + SLIDER_LENGTH, height/3 + (SLIDER_HEIGHT*5))):
                    onSlider = True

            if (event.type == pygame.MOUSEMOTION) and (onSlider):
                mouseX, mouseY = pygame.mouse.get_pos()
                height = (mouseX - height/10)*(MAX_HEIGHT - MIN_HEIGHT)/SLIDER_LENGTH + MIN_HEIGHT
                screen = pygame.display.set_mode((int(height*4/3), int(height)))
                comicSans = createFont("Comic Sans MS", height/30)
                buttonComicSans = createFont("Comic Sans MS", height/20)
                titleComicSans = createFont("Comic Sans MS", height/10)
                paddleSize1 = height/6
                paddleSize2 = height/6
                ballSize = height/12
                player1Pos = (height/2) - (paddleSize1/2)
                player2Pos = (height/2) - (paddleSize2/2)
            if (onSlider) and (event.type == pygame.MOUSEBUTTONUP):
                onSlider = False

        elif gameMode == "credits":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseIsIn(mouse, (0, 0), (height/10, height/15)):
                    gameMode = "menu"

        elif gameMode == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1Direction = -1
                elif event.key == pygame.K_s:
                    player1Direction = 1
                elif event.key == pygame.K_i:
                    player2Direction = -1
                elif event.key == pygame.K_k:
                    player2Direction = 1
                elif event.key == pygame.K_ESCAPE:
                    gameMode = "pause"
                elif (event.key == pygame.K_q) and (not cheatUsed):
                    cheatUsed = True
                    cheatInEffect = True
                    rgbMod = 7
                    if theme == "christmas":
                        lastTime = time.time()*ONE_SECOND
                        curTime = time.time()*ONE_SECOND
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_w) or (event.key == pygame.K_s):
                    player1Direction = 0
                elif (event.key == pygame.K_i) or (event.key == pygame.K_k):
                    player2Direction = 0
        elif gameMode == "winScreen":
            gameMode = "menu"
        elif gameMode == "pause":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameMode = "menu"
                elif event.key == pygame.K_RETURN:
                    gameMode = "game"

    if gameMode == "menu":
        #text
        screen.blit(*generateCenteredText(width/2, 50, "Pong!", titleComicSans, (r, g, b)))
        screen.blit(*generateText(height*3/5    , height/3      , "Play!", buttonComicSans, (r, g, b)))
        screen.blit(*generateText(height*320/600, height*270/600, "How to play", buttonComicSans, (r, g, b)))
        screen.blit(*generateText(height*340/600, height*340/600, "Settings", buttonComicSans, (r, g, b)))
        screen.blit(*generateText(height*350/600, height*410/600, "Credits", buttonComicSans, (r, g, b)))
        #button outlines
        for yPos in range(int(height*200/600), int(height*420/600), int(height*70/600)):
            pygame.draw.rect(screen, (r, g, b), (height/2, yPos, height/3, height/12), 1)

    elif gameMode == "instructions":
        #draw buttons
        screen.blit(*generateText(height/120, 0, "Back", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (0, 0, height/10, height/15), 1)
        screen.blit(*generateText(height*121/120, height*7/8, "Continue to Game!", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (height, height*7/8, height*3/10, height/15), 1)

        #text for the actual instructions
        for i in range(len(rules)):
            screen.blit(*generateText(height/60, (height*i/20) + (height/10), rules[i], comicSans, (r, g, b)))
        
    elif gameMode == "settings":
        #back button
        screen.blit(*generateText(height/120, 0, "Back", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (0, 0, height/10, height/15), 1)

        #screen size adjustment
        screen.blit(*generateText(height/10, height/10, "Screen size:", comicSans, (r, g, b)))
        curScreenSize = comicSans.render(str(height*4/3)+" X "+str(height), 0, (r, g, b))
        screen.blit(curScreenSize, (height/10, height/5))
        pygame.draw.rect(screen, (r, g, b), (height/10, height/3, SLIDER_LENGTH, SLIDER_HEIGHT), 0)
        pygame.draw.rect(screen, (r, g, b), ((height/10) + ((height - MIN_HEIGHT)*SLIDER_LENGTH/(MAX_HEIGHT - MIN_HEIGHT)), height/3 - (SLIDER_HEIGHT*5), SLIDER_HEIGHT*5, SLIDER_HEIGHT*10), 0)
        
        #toggles for sfx and music
        screen.blit(*generateText(height/15, height*3/5, "SFX:", comicSans, (r, g, b)))
        screen.blit(*generateText(height/15, height*7/10, "Music:", comicSans, (r, g, b)))

        # on/off sliders
        screen.blit(*generateText(height/5, height*3/5, "ON OFF", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (height/5, height*3/5, height/7, height/20), 1)
        screen.blit(*generateText(height/5, height*7/10, "ON OFF", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (height/5, height*7/10, height/7, height/20), 1)

        if soundEffects:
            pygame.draw.rect(screen, (r, g, b), (height*13/50, height*3/5, height/12, height/20), 0)
        else:
            pygame.draw.rect(screen, (r, g, b), (height/5, height*3/5, height/15, height/20), 0)
        if playMusic:
            pygame.mixer.music.set_volume(0.7)
            pygame.draw.rect(screen, (r, g, b), (height*13/50, height*7/10, height/12, height/20), 0)
        else:
            pygame.mixer.music.set_volume(0)
            pygame.draw.rect(screen, (r, g, b), (height/5, height*7/10, height/15, height/20), 0)

    elif gameMode == "credits":
        #back button
        screen.blit(*generateText(height/120, 0, "Back", comicSans, (r, g, b)))
        pygame.draw.rect(screen, (r, g, b), (0, 0, height/10, height/15), 1)
        #Actual credits
        screen.blit(*generateCenteredText(width/2, 50, "Due Date: Mr. Grigorov", comicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, 100, "Basically all the code: Vivian", comicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, 150, "Music: The internet", comicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, 200, "sfx and morale encouragement: Joseph", comicSans, (r, g, b)))
    elif gameMode == "game":
        if playMusic:
            pygame.mixer.music.set_volume(0.7)
        #cheats are fun
        if cheatInEffect:
            if theme == "joseph":
                ballSize = height/24
            elif theme == "halloween":
                ballX += (ballSpeed*ballDirX)*2
            elif theme == "christmas":
                ballX -= ballSpeed*ballDirX
                ballY -= angle*ballDirY
                curTime = time.time()*1000
                if curTime - lastTime > THREE_SECONDS:
                    cheatInEffect = False
                    rgbMod = 1
            elif theme == "grigorov":
                paddleSize1 = paddleSize2*2
            else:
                paddleSize2 = paddleSize1*1/4
        #ball movement
        ballX += ballSpeed*ballDirX
        ballY += angle*ballDirY
        #ball bounce
        if ballY <= 0 or ballY >= height-ballSize:
            ballDirY *= -1
        #score points
        if ballX <= 0:
            player2Score += 1
            ballX, ballY, ballSpeed, angle = resetGame()
            if soundEffects:
                pointSound.play()
        elif ballX >= (height*4/3)-ballSize:
            player1Score += 1
            ballX, ballY, ballSpeed, angle = resetGame()
            if soundEffects:
                pointSound.play()
            #reset the cheat after scoring a point
            cheatInEffect = False
            rgbMod = 1

            if theme == "joseph":
                ballSize = height/12
            elif theme == "grigorov":
                paddleSize1 = paddleSize2
            else:
                paddleSize2 = paddleSize1

        #recieve ball
        if (abs(ballX - (height/10) <= ballSpeed)) and (ballY + ballSize >= player1Pos) and (ballY <= player1Pos + paddleSize1):
            ballDirX = 1
            angle = abs((((ballY + ballSize) - (player1Pos + (paddleSize1/2)))/paddleSize1)*(height/200))
            if (ballY + ballSize) - (player1Pos + (paddleSize1/2)) > 0:
                ballDirY = 1
            else:
                ballDirY = -1
            if soundEffects:
                hitSound.play()
        elif (abs((height*6/5) - ballSize - ballX <= ballSpeed)) and (ballY + ballSize >= player2Pos) and (ballY <= player2Pos + paddleSize2):
            ballDirX = -1
            angle = abs((((ballY + ballSize)- (player2Pos + (paddleSize2/2)))/paddleSize2)*(height/200))
            if (ballY + ballSize) - (player1Pos + (paddleSize2/2)) > 0:
                ballDirY = 1
            else:
                ballDirY = -1
            if soundEffects:
                hitSound.play()

        #update player positions
        if (player1Pos > 0 and player1Pos < height - paddleSize1) or (player1Pos <= 0 and player1Direction == 1) or (player1Pos >= height - paddleSize1 and player1Direction == -1):
            player1Pos += player1Direction * (height/300)
        if (player2Pos > 0 and player2Pos < height - paddleSize2) or (player2Pos <= 0 and player2Direction == 1) or (player2Pos >= height - paddleSize2 and player2Direction == -1):
            player2Pos += player2Direction * (height/300)

        #score check
        screen.blit(*generateCenteredText(width/2, 25, "Score: " + str(player1Score) + "-" + str(player2Score), comicSans, (r, g, b)))
        if (player1Score == 7) or (player2Score == 7):
            gameMode = "winScreen"

        #draw stuff based on theme assigned by date
        if (theme == "default" or theme == "aprfools") or (ballImage == None or paddleImage == None):
            if (ballImage == None or paddleImage == None) and (theme != "default" and theme != "aprfools"):
                print("Had trouble loading a ball or paddle image.")
            if not((theme == "aprfools") and (cheatInEffect)):
                pygame.draw.ellipse(screen, (r, g, b), (ballX, ballY, ballSize, ballSize), 1)
            pygame.draw.rect(screen, (r, g, b), (height/15, player1Pos, height/30, paddleSize1), 1)
            pygame.draw.rect(screen, (r, g, b), (height*6/5, player2Pos, height/30, paddleSize2), 1)
        else:
            if (theme == "christmas") and (cheatInEffect):
                screen.blit(pygame.transform.scale(iceImage, (int(ballSize), int(ballSize))), (ballX, ballY))
            else:
                screen.blit(pygame.transform.scale(ballImage, (int(ballSize), int(ballSize))), (ballX, ballY))
            screen.blit(pygame.transform.scale(paddleImage, (int(height/30), int(paddleSize1))), (int(height/15), player1Pos))
            screen.blit(pygame.transform.scale(pygame.transform.flip(paddleImage, True, False), (int(height/30), paddleSize2)), (int(height*6/5), player2Pos))
        #slow increase in ball speed
        ballSpeed += float(height)/BALL_SPEED_INCREASE
    elif gameMode == "winScreen":
        if player1Score == 7:
            screen.blit(*generateCenteredText(width/2, 150, "Player 1 wins!", titleComicSans, (r, g, b)))
        else:
            screen.blit(*generateCenteredText(width/2, 150, "Player 2 wins!", titleComicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, height - 150, "Click anywhere or any  key to return to the main menu", comicSans, (r, g, b)))

    elif gameMode == "pause":
        if playMusic:
            pygame.mixer.music.set_volume(0.3)
        if (theme == "default" or theme == "aprfools") or (ballImage == None or paddleImage == None): #draw the old paddle and stuff
            if (ballImage == None or paddleImage == None) and (theme != "default" and theme != "aprfools"):
                print("Had trouble loading a ball or paddle image.")
            if not((theme == "aprfools") and (cheatInEffect)):
                pygame.draw.ellipse(screen, (r, g, b), (ballX, ballY, ballSize, ballSize), 1)
            pygame.draw.rect(screen, (r, g, b), (height/15, player1Pos, height/30, paddleSize1), 1)
            pygame.draw.rect(screen, (r, g, b), (height*6/5, player2Pos, height/30, paddleSize2), 1)
        else:
            if (theme == "christmas") and (cheatInEffect):
                screen.blit(pygame.transform.scale(iceImage, (int(ballSize), int(ballSize))), (ballX, ballY))
            else:
                screen.blit(pygame.transform.scale(ballImage, (int(ballSize), int(ballSize))), (ballX, ballY))
            screen.blit(pygame.transform.scale(paddleImage, (int(height/30), paddleSize1)), (int(height/15), player1Pos))
            screen.blit(pygame.transform.scale(pygame.transform.flip(paddleImage, True, False), (int(height/30), paddleSize2)), (int(height*6/5), player2Pos))

        screen.blit(pauseBackground, (0, 0)) #transparent background is cool
        screen.blit(*generateCenteredText(width/2, 50, "PAUSED", titleComicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, 150, "Press Enter to return", comicSans, (r, g, b)))
        screen.blit(*generateCenteredText(width/2, 200, "Press Esc to return to menu", comicSans, (r, g, b)))
    #change colours
    dr, dg, db, r, g, b = cycleRGB(dr, dg, db, r, g, b, rgbMod)

    #draw over
    pygame.display.update()
    pygame.display.flip()
########## GAME ##########
pygame.quit()