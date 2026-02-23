###### TEXT BOX AND TEXT LOCATION VARS ###############


USERNAME_TEXT_LOC = 40, 100
PASSWORD_TEXT_LOC = 40, 160
TITLE_BOX_BACKGROUND_LOC = 200,40
TITLE_TEXT_LOC = 212, 45


GRASS_LOC_LOGIN = -35,325
SKY_LOC = 0,0



### colors ####
WHITE = (255, 255, 255)
LIGHT_PURPLE = (200, 162, 200)
DARK_PURPLE = (150, 112, 150)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)



#### LOADING CONFIGS ###

import math


### colors ####


## asset locations load screen ######
GRASS_LOC = -35,450
LOADING_LOC = 225, 50
TREE_LOC = 50, 250
CLOUD_LOC = 25, 100


TREE_SIZE = 250, 350
GRASS_SIZE = 900, 150
LOADING_SIZE = 350, 125
CLOUD_SIZE = 100, 100

### vars needed for moving star

STARX ,STARY = 100, 300
STARDX, STARDY = 100, -50
STARSIZE = (50,50)








### animation fucntions ####





def updateStar(dx,dy):
    
    global STARX, STARY  # Access and modify global variables

    if(STARX >=625):
        STARX = 100
        STARY= 300
    STARX += dx
    STARY += dy
    return STARX, STARY  # Return updated values
