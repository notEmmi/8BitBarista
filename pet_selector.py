import pygame
import sys
class PetSelector:
    def __init__(self, img_path, playername, selected_character, username): ## pass a pet type that will be used to decide between lists of pngs to choose from
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pet Selector")
        self.playername = playername
        self.username = username
        self.building = img_path
        # Set up clock for frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BROWN = (240, 161, 36)
        self.selection = pygame.image.load("images/questionmark.png")
        self.selection = pygame.transform.scale(self.selection, (150,150))
 
        self.background = pygame.image.load("images/petScreenBkgrnd.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        
        self.sign = pygame.image.load("assets/images/others/petsign.png")
        self.sign = pygame.transform.scale(self.sign, (self.WIDTH/4, self.HEIGHT/4))

        self.rightarrowRect1 = pygame.Rect(self.WIDTH -150, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.rightarrow1 = pygame.image.load("images/rightarrow.png")
        self.rightarrow1 = pygame.transform.scale(self.rightarrow1, (50, 50))

        self.leftarrowRect1 = pygame.Rect((self.WIDTH-self.WIDTH)+100, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.leftarrow1 = pygame.image.load("images/leftarrow.png")
        self.leftarrow1 = pygame.transform.scale(self.leftarrow1, (50, 50))

        self.rightarrowRect2 = pygame.Rect((self.WIDTH-self.WIDTH)+150, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.rightarrow2 = pygame.image.load("images/rightarrow.png")
        self.rightarrow2 = pygame.transform.scale(self.rightarrow2, (50, 50))

        self.leftarrowRect2 = pygame.Rect(self.WIDTH -200, self.HEIGHT/2, 50, 50)  # Placeholder for arrow rectangle
        self.leftarrow2 = pygame.image.load("images/leftarrow.png")
        self.leftarrow2 = pygame.transform.scale(self.leftarrow2, (50, 50))

        self.selected_character = selected_character    
            
        self.dogsList = ["assets/images/pets/greydog.png", "assets/images/pets/yellowdog.png", "assets/images/pets/browndog.png"]
        self.dogRect = pygame.Rect(self.WIDTH/1.3, self.HEIGHT/1.7, 150,150)
        self.dog = pygame.image.load("assets/images/pets/greydog.png")
        self.dog = pygame.transform.scale(self.dog, (150,150))


        self.catList = ["assets/images/pets/greycat.png", "assets/images/pets/yellowcat.png", "assets/images/pets/browncat.png"]
        self.catRect = pygame.Rect(self.WIDTH/10, self.HEIGHT/1.6, 150,150)
        self.cat = pygame.image.load("assets/images/pets/greycat.png")
        self.cat = pygame.transform.scale(self.cat, (150,150))



        self.selectionRect = pygame.Rect(self.WIDTH/2 -60, self.HEIGHT/1.6, 150,150)
        
        self.isThisYourChoiceRect = pygame.Rect(self.WIDTH/2 -150, self.HEIGHT/2.2, 300, 100)
        self.choice = pygame.image.load("images/choicesign.png")
        self.choice = pygame.transform.scale(self.choice, (300,100))
        self.petChoice = "assets/images/pets/greydog.png"
       
       
        self.arrowPressCountdog =0
        self.arrowPressCountcat =0
        self.madeachoice =0
        
        
    def parseDogListRight(self):
        
            
            if self.arrowPressCountdog < 2:
                self.arrowPressCountdog +=1
                self.dog = self.dogsList[self.arrowPressCountdog]
                return

    def parseDogListLeft(self):
        
            
            if  self.arrowPressCountdog >0:
                self.arrowPressCountdog -=1
                self.dog = self.dogsList[self.arrowPressCountdog]
                return
    def parsecatListLeft(self):
        
            
            if self.arrowPressCountcat >0:
                self.arrowPressCountcat -=1
                self.cat = self.catList[self.arrowPressCountcat]
                return
            
    def parsecatListRight(self):
        
            
            if self.arrowPressCountcat < 2:
                self.arrowPressCountcat +=1
                self.cat = self.catList[self.arrowPressCountcat]
                return

    def run(self):
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if self.rightarrowRect1.collidepoint(event.pos):
                       self.dog = self.parseDogListRight()
                       self.dog = pygame.image.load(self.dogsList[self.arrowPressCountdog])
                       self.dog = pygame.transform.scale(self.dog, (150,150))
                    elif self.leftarrowRect2.collidepoint(event.pos):
                       self.dog = self.parseDogListLeft()
                       self.dog = pygame.image.load(self.dogsList[self.arrowPressCountdog])
                       self.dog = pygame.transform.scale(self.dog, (150,150))
                         
                    
                    elif self.rightarrowRect2.collidepoint(event.pos):
                       self.cat = self.parsecatListRight()
                       self.cat = pygame.image.load(self.catList[self.arrowPressCountcat])
                       self.cat = pygame.transform.scale(self.cat, (150,150))
                    elif self.leftarrowRect1.collidepoint(event.pos):
                       self.cat = self.parsecatListLeft()
                       self.cat = pygame.image.load(self.catList[self.arrowPressCountcat])
                       self.cat = pygame.transform.scale(self.cat, (150,150))
                    elif self.dogRect.collidepoint(event.pos):
                         print("clicked dog rect")
                         self.selection = self.dog
                         self.madeachoice =1
                         self.petChoice = self.dogsList[self.arrowPressCountdog]
                    elif self.catRect.collidepoint(event.pos):
                         print("clicked cat rect")
                         self.selection = self.cat
                         self.madeachoice =1
                         self.petChoice = self.catList[self.arrowPressCountcat]
                    elif self.isThisYourChoiceRect.collidepoint(event.pos):
                         if self.madeachoice >0:
                            
                            from first_page import Game
                            game = Game(self.building, self.petChoice, self.playername, selected_character=self.selected_character, username=self.username)
                            game.run()
                            running = False
                   
                         
                         
                    

            # Fill the screen with white (or any color you like)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.sign, (self.WIDTH/2 - 100, self.HEIGHT/6))
            
            

            pygame.draw.rect(self.screen, self.BROWN, self.leftarrowRect1)
            pygame.draw.rect(self.screen, self.WHITE, self.rightarrowRect1)
            pygame.draw.rect(self.screen, self.BROWN, self.leftarrowRect2)
            pygame.draw.rect(self.screen, self.WHITE, self.rightarrowRect2)
            
            
            self.screen.blit(self.leftarrow1, self.leftarrowRect1.topleft)
            self.screen.blit(self.rightarrow1, self.rightarrowRect1.topleft)
            self.screen.blit(self.rightarrow2, self.rightarrowRect2.topleft)
            self.screen.blit(self.leftarrow2, self.leftarrowRect2.topleft)
            self.screen.blit(self.dog, self.dogRect.topleft)
            self.screen.blit(self.cat, self.catRect.topleft) 
            self.screen.blit(self.selection, self.selectionRect)
            if self.madeachoice >0:
                 self.screen.blit(self.choice, self.isThisYourChoiceRect.topleft)
             
            

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(self.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pet_selector = PetSelector("assets/images/buildings/building1.png", "jake")
    pet_selector.run()