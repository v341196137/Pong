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

pygame.init() # start the hell

########## INITIALIZATION FUNCTIONS ##########
def loadImage(imageName):
    return pygame.image.load("/assets/pictures/"+imageName).convert()

def loadTransparentImage(imageName):
    return pygame.image.load("/assets/pictures/"+imageName).convert_alpha()

def createFont(font, size):
    return pygame.font.SysFont(font, size)
##############################################

########## VARIABLES ##########
paddleSize = 100
player1Score = 0
player2Score = 0
player1Pos = 300 - (paddleSize/2)
player2Pos = 300 - (paddleSize/2)
player1Direction = 0
player2Direction = 0
ballSize = 50
ballX = 400 - (ballSize/2)
ballY = 300 - (ballSize/2)
ballSpeed = 1
angle = random.random()*3
ballDirY = randrange(-1, 2, 2)
ballDirX = randrange(-1, 2, 2)
r = 255
g = 0
b = 0
dr = 0
dg = 1
db = 0
month, day = datetime.datetime.now().month, datetime.datetime.now().day
comicSans = pygame.font.SysFont("Comic Sans MS", 20)
buttonComicSans = pygame.font.SysFont("Comic Sans MS", 30)
titleComicSans = pygame.font.SysFont("Comic Sans MS", 60)
gameMode = "menu"
theme = ""
ballImage = 0
paddleImage = 0
screen = pygame.display.set_mode((800, 600))

########## VARIABLES ##########

#create the theme
if (month == 4) and (day == 1):
    theme = "aprfools"
elif (month == 9) and (day == 20):
    theme = "joseph"
    ballImage = loadTransparentImage("thonk.gif")
    paddleImage = loadImage("creeper.png")
elif (month == 10) and (day == 31):
    theme = "halloween"
    ballImage = loadTransparentImage("halloweenBall.png")
    paddleImage = loadTransparentImage("bone.png")
elif (month == 12) and (day == 25):
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
def startGame(ballX, ballY, ballSpeed, angle):
    ballX = 400 - (ballSize/2)
    ballY = 300 - (ballSize/2)
    ballSpeed = 1
    angle = random.random()*3
    return ballX, ballY, ballSpeed, angle

########## FUNCTIONS ##########

########## GAME ##########
#start the game
ballX, ballY, ballSpeed, angle = startGame(ballX, ballY, ballSpeed, angle)
inPlay = True

while inPlay:
    #fill screen based on theme
    if (theme == "default") or (theme == "joseph") or (theme == "halloween"):
        screen.fill((0, 0, 0))
    elif (theme == "aprfools"):
        screen.fill((255 - r, 255 - g, 255 -b))
    elif (theme == "christmas"):
        screen.fill((200, 230, 255))

    #handle i/o, different i/o based on mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if gameMode == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (mouseX >= 300) and (mouseX <= 500):
                    if (mouseY >= 200) and (mouseY <= 250):
                        gameMode = "game"
                    elif (mouseY >= 270) and (mouseY <= 320):
                        gameMode = "instructions"
        elif gameMode == "instructions":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (mouseX >= 0) and (mouseX <= 60) and (mouseY >= 0) and (mouseY <= 40):
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
        screen.blit(title, (325, 20))
        play = buttonComicSans.render("Play!", 0, (r, g, b))
        screen.blit(play, (360, 200))
        instructions = buttonComicSans.render("How to play", 0, (r, g, b))
        screen.blit(instructions, (320, 270))
        #button outlines
        for yPos in range(200, 300, 70):
            pygame.draw.rect(screen, (r, g, b), (300, yPos, 200, 50), 1)
    elif gameMode == "instruction":
        #buttons
        backButton = comicSans.render("Back", 0, (r, g, b))
        screen.blit(backButton, (5, 0))
        pygame.draw.rect(screen, (r, g, b), (0, 0, 60, 40), 1)
    elif gameMode == "game":
        #ball movement
        ballX += ballSpeed*ballDirX
        ballY += angle*ballDirY
        #ball bounce
        if ballY <= 0 or ballY >= 600-ballSize:
            ballDirY *= -1
        #score points
        if ballX <= 0:
            player2Score += 1
            ballX, ballY, ballSpeed, angle = startGame(ballX, ballY, ballSpeed, angle)
        elif ballX >= 800-ballSize:
            player1Score += 1
            ballX, ballY, ballSpeed, angle = startGame(ballX, ballY, ballSpeed, angle)

        #recieve ball
        if (abs(ballX - 60 <= ballSpeed)) and (ballY + ballSize >= player1Pos) and (ballY <= player1Pos + paddleSize):
            ballDirX = 1
            angle = ((ballY - (player1Pos + (paddleSize/2)))/paddleSize)*3
        elif (abs(720 - ballSize - ballX <= ballSpeed)) and (ballY + ballSize >= player2Pos) and (ballY <= player2Pos + paddleSize):
            ballDirX = -1
            angle = ((ballY - (player2Pos + (paddleSize/2)))/paddleSize)*3

        #update player positions
        if (player1Pos > 0 and player1Pos < 600 - paddleSize) or (player1Pos <= 0 and player1Direction == 1) or (player1Pos >= 600 - paddleSize and player1Direction == -1):
            player1Pos += player1Direction
        if (player2Pos > 0 and player2Pos < 600 - paddleSize) or (player2Pos <= 0 and player2Direction == 1) or (player2Pos >= 600 - paddleSize and player2Direction == -1):
            player2Pos += player2Direction

        #score check
        score = comicSans.render("Score\n" + str(player1Score) + ":" + str(player2Score), 0, (r, g, b))
        screen. blit(score, (350, 0))
        if (player1Score == 7) or (player2Score == 7):
            gameMode = "winScreen"
        #draw stuff based on theme assigned by date
        if (theme == "default") or (theme == "aprfools"):
            pygame.draw.ellipse(screen, (r, g, b), (ballX, ballY, ballSize, ballSize), 1)
            pygame.draw.rect(screen, (r, g, b), (40, player1Pos, 20, paddleSize), 1)
            pygame.draw.rect(screen, (r, g, b), (720, player2Pos, 20, paddleSize), 1)
        else:
            screen.blit(ballImage, (ballX, ballY))
            screen.blit(paddleImage, (40, player1Pos))
            screen.blit(paddleImage, (720, player2Pos))
    elif gameMode == "winScreen":
        if player1Score == 7:
            winMessage = comicSans.render("Player 1 wins!", 0, (r, g, b))
            screen.blit(winMessage, (325, 270))
        else:
            winMessage = comicSans.render("Player 2 wins!", 0, (r, g, b))
            screen.blit(winMessage, (325, 270))
        playAgainMessage = comicSans.render("Click anywhere or any  key to return to the main menu", 0, (r, g, b))
        screen.blit(playAgainMessage, (150, 400))
    #change colours
    r+=dr
    g+=dg
    b+=db
    if r>=255 and g>=255:
        dr=-1
        dg=0
        db=0
    elif r>=255 and b>=255:
        dr=0
        dg=0
        db=-1
    elif r>=255 and b==0:
        dr=0
        dg=1
        db=0
    elif g>=255 and b>=255:
        dr=0
        dg=-1
        db=0
    elif g>=255 and r==0:
        dr=0
        dg=0
        db=1
    elif b>=255 and g==0:
        dr=1
        dg=0
        db=0
    
    #draw over
    pygame.display.update()
    pygame.display.flip()
########## GAME ##########
pygame.quit()