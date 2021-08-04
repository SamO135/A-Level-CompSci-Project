# Game options/settings
import pygame as pg
import os


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Alien Adventure"
FPS = 60
FONT_NAME = "Neon.ttf"
#"nasalization-rg.ttf"
#"neon.ttf"
XML_FILE = os.path.join(os.path.dirname(__file__), "spritesheet_complete.xml")
HS_FILE = os.path.join(os.path.dirname(__file__), "Highscore.txt")
BG_IMAGE = os.path.join(os.path.dirname(__file__), "skyhill.png")
SPRITESHEET = os.path.join(os.path.dirname(__file__), "spritesheet_complete.png")
#"Background.jpg"
#"skyhill.png"



#---------------------------------------------------------------------
# Colours
#---------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 191, 11)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
GREY = (85, 85, 85)
GOLD = (255,223,0)
PINK = (255,105,180)
GREY2 = (90, 128, 135)
BG_COLOUR = LIGHT_BLUE
START_SCREEN_COLOUR = BLACK


#---------------------------------------------------------------------
# GAME STUFF
#---------------------------------------------------------------------
"""LEADERBOARD"""
NUM_OF_TOP_SCORES = 10
DEFAULT_TOP_SCORES = 0
LB_TOP_LEFT = ((SCREEN_WIDTH * 3/4) ,(SCREEN_HEIGHT / 4)) #(x, y)
LB_FONT_SIZE = 25
LB_TITLE_SIZE = 35
LB_COLOUR = WHITE

"""TEXT"""
TEXT_COLOUR = WHITE
TEXT_SIZE = 25
GAME_OVER_COLOUR = RED
TITLE_COLOUR = GOLD
TITLE_FONT_SIZE = 72
SCORE_FONT_SIZE = 40


"""BACKGROUND"""
NUM_OF_BG = 2
BG_SPEED = 1
MAX_PARALAX_DELAY = 2


#--------------------------------------------------------------------------------
# PLAYER PROPERTIES
#--------------------------------------------------------------------------------
PLAYER_ACC = (0.075/FPS) # Add this value to the velocity every second: x/FPS
PLAYER_GRAV = 0.8
JUMP_POWER = -18
DOUBLE_JUMP_POWER = -14
JUMP_CUT_POWER = -8
MAX_SPEED = 16
STARTING_VEL_X = 8
PLAYER_FRAME_DELAY = 150 #ms


#---------------------------------------------------------------------
# PLATFORM PROPERTIES
#---------------------------------------------------------------------
NUM_OF_PLATFORMS = 4
PLATFORM_HEIGHT = 20
TOP_BOUNDARY = 250
BOTTOM_BOUNDARY = SCREEN_HEIGHT - 100
BASE_PLATFORM_GAP_X = 200
PLATFORM_GAP_Y = 150
PLATFORM_COLOUR = DARK_GREEN
LAND_POINTS = 10
PLATFORM_WIDTHS = [4, 6, 8, 10, 12]

#---------------------------------------------------------------------
# STARTING PLATFORM LIST
#---------------------------------------------------------------------
STARTING_PLATFORM_LENGTH = "8"
STARTING_PLATFORM = (150, SCREEN_HEIGHT * 3/4, STARTING_PLATFORM_LENGTH)




#---------------------------------------------------------------------
# ENEMY PROPERTIES
#---------------------------------------------------------------------
START_CHANCE_OF_ENEMY = 30    #As a percentage
MAX_CHANCE_OF_ENEMY = 80   #As a percentage (Added in 13)
KILL_POINTS = 10
PTS_TO_INC_CHANCE = 40    #Points to increase chance of enemy spawning by 1%
ENEMY_FRAME_DELAY = 200



#---------------------------------------------------------------------
# BULLET PROPERTIES
#---------------------------------------------------------------------
BULLET_VEL = 20
BULLET_RAD = 5
BULLET_COLOUR = BLACK
STARTING_BULLETS = 30


#--------------------------------------------------------------------
# POWERUPS
#--------------------------------------------------------------------
CHANCE_OF_POW = 15   #As a percentage
MORE_BULLETS = 5

#-------------------------------------------------------------------
# COINS
#-------------------------------------------------------------------
COIN_POINTS = 10
CHANCE_OF_COIN = 50    #As a percentage


