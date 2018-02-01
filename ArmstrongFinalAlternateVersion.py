''' Emily Armstrong
 CSC 383
 Final Project: Maze Game
 The player is trying to find his/her around Ireland through a simple maze.
 In order to win, he/she must collect the 3 pints of Guinness scattered
 across the maze and head to the exit. The player only has 40 seconds to do so.
 If the timer hits 0 before this, the player loses.

 This program is the alternate, harder version of the traditional maze game. The
 player has only 40 seconds instead of 60 to collect the pints and to reach the
 finish line. However, a ricochet effect has been added where the player can
 bounce off of the wall and travel faster than normal. In order to win, the
 must strategize and bounce off of the walls or else he/she will not have enough
 time. 
'''
import pygame, sys
from pygame.locals import *
import time

pygame.init()
# set up music mixer 
pygame.mixer.pre_init(44100, -16, 8, 2048)
pygame.mixer.init()
music = pygame.mixer.Sound('mirorb.ogg')
# set up screen dimensions and colors
display_width = 900
display_height = 675
black = (0,0,0)
white = (255,255,255)
green = (0,50,0)
green2 = (0,150,0)
orange = (255,128,0)
red = (255,0,0)
# list of maze boundary points for drawing
maze_lines = [(580,570),(580,410),(340,410),(340,250),(580,250),(580,90),(420,90),(420,10),
              (660,10),(660,650),(500,650),(500,490)]
maze_lines2 = [(420,650),(100,650),(100,10),(340,10),(340,170),(500,170)]
maze_lines3 = [(100,250),(180,250),(180,90),(260,90),(260,170)]
maze_lines4 = [(180,410),(180,330),(260,330),(260,570),(180,570)]
maze_lines5 = [(340,490),(340,570),(420,570),(420,410)]

# maze outer dimensions
maze_top = 10
maze_bottom = 650
maze_left = 100
maze_right = 660
gameDisplay = pygame.display.set_mode((display_width, display_height), 0, 32)
pygame.display.set_caption('Find your way around Ireland')
clock = pygame.time.Clock()
#load images
bg_img = pygame.image.load('ireland.jpg').convert()
me_img = pygame.image.load('derp.png').convert_alpha()
guinness_img = pygame.image.load('guinness.jpg').convert()

# begin checking for collisions between player and maze lines
# originally created as sprites and rectangle but too many errors arose
# line coordinates calculated and hardcoded here
# organized by units of 80 horizontally and verically
# each nested if represents a line within the same unit

# left collsions
def check_left(x,y,x_change,img_bottom,img_right):

    if x <= maze_left:
        x_change = 4
        # x axis 
    if x <= 180 and img_right > 180:
        # possible vertical lines (y axis)
        if y >= 90 and y <= 250:
            x_change = 4
        elif y >= 330 and y <= 410:
            x_change = 4
    elif x <= 260 and img_right > 260:
        if img_bottom >= 90 and y <= 170:
            x_change = 4
        elif img_bottom >= 330 and y <= 570:
            x_change = 4
    elif x <= 340 and img_right > 340:
        if y >= 10 and img_bottom <= 170:
            x_change = 4
        elif y >= 250 and img_bottom <= 410:
            x_change = 4
        elif img_bottom >= 490 and img_bottom <= 570:
            x_change = 4
    elif x <= 420 and img_right > 420:
        if y >= 10 and img_bottom <= 90:
            x_change = 4
        elif y >= 410 and y <= 570:
            x_change = 4
    elif x <= 500 and img_right > 500:
        if img_bottom >= 490 and img_bottom <= 650:
            x_change = 4
        # not a line; just a point sticking out 
        elif y > 130 and img_bottom < 210:
            x_change = 4
    elif x <= 580 and img_right > 580:
        if img_bottom >= 90 and y <= 250:
            x_change = 4
        elif img_bottom >= 410 and y <= 560:
            x_change = 4
    return x_change

def check_right(x,y,x_change,img_bottom,img_right):
# right collisions 
        if img_right >= maze_right:
            x_change = -4
        elif img_right >= 180 and x < 180:
            if img_bottom >= 90 and img_bottom <= 250:
                x_change = -4
            elif img_bottom >= 330 and y <= 410:
                x_change = -4
            elif img_bottom <= 610 and y >= 530:
                x_change = -4
        elif img_right >= 260 and x < 260:
            if y >= 90 and y <= 170:
                x_change = -4
            elif y >= 210 and img_bottom <= 290:
                x_change = -4
            elif y >= 330 and img_bottom <= 570:
                x_change = -4
        elif img_right >= 340 and x < 340:
            if y >= 10 and y <= 170:
                x_change = -4
            elif y >= 250 and y <= 410:
                x_change = -4
            elif img_bottom >= 490 and y <= 570:
                x_change = -4
        elif img_right >= 420 and x < 420:
            if y >= maze_top and y <= 90:
                x_change = -4
            elif y >= 290 and img_bottom <= 370:
                x_change = -4
            elif y >= 410 and img_bottom <= 570:
                x_change = -4
        elif img_right >= 500 and x < 500:
            if img_bottom >= 490 and img_bottom <= maze_bottom:
                x_change = -4
        elif img_right >= 580 and x < 580:
            if y >= 90 and img_bottom <= 250:
                x_change = -4
            elif y >= 410 and y <= 570:
                x_change = -4
        return x_change

# collisions between top of character and horizontal lines
def check_up(x,y,y_change,img_bottom,img_right):
    if y <= maze_top:
            y_change = 4
    elif y <= 90 and img_bottom > 90:
        if x >= 180 and img_right <= 260:
            y_change = 4
        elif img_right >= 420 and img_right <= 580:
            y_change = 4
    elif y <= 170 and img_bottom > 170:
        if x >= 220 and img_right <= 300:
            y_change = 4
        elif img_right >= 340 and x <= 500:
            y_change = 4
    elif y <= 250 and img_bottom > 250:
        if x >= maze_left and x <= 180:
            y_change = 4
        elif img_right >= 260 and x <= 580:
            y_change = 4
    elif y <= 330 and img_bottom > 330:
        if x >= 180 and img_right <= 260:
            y_change = 4
        elif img_right >= 420 and img_right <= maze_right:
            y_change = 4
    elif y <= 410 and img_bottom > 410:
        if x >= 140 and img_right <= 220:
            y_change = 4
        elif img_right >= 340 and img_right <= 580:
            y_change = 4
    elif y <= 490 and img_bottom > 490:
        if x >= maze_left and img_right <= 260:
            y_change = 4
    elif y <= 570 and img_bottom > 570:
        if img_right >= 180 and x <= 260:
            y_change = 4
        elif img_right >= 340 and x <= 420:
            y_change = 4
        elif x >= 540 and img_right <= 620:
            y_change = 4
    return y_change

# collisions between bottom of character and horizontal lines
def check_down(x,y,y_change,img_bottom,img_right):
    if img_bottom >= maze_bottom:
        y_change = -4   
    elif img_bottom >= 90 and y < 90:
        if img_right >= 180 and x <= 260:
            y_change = -4
        elif x >= 420 and x <= 580:
            y_change = -4
    elif img_bottom >= 170 and y < 170:
        if x >= 340 and x <= 500:
            y_change = -4
    elif img_bottom >= 250 and y < 250:
        if x >= maze_left and img_right <= 180:
            y_change = -4
        elif img_right >= 260 and img_right <= 580:
            y_change = -4
    elif img_bottom >= 330 and y < 330:
        if img_right >= 180 and x <= 260:
            y_change = -4
        elif img_right >= 420 and img_right <= maze_right:
            y_change = -4
    elif img_bottom >= 410 and y < 410:
        if x >= 340 and x <= 580:
            y_change = -4
    elif img_bottom >= 490 and y < 490:
        if x >= maze_left and img_right <= 260:
            y_change = -4
        elif x >= 300 and img_right <= 380:
            y_change = -4
        elif x >= 460 and img_right <= 540:
            y_change = -4
    elif img_bottom >= 570 and y < 570:
        if img_right >= 180 and img_right <= 260:
            y_change = -4
        elif x >= 340 and img_right <= 420:
            y_change = -4
    return y_change

# create text objects
# taken from in class work
def text_objects(text, font, color):
    textSurface = font.render(text,True, color)
    return textSurface, textSurface.get_rect()

# displays message that player finished the game and
# asks if they want to play again
# some coordinates hardcoded, others calculated
def message_display(text):
    while True: 
        largeText=pygame.font.SysFont('Arial',125, True)
        TextSurf, TextRect = text_objects(text, largeText, orange)
        TextRect.center = ((display_width/2),(display_height/8))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.lock()
        pygame.draw.rect(gameDisplay, green, Rect((200,150),(400,200)))
        largeText=pygame.font.SysFont('Comic Sans',30, False)
        TextSurf1, TextRect1 = text_objects('Play again?', largeText, white)
        TextRect1.center = ((display_width/2.2),(display_height/3))
        pygame.draw.rect(gameDisplay, white, Rect((275,275),(100,50)))
        TextSurfYes, TextRectYes = text_objects('Yes', largeText, black)
        TextRectYes.center = ((display_width/2.8),(display_height/2.2))
        pygame.draw.rect(gameDisplay, white, Rect((425,275),(100,50)))
        TextSurfNo, TextRectNo = text_objects('No', largeText, black)
        TextRectNo.center = ((display_width/1.9),(display_height/2.2))
        gameDisplay.unlock()
        gameDisplay.blit(TextSurf1, TextRect1)
        gameDisplay.blit(TextSurfYes, TextRectYes)
        gameDisplay.blit(TextSurfNo, TextRectNo)

        # checks if player clicks in "Yes" or "No" rectangles 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Player clicks "Yes"; play again
                if x > 275 and x < 375 and y > 275 and y < 325:
                    music.stop()
                    game_loop()
                # player clicks "No"; exit game 
                elif x > 425 and x < 525 and y > 275 and y < 325:
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.update() 
        time.sleep(2)

