import pygame
import sys
class confirmPet:
    def __init__(self): ## pass a pet type that will be used to decide between lists of pngs to choose from
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("confrim pet")
        
        # Set up clock for frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.WHITE = (255, 255, 255)
        self.BROWN = (240, 161, 36)
        
    
    def run(self):
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                
            

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(self.FPS)

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    confirm_pet = confirmPet()
    confirm_pet.run()