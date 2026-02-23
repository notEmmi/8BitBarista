import pygame
import sys
import temp_recipes_open_screen

class PlaceholderScreen:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Placeholder Screen")
        self.font = pygame.font.Font(None, 74)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_RETURN:
                        ## create an intance of placeholder recipe screen to be replaced later
                       TempRecipeStart = temp_recipes_open_screen.TempRecipeOptionScreen()
                       TempRecipeStart.run()


            self.screen.fill((0, 0, 0))
            text_surface = self.font.render("Coming Soon...", True, (255, 255, 255))
            self.screen.blit(text_surface, (self.WIDTH // 2 - text_surface.get_width() // 2, self.HEIGHT // 2 - text_surface.get_height() // 2))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Example usage
# placeholder_screen = PlaceholderScreen()
# placeholder_screen.run()