# displays a countdown clock; the user must finish the game before the time displays 0
def display_time(seconds):
    timeText=pygame.font.SysFont('Arial',60, True)
    TextSurf, TextRect = text_objects('Time:' + str(seconds), timeText, green2)
    TextRect.center = (775, 50)
    gameDisplay.blit(TextSurf, TextRect)
    
def game_loop():
    music.play() # start music until game restarted
    seconds = 40 # beginning number of seconds on countdown clock
    x = 350 
    y = 12
    img_dim = 40
    img_bottom = y + img_dim
    img_right = x + img_dim
    x_change = 0
    y_change = 0
    found1 = False
    found2 = False
    found3 = False 
    pygame.time.set_timer(1, 1000) # event to occur every second (1000 ms)
    while True:
        for event in pygame.event.get():
            # update countdown clock every second 
            if event.type == 1:
               # game over
                if seconds == 0:
                    message_display('OUT OF TIME')
                else:
                    seconds -= 1
            # user quits game 
            if event.type == pygame.QUIT:
                music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -2
                elif event.key == pygame.K_RIGHT:
                    x_change = 2
                elif event.key == pygame.K_UP:
                    y_change = -2
                elif event.key == pygame.K_DOWN:
                    y_change = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                    
        #check for collisions; if it occurs the img will bounce back a little
        # this prevents us getting stuck in our if statements
        # left collisions
        if x_change < 0:
            x_change = check_left(x,y,x_change,img_bottom,img_right)
        elif x_change > 0:    
            x_change = check_right(x,y,x_change,img_bottom,img_right)
        if y_change < 0:
            y_change = check_up(x,y,y_change,img_bottom,img_right)
        elif y_change > 0:
            y_change = check_down(x,y,y_change,img_bottom,img_right)
                
        x += x_change
        y += y_change 
        img_bottom = y + img_dim
        img_right = x + img_dim
        
        # made it to end
        if img_bottom >= 650 and x > 420 and img_right <= 500:
            # collected all guinness pints
            if found1 and found2 and found3:
                # player wins game 
                message_display('YOU WON!')
                
        # draw background       
        gameDisplay.blit(bg_img, (0,0))
        #draw images if player hasn't already found them
        if not found1:
            gameDisplay.blit(guinness_img, (440,20))
        if not found2:
            gameDisplay.blit(guinness_img, (110,180))
        if not found3:
            gameDisplay.blit(guinness_img, (350,510))

        # draw player
        gameDisplay.blit(me_img, (x,y))

        # set up rectangles            
        guinness1 = guinness_img.get_rect()
        guinness1.topleft = (440,20)
        guinness2 = guinness_img.get_rect()
        guinness2.topleft = (110,180)
        guinness3 = guinness_img.get_rect()
        guinness3.topleft = (350,510)
        me = me_img.get_rect()
        me.topleft = (x,y)
        # check for collisions with guinness pints
        if not found1 and guinness1.colliderect(me):
            found1 = True
        if not found2 and guinness2.colliderect(me):
            found2 = True
        if not found3 and guinness3.colliderect(me):
            found3 = True

        # display time in top right corner of screen
        display_time(seconds)

        # draw maze lines from lists
        pygame.draw.lines(gameDisplay,red,False,maze_lines, 3)
        pygame.draw.lines(gameDisplay,red,False,maze_lines2, 3)
        pygame.draw.lines(gameDisplay,red,False,maze_lines3, 3)
        pygame.draw.lines(gameDisplay,red,False,maze_lines4, 3)
        pygame.draw.lines(gameDisplay,red,False,maze_lines5, 3)
        pygame.draw.line(gameDisplay,red,(420,330),(660,330), 3)
        pygame.draw.line(gameDisplay,red,(260,250),(340,250), 3)
        pygame.draw.line(gameDisplay,red,(100,490),(260,490), 3)
        pygame.display.update()
        clock.tick(60)

    
game_loop()
music.stop()
pygame.quit()
quit()

# media credit: http://www.raindrop.org/rugrat/fun/maze01.gif
# http://rlv.zcache.ca/awesome_b_smiley_face_postcards-r8a3d3c8d48c04ba0aff44509d5fbe638_vgbaq_8byvr_512.jpg
# http://irishpubchallenge.com/wp-content/uploads/2013/01/guinness.jpg#
# Music: https://www.youtube.com/watch?v=mGI4kSdUOJQ
