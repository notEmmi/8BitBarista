# code reused from within the project from a branch by darren, permission granted in private --arthur
import pygame # type: ignore [this is so vscode doesn't yell at me]

class AdvancedMenu:
    # Initialize Pygame
    def __init__(self):
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("ADVANCED OPTIONS")

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
        self.optionText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.inputValueText = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # Toggles
        self.toggles = {
            "RAIN ANIMATIONS": True,
            "SHADERS": True,
            "SCREEN SHAKE": False,
        }
        self.toggleSquares = {}

        # inputs
        self.inputs = {
            "RANDOM SEED": 23457894738,
        }
        global inputRects
        inputRects = {}

        # Bottom menu buttons
        self.menuButtons = {
            "BACK": pygame.Rect(self.WIDTH // 2 - 40, 485, 80, 30)
        }

        self.running = True

    # Function to draw a toggle
    def drawToggle(self, name, yPos, value):
        min_x, max_x = 550, 590
        length = max_x - min_x
        buttonRect = pygame.Rect(min_x, yPos, length, length)
        self.toggleSquares[name] = (buttonRect, value)
        optionLabel = self.optionText.render(name, True, self.WHITE)
        self.screen.blit(optionLabel, (min_x // 2 - 50, yPos + 10))
        pygame.draw.rect(self.screen, self.BRIGHT_BROWN, buttonRect, border_radius=7)
        if (value != True): return
        buttonRectIfToggled = pygame.Rect(min_x + 5, yPos + 5, length - 10, length - 10)
        pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, buttonRectIfToggled, border_radius=7)

    # Function to draw text input options
    def drawTextInputs(self, name, yPos, value):
        min_x, max_x = 440, 590
        length, height = max_x - min_x, 40
        buttonRect = pygame.Rect(min_x, yPos, length, height)
        inputRects[name] = (buttonRect, value)
        optionLabel = self.optionText.render(name, True, self.WHITE)
        self.screen.blit(optionLabel, (min_x // 2 + 5, yPos + 10))
        pygame.draw.rect(self.screen, self.BRIGHT_BROWN, buttonRect, border_radius=7)
        inputValueLabel = self.inputValueText.render(str(value), True, self.WHITE)
        self.screen.blit(inputValueLabel, (min_x + 10, yPos + 10))

    # Main Loop
    def run(self):
        while self.running:
            self.screen.fill(self.LIGHT_BROWN)  # Outer Coffee Background
            pygame.display.set_caption("ADVANCED OPTIONS")
            
            # Middle Dark Background
            middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
            shadow_offset = 6
            shadow_rect = middle_rect.move(shadow_offset, shadow_offset)
            shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
            
            # Inner Panel
            panel_rect = pygame.Rect(180, 50, 450, 500)
            shadow_rect_inner = panel_rect.move(shadow_offset, shadow_offset)
            shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
            shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
            pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
            self.screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
            pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)
            
            # Draw Title
            titleLabel = self.titleText.render("ADVANCED", True, self.WHITE)
            self.screen.blit(titleLabel, (self.WIDTH // 2 - titleLabel.get_width() // 2, 85))
            
            # Draw Sliders
            yOffset = 275 - (len(self.toggles) * 25) - 25 # -25 for seed text input height + padding
            for name, value in self.toggles.items():
                self.drawToggle(name, yOffset, value)
                yOffset += 60

            for inputName, inputValue in self.inputs.items():
                self.drawTextInputs(inputName, yOffset, inputValue)
                yOffset += 60

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
                    for toggleName, rectAndValue in self.toggleSquares.items():
                        if not rectAndValue[0].collidepoint(mousePosition): continue
                        print(f"{toggleName} value before change: {self.toggles[toggleName]}")
                        self.toggles[toggleName] = not self.toggles[toggleName]
                        print(f"{toggleName} value after change: {self.toggles[toggleName]}")
                        break
                    for inputName, rectangleValueTuple in inputRects.items():
                        if not rectangleValueTuple[0].collidepoint(mousePosition): continue
                        print(f"{inputName} clicked. its value is {self.inputs[inputName]}")
                        break
                    x_positions = [320, 400, 480]
            
            pygame.display.flip()