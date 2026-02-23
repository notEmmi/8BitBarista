import pygame

import settingsdata
from pygame import mixer

class Recipes:
    def __init__(self, cafe_instance):
        # Initialize pygame
        pygame.init()
        mixer.init()

        self.cafe = cafe_instance  # Store the cafe instance

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Recipes")
        
        # Load images
        self.background = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/recipebook.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.hotcocoa = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/hotchocolate.png")
        self.hotcocoa = pygame.transform.scale(self.hotcocoa, (100, 100))
        self.sweetcoffee = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/sweetcoffee.png")
        self.sweetcoffee = pygame.transform.scale(self.sweetcoffee, (100, 100))
        self.teacake = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/teacake.png")
        self.teacake = pygame.transform.scale(self.teacake, (100, 100))
        self.honeycornbread = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/honeycornbread.png")
        self.honeycornbread = pygame.transform.scale(self.honeycornbread, (100, 100))
        self.tomatojam = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/tomatojam.png")
        self.tomatojam = pygame.transform.scale(self.tomatojam, (100, 100))

        self.description_box1 = pygame.Rect(200, 50, 150, 100)
        self.description_box2 = pygame.Rect(200, 150, 150, 100)
        self.description_box3 = pygame.Rect(200, 250, 150, 100)
        self.description_box4 = pygame.Rect(200, 350, 150, 100)
        self.description_box5 = pygame.Rect(200, 450, 150, 100)

        self.ingredients_box1 = pygame.Rect(500, 50, 150, 100)
        self.ingredients_box2 = pygame.Rect(500, 150, 150, 100)
        self.ingredients_box3 = pygame.Rect(500, 250, 150, 100)
        self.ingredients_box4 = pygame.Rect(500, 350, 150, 100)
        self.ingredients_box5 = pygame.Rect(500, 450, 150, 100)

        # Colors
        self.WHITE = (255, 255, 255)
        self.LIGHTBROWN = (254, 195, 117)
        self.BACKGROUNDBROWN = (205, 149, 74)
        self.SADDLEBROWN = (139, 69, 19)
        self.BLACK = (0, 0, 0)

        # Rectangle dimensions
        self.RECT_WIDTH, self.RECT_HEIGHT = 200, 100
        self.SPACING = 20

        # Calculate center positions
        center_x, center_y = self.WIDTH // 2, self.HEIGHT // 2

        # Define rectangles

        # Create surfaces for rectangles
        self.backButton = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 60, 200, 40)

        # Load font
        self.font = pygame.font.Font(pygame.font.match_font("courier"), 24)
        self.font2 = pygame.font.Font(pygame.font.match_font("courier"), 14)

        # Load and play background music
        mixer.music.load("tracks/08 - Shop.mp3")
        mixer.music.play()

    def draw_text(self, surface, text, rect, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect.topleft)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Check for hover effect

                # Check for click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backButton.collidepoint(event.pos):
                        print("Returning to cafe...")
                        running = False
                        self.cafe.run()  # Call the `run` method of the cafe instance

            # Draw background and UI elements
            self.screen.blit(self.background, (0, 0))

            self.draw_text(self.screen, "Hot Chocolate", self.description_box1, self.font, self.BLACK)
            self.screen.blit(self.hotcocoa, (80, 50))

            self.draw_text(self.screen, "Sweet Coffee", self.description_box2, self.font, self.BLACK)
            self.screen.blit(self.sweetcoffee, (80, 150))

            self.draw_text(self.screen, "Tea Cake", self.description_box3, self.font, self.BLACK)
            self.screen.blit(self.teacake, (80, 250))

            self.draw_text(self.screen, "Honey Cornbread", self.description_box4, self.font, self.BLACK)
            self.screen.blit(self.honeycornbread, (75, 350))

            self.draw_text(self.screen, "Tomato Jam", self.description_box5, self.font, self.BLACK)
            self.screen.blit(self.tomatojam, (80, 450))

            self.draw_text(self.screen, "Ingredients:Cocoa/Milk/Sugar", self.ingredients_box1, self.font2, self.BLACK)
            self.draw_text(self.screen, "Ingredients:Coffee Beans/Milk/Sugar", self.ingredients_box2, self.font2, self.BLACK)
            self.draw_text(self.screen, "Ingredients:Wheat/TeaLeaves/Milk/Sugar", self.ingredients_box3, self.font2, self.BLACK)
            self.draw_text(self.screen, "Ingredients:Corn/Milk/Honey", self.ingredients_box4, self.font2, self.BLACK)
            self.draw_text(self.screen, "Ingredients:Tomato/Sugar", self.ingredients_box5, self.font2, self.BLACK)

            pygame.draw.rect(self.screen, self.LIGHTBROWN, self.backButton, border_radius=12)
            self.draw_text(self.screen, "Back to Cafe", self.backButton, self.font, self.BLACK)

            pygame.display.flip()

        pygame.quit()

# Create an instance of RecipeScreen and run it
if __name__ == "__main__":
    app = Recipes()
    app.run()

