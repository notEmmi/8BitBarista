## THIS PAGE IS MEANT ONLY AS A TEMPORAY PLACE HODER UNTIL GAME IS FULL IMPLIMENTED TO SHOW NAVIAGTION TO RECIPE SCREEN WORKS AND CAN BE EASILY SWAPPED.

import pygame
import Recipes

class TempRecipeOptionScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Constants
        self.WIDTH, self.HEIGHT = 500, 400
        self.BUTTON_COLOR = (100, 200, 255)
        self.BUTTON_HOVER_COLOR = (50, 150, 255)
        self.BUTTON_TEXT_COLOR = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Create Screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Place Holder Recipe Option")
        
        # Load background image
        self.background = pygame.image.load("images/pinksky.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 30)
        
        # Button Setup
        self.button_rect = pygame.Rect(self.WIDTH // 2 - 75, self.HEIGHT // 2 - 25, 150, 50)
    
    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.BUTTON_HOVER_COLOR if self.button_rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.button_rect, border_radius=10)
        text_surface = self.button_font.render("See Recipes", True, self.BUTTON_TEXT_COLOR)
        self.screen.blit(text_surface, (self.button_rect.x + 25, self.button_rect.y + 10))
    
    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            
            # Draw Background
            self.screen.blit(self.background, (0, 0))
            
            # Draw Title
            title_surface = self.font.render("Place Holder Recipe Option", True, (0, 0, 0))
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 50))
            
            # Draw Button
            self.draw_button()
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        Recipes_Category_Screen = Recipes.Recipes()
                        Recipes_Category_Screen.run()
                        print("Button Clicked!")
            
            # Update Display
            pygame.display.flip()
        
        pygame.quit()

# Example usage
if __name__ == "__main__":
    app = TempRecipeOptionScreen()
    app.run()
