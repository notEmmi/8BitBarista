# code reused from within the project from a branch by darren, permission granted in private --arthur
import pygame # type: ignore [this is so vscode doesn't yell at me]

class ControlsMenu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("KEYBINDS")

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)  # Outer Background
        self.DARK_BROWN = (38, 35, 34)  # Middle Dark Background
        self.BROWN = (99, 55, 44)  # Inner Panel Color
        self.WHITE = (255, 255, 255)
        self.SHADOW_COLOR = (20, 20, 20, 30)
        self.GRAY = (100, 100, 100)
        self.ACTIVE_COLOR = (160, 100, 80)
        self.BRIGHT_BROWN = (143, 89, 68)
        self.BRIGHTEST_BROWN = (201, 125, 96)

        # Fonts
        self.titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
        self.actionText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.keybindValueText = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # keybinds
        self.keybinds = {
            "UP": "W",
            "DOWN": "S",
            "LEFT": "A",
            "RIGHT": "D",
            "INVENTORY": "E",
            "PRIMARY ACTION": "C",
            "SECONDARY ACTION": "X",
            "PAUSE": "ESCAPE",
            "TOOLBAR SLOTS": "1 to 5",
        }
        self.keybindSquares = {}

        # Bottom menu buttons
        self.menuButtons = {
            "BACK": pygame.Rect(self.WIDTH // 2 - 40, 485, 80, 30)
        }

        self.running = True

    # Function to draw a toggle
    def drawKeybind(self, name, yPos, xPos, value):
        keybindXPos, length = 475, 30
        buttonRect = pygame.Rect(keybindXPos, yPos, length * 3.75, length)
        self.keybindSquares[name] = (buttonRect, value)
        actionLabel = self.actionText.render(name, True, self.WHITE)
        self.screen.blit(actionLabel, (xPos, yPos + 10))
        pygame.draw.rect(self.screen, self.BRIGHT_BROWN, buttonRect, border_radius=7)
        keybindValueLabel = self.keybindValueText.render(value, True, self.WHITE)
        self.screen.blit(keybindValueLabel, (keybindXPos + (buttonRect.width // 2 - keybindValueLabel.get_width() // 2), yPos + 7.5))

    def run(self):
        # Main Loop
        while self.running:
            self.screen.fill(self.LIGHT_BROWN)  # Outer Coffee Background
            pygame.display.set_caption("KEYBINDS")
            
            # Middle Dark Background
            middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
            shadow_offset = 6
            shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
            
            # Inner Panel
            panel_rect = pygame.Rect(180, 50, 450, 500)
            shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
            shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)
            
            # Draw Title
            titleLabel = self.titleText.render("KEYBINDS", True, self.WHITE)
            self.screen.blit(titleLabel, (self.WIDTH // 2 - titleLabel.get_width() // 2, 85))
            
            # Draw keybinds
            # if 6, reset y offset
            yOffset = 300 - (6 * 25)
            xOffset = 225
            for name, value in self.keybinds.items():
                self.drawKeybind(name, yOffset, xOffset, value)
                yOffset += 35

            # draw menuButtons
            for name, rect in self.menuButtons.items():
                pygame.draw.rect(self.screen, self.BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=14)
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))
            
            # Event Handling
            mousePosition = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITTING")
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("MOUSEDOWN")
                    for name, rect in self.menuButtons.items():
                        if not rect.collidepoint(mousePosition): continue
                        return "options"
                    for actionName, rectAndValue in self.keybindSquares.items():
                        if not rectAndValue[0].collidepoint(mousePosition): continue
                        print(f"{actionName} clicked. keybind: {self.keybinds[actionName]}")
            
            pygame.display.flip()
        return "options"
