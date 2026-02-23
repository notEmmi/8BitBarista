import pygame
from screens.Building_Confirm_Selection_Screen import BuildingConfirmationScreen

class BuildingSelectionScreen:
    def __init__(self, playername, selected_character, username):
        # Screen settings
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.SCREEN_COLOR = (30, 30, 30)
        self.SQUARE_SIZE = 160
        self.PADDING = 20
        self.ROWS, self.COLS = 2, 3
        self.HOVER_COLOR = (144, 238, 144)
        self.SQUARE_COLOR = (0, 0, 0)

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Building Selection")
        self.playername = playername
        self.selected_character = selected_character
        self.username = username
        # Load background and sign
        self.background = pygame.image.load("assets/images/others/sky.png")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.sign = pygame.image.load("images/buildingSign.png")
        self.sign = pygame.transform.scale(self.sign, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 5))

        # Load and store buildings
        self.image_paths = [
            "assets/images/buildings/building1.png",
            "assets/images/buildings/building2.png",
            "assets/images/buildings/building3.png",
            "assets/images/buildings/building4.png",
            "assets/images/buildings/building5.png",
            "assets/images/buildings/building6.png"
        ]
        self.images = [pygame.image.load(path) for path in self.image_paths]
        self.resized_images = [pygame.transform.scale(img, (self.SQUARE_SIZE, self.SQUARE_SIZE)) for img in self.images]
        self.squares = self.create_squares()

    def create_squares(self):
        total_width = self.COLS * self.SQUARE_SIZE + (self.COLS - 1) * self.PADDING
        total_height = self.ROWS * self.SQUARE_SIZE + (self.ROWS - 1) * self.PADDING
        start_x = (self.SCREEN_WIDTH - total_width) // 2
        start_y = (self.SCREEN_HEIGHT - total_height) // 2

        squares = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = start_x + col * (self.SQUARE_SIZE + self.PADDING)
                y = start_y + row * (self.SQUARE_SIZE + self.PADDING)
                index = row * self.COLS + col
                squares.append({
                    "rect": pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE),
                    "image": self.resized_images[index],
                    "image_path": self.image_paths[index],
                    "hover": False
                })
        return squares

    def run(self):
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for square in self.squares:
                        if square["rect"].collidepoint((mouse_x, mouse_y)):
                            print("Square clicked!")
                            building_confirm_screen = BuildingConfirmationScreen(square["image_path"], self.playername, self.selected_character, self.username)
                            building_confirm_screen.run()
                            running = False

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.sign, (self.SCREEN_WIDTH // 4, 5))

            for square in self.squares:
                square["hover"] = square["rect"].collidepoint((mouse_x, mouse_y))
                color = self.HOVER_COLOR if square["hover"] else self.SQUARE_COLOR
                pygame.draw.rect(self.screen, color, square["rect"])
                pygame.draw.rect(self.screen, (255, 255, 255), square["rect"], 2)
                self.screen.blit(square["image"], (square["rect"].x, square["rect"].y))

            pygame.display.flip()

        pygame.quit()

# Optional: Run directly
if __name__ == "__main__":
    screen = BuildingSelectionScreen()
    screen.run()
