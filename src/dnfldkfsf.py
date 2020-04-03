# Pong
# Gamers
# March 30, 2020
# Python is wack

# Imports
import pygame
import sys
import random
import datetime
from random import randrange

pygame.init()  # start the hell

########## CONSTS ##########
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_PADDLE_SIZE = 100
DEFAULT_BALL_SIZE = 50
############################

screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))

########## INITIALIZATION FUNCTIONS ##########
def loadImage(imageName):
    return pygame.image.load("/assets/pictures/"+imageName).convert()

def loadTransparentImage(imageName):
    return pygame.image.load("/assets/pictures/"+imageName).convert_alpha()

def createFont(font, size):
    return pygame.font.SysFont(font, int(size))
##############################################

########## VARIABLES ##########

height = DEFAULT_HEIGHT

comicSans = createFont("Comic Sans MS", height/30)
buttonComicSans = createFont("Comic Sans MS", height/20)
titleComicSans = createFont("Comic Sans MS", height/10)

paddleSize = DEFAULT_PADDLE_SIZE
ballSize = DEFAULT_BALL_SIZE

player1Pos = (height/2) - (paddleSize/2)
player2Pos = (height/2) - (paddleSize/2)
player1Direction = 0
player2Direction = 0

ballDirY = randrange(-1, 2, 2)
ballDirX = randrange(-1, 2, 2)
r = 255
g = 0
b = 0
dr = 0
dg = 1
db = 0
month, day = datetime.datetime.now().month, datetime.datetime.now().day

player1Score = 0
player2Score = 0

ballImage, paddleImage = None, None
ballX, ballY, ballSpeed, angle = 0, 0, 0, 0
###############################

#create the theme
theme = ""
if month == 4 and day == 1:
    theme = "aprfools"
elif month == 9 and day == 20:
    theme = "joseph"
    ballImage = loadTransparentImage("thonk.gif")
    paddleImage = loadImage("creeper.png")
elif month == 10 and day == 31:
    theme = "halloween"
    ballImage = loadTransparentImage("halloweenBall.png")
    paddleImage = loadTransparentImage("bone.png")
elif month == 12 and day == 25:
    theme = "christmas"
    ballImage = loadTransparentImage("christmasBall.png")
    paddleImage = loadTransparentImage("christmasPaddle.png")
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

########## FUNCTIONS ##########

########## GAME ##########
#start the game
gameMode = "menu"
ballX, ballY, ballSpeed, angle = resetGame()
inPlay = True

