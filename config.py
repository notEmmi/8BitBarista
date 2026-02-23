
import math


### colors ####
WHITE = (255, 255, 255)
LIGHT_PURPLE = (200, 162, 200)
DARK_PURPLE = (150, 112, 150)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

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

    









 




