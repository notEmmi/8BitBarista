import pygame
import screens.Building_Selection_Screen
from screens.Building_Congratz_Screen import BuildingCongratzScreen

class BuildingConfirmationScreen:
    def __init__(self, image_path, playername, selected_character, username):
        pygame.init()

        # Save image path
        self.image_path = image_path
        self.playername = playername
        self.selected_character = selected_character
        self.username = username
        # Screen settings
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.SQUARE_SIZE = 200
        self.RECT_WIDTH, self.RECT_HEIGHT = 400, 50
        self.TITLE_SIZE = (400, 100)
        self.CIRCLE_RADIUS = 50

        # Set up display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Building Confirmation")

        # Load assets
        self.background = pygame.image.load("assets/images/others/sky.png")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.title = pygame.image.load("images/buildingconfrim.png")
        self.title = pygame.transform.scale(self.title, self.TITLE_SIZE)

        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        # Font and text
        self.font = pygame.font.Font(None, 36)
        self.yes_text = self.font.render("YES", True, (255, 255, 255))
        self.no_text = self.font.render("NO", True, (255, 255, 255))

        # Precompute layout
        self.square_x = (self.SCREEN_WIDTH - self.SQUARE_SIZE) // 2
        self.square_y = (self.SCREEN_HEIGHT - self.SQUARE_SIZE) // 2
        self.circle_left_x = self.square_x - self.CIRCLE_RADIUS - 50
        self.circle_right_x = self.square_x + self.SQUARE_SIZE + 50 + self.CIRCLE_RADIUS
        self.circle_y = self.square_y + self.SQUARE_SIZE // 2

    def is_inside_circle(self, point, circle_x, circle_y, radius):
        return (point[0] - circle_x) ** 2 + (point[1] - circle_y) ** 2 <= radius ** 2

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_inside_circle(mouse_pos, self.circle_left_x, self.circle_y, self.CIRCLE_RADIUS):
                        print("YES clicked! Proceeding with selection.")
                        congratz_screen = BuildingCongratzScreen(self.image_path, self.playername, self.selected_character, self.username)
                        congratz_screen.run()
                        running = False

                    elif self.is_inside_circle(mouse_pos, self.circle_right_x, self.circle_y, self.CIRCLE_RADIUS):
                        print("NO clicked! Cancelling selection.")
                        from screens.Building_Selection_Screen import BuildingSelectionScreen
                        selection_screen = BuildingSelectionScreen()
                        selection_screen.run()
                        running = False

            self.draw()

        pygame.quit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.image, (self.square_x, self.square_y))
        self.screen.blit(self.title, (self.square_x // 2 + 50, self.square_y - 150))

        # Draw YES and NO circles
        pygame.draw.circle(self.screen, (0, 255, 0), (self.circle_left_x, self.circle_y), self.CIRCLE_RADIUS)
        pygame.draw.circle(self.screen, (255, 0, 0), (self.circle_right_x, self.circle_y), self.CIRCLE_RADIUS)

        # Draw text
        self.screen.blit(self.yes_text, (self.circle_left_x - self.yes_text.get_width() // 2, self.circle_y - self.yes_text.get_height() // 2))
        self.screen.blit(self.no_text, (self.circle_right_x - self.no_text.get_width() // 2, self.circle_y - self.no_text.get_height() // 2))

        pygame.display.flip()

# Optional: Run directly
if __name__ == "__main__":
    screen = BuildingConfirmationScreen("assets/images/buildings/building1.png")
    screen.run()