while inPlay:
    #fill screen based on theme
    if theme == "default" or theme == "joseph" or theme == "halloween":
        screen.fill((0, 0, 0))
    elif theme == "aprfools":
        screen.fill((255 - r, 255 - g, 255 -b))
    elif theme == "christmas":
        screen.fill((200, 230, 255))

    #handle i/o, different i/o based on mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if gameMode == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (mouseX >= height/2) and (mouseX <= height*5/6):
                    if (mouseY >= height/3) and (mouseY <= height*5/12):
                        player1Direction = 0
                        player2Direction = 0
                        player1Score = 0
                        player2Score = 0
                        gameMode = "game"
                    elif (mouseY >= height*9/20) and (mouseY <= height*8/15):
                        gameMode = "instructions"
                    elif (mouseY >= height*17/30) and (mouseY <= height*13/20):
                        gameMode = "settings"
        elif gameMode == "instructions":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (mouseX >= 0) and (mouseX <= height/10) and (mouseY >= 0) and (mouseY <= height/15):
                    gameMode = "menu"
        elif gameMode == "settings":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (mouseX >= 0) and (mouseX <= height/10) and (mouseY >= 0) and (mouseY <= height/15):
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
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_w) or (event.key == pygame.K_s):
                    player1Direction = 0
                elif (event.key == pygame.K_i) or (event.key == pygame.K_k):
                    player2Direction = 0
        elif gameMode == "winScreen":
            gameMode = "menu"

    if gameMode == "menu":
        #text
        title = titleComicSans.render("Pong!", 0, (r, g, b))
        screen.blit(title, (height*13/24, height/30))
        play = buttonComicSans.render("Play!", 0, (r, g, b))
        screen.blit(play, (height*3/5, height/3))
        instructions = buttonComicSans.render("How to play", 0, (r, g, b))
        screen.blit(instructions, (height*320/600, height*270/600))
        settings = buttonComicSans.render("Settings", 0, (r, g, b))
        screen.blit(settings, (height*340/600, height*340/600))
        #button outlines
        for yPos in range(int(height*200/600), int(height*350/600), int(height*70/600)):
            pygame.draw.rect(screen, (r, g, b), (height/2, yPos, height/3, height/12), 1)
    elif gameMode == "instructions":
        #buttons
        backButton = comicSans.render("Back", 0, (r, g, b))
        screen.blit(backButton, (height/120, 0))
        pygame.draw.rect(screen, (r, g, b), (0, 0, height/10, height/15), 1)

    elif gameMode == "settings":
        #back button
        backButton = comicSans.render("Back", 0, (r, g, b))
        screen.blit(backButton, (height/120, 0))
        pygame.draw.rect(screen, (r, g, b), (0, 0, height/10, height/15), 1)
    elif gameMode == "game":
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
        elif ballX >= (height*4/3)-ballSize:
            player1Score += 1
            ballX, ballY, ballSpeed, angle = resetGame()

        #recieve ball
        if (abs(ballX - (height/10) <= ballSpeed)) and (ballY + ballSize >= player1Pos) and (ballY <= player1Pos + paddleSize):
            ballDirX = 1
            angle = (((ballY + ballSize) - (player1Pos + (paddleSize/2)))/paddleSize)*(height/200)
        elif (abs((height*6/5) - ballSize - ballX <= ballSpeed)) and (ballY + ballSize >= player2Pos) and (ballY <= player2Pos + paddleSize):
            ballDirX = -1
            angle = (((ballY + ballSize)- (player2Pos + (paddleSize/2)))/paddleSize)*(height/200)

        #update player positions
        if (player1Pos > 0 and player1Pos < height - paddleSize) or (player1Pos <= 0 and player1Direction == 1) or (player1Pos >= height - paddleSize and player1Direction == -1):
            player1Pos += player1Direction * (height/300)
        if (player2Pos > 0 and player2Pos < height - paddleSize) or (player2Pos <= 0 and player2Direction == 1) or (player2Pos >= height - paddleSize and player2Direction == -1):
            player2Pos += player2Direction * (height/300)

        #score check
        score = comicSans.render("Score\n" + str(player1Score) + ":" + str(player2Score), 0, (r, g, b))
        screen. blit(score, (height*35/60, 0))
        if (player1Score == 7) or (player2Score == 7):
            gameMode = "winScreen"
        #draw stuff based on theme assigned by date
        if (theme == "default" or theme == "aprfools") or (ballImage == None or ballPaddle == None):
            if (ballSpeed == None or ballPaddle == None) and (theme != "default" and theme != "aprfools"):
                print("Had trouble loading a ball or paddle image.")
                
            pygame.draw.ellipse(screen, (r, g, b), (ballX, ballY, ballSize, ballSize), 1)
            pygame.draw.rect(screen, (r, g, b), (height/15, player1Pos, height/30, paddleSize), 1)
            pygame.draw.rect(screen, (r, g, b), (height*6/5, player2Pos, height/30, paddleSize), 1)
        else:
            screen.blit(ballImage, (ballX, ballY))
            screen.blit(paddleImage, (height/15, player1Pos))
            screen.blit(pygame.transform.flip(paddleImage, True, False), (height*6/5, player2Pos))
        #slow increase in ball speed
        ballSpeed += float(height)/240000
    elif gameMode == "winScreen":
        if player1Score == 7:
            winMessage = comicSans.render("Player 1 wins!", 0, (r, g, b))
            screen.blit(winMessage, (height*13/24, height*9/20))
        else:
            winMessage = comicSans.render("Player 2 wins!", 0, (r, g, b))
            screen.blit(winMessage, (height*13/24, height*9/20))
        playAgainMessage = comicSans.render("Click anywhere or any  key to return to the main menu", 0, (r, g, b))
        screen.blit(playAgainMessage, (height/4, height*2/3))
    #change colours
    r += dr
    g += dg
    b += db
    if r >= 255 and g >= 255:
        d = -1
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
    
    #draw over
    pygame.display.update()
    pygame.display.flip()
########## GAME ##########
pygame.quit()