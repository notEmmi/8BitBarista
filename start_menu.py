import pygame
import sys
import os
from options import OptionsMenu
from credits import CreditsScreen
from advanced import AdvancedMenu
from keybinds import ControlsMenu
from GameState import GameState
import sqlite3

class StartMenu:
    def __init__(self, username, gameInstance = None):
        # Initialize Pygame
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("8-BIT BARISTA")

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)  # Background
        self.DARK_BROWN = (38, 35, 34)  # Inner background
        self.BROWN = (99, 55, 44)  # Buttons and title bar
        self.WHITE = (255, 255, 255)
        self.SHADOW_COLOR = (20, 20, 20, 180)  # Shadow opacity adjustment

        # Fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.button_font = pygame.font.Font(pygame.font.match_font('courier'), 22)

        # Game States
        self.MENU = "menu"
        self.OPTIONS = "options"
        self.CHARACTER_SELECTION = "character_selection"
        self.CREDITS = "credits"
        self.CONTROLS = "controls"
        self.ADVANCED = "advanced"
        self.current_screen = self.MENU  # Start at the menu
        self.username = username

        self.isFromGame = False

        self.currentGameInstance = gameInstance

        # Define Buttons
        button_width, button_height = 200, 60
        button_x = (self.WIDTH - button_width) // 2
        button_spacing = 90
        button_start_y = 220
        self.buttons = [
            self.Button("NEW GAME", button_x -120, button_start_y, button_width, button_height, self.CHARACTER_SELECTION),
            self.Button("CONTINUE", button_x + 120, button_start_y, button_width, button_height, self.CHARACTER_SELECTION),
            self.Button("OPTIONS", button_x, button_start_y + button_spacing, button_width, button_height, self.OPTIONS),
            self.Button("CREDITS", button_x, button_start_y + 2 * button_spacing, button_width, button_height, self.CREDITS),
            self.Button("EXIT", (self.WIDTH - 150) // 2, button_start_y + 3 * button_spacing, 150, 55, None)
        ]

        # Load Coffee Cup Image
        try:
            image_path = os.path.join("assets", "images", "others", "coffee.png")
            self.coffee_img = pygame.image.load(image_path)
            self.coffee_img = pygame.transform.scale(self.coffee_img, (235, 235))
        except:
            self.coffee_img = None

    def draw_blurred_shadow(self, surface, rect, blur_radius=10, offset_x=8, offset_y=8, border_radius=12):
        """Draws a smooth, blurred shadow for UI elements."""
        shadow_surface = pygame.Surface((rect.width + offset_x * 2, rect.height + offset_y * 2), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 0))  # Transparent layer
        shadow_rect = pygame.Rect(offset_x, offset_y, rect.width, rect.height)
        pygame.draw.rect(shadow_surface, self.SHADOW_COLOR, shadow_rect, border_radius=border_radius)
        surface.blit(shadow_surface, (rect.x, rect.y))

    def load_user_save(username):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT character, building, pet, day, weather, hour, minute FROM saves WHERE username = ?", (username,))
        save = cursor.fetchone()
        conn.close()
        return save

    class Button:
        """UI Button with hover effects and shadows."""
        def __init__(self, text, x, y, width, height, action, border_radius=12):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = (99, 55, 44)
            self.border_radius = border_radius
            self.action = action  # Action defines which screen to switch to

        def draw(self, screen, mouse_pos, button_font, draw_blurred_shadow, DARK_BROWN, BROWN, WHITE):
            draw_blurred_shadow(screen, self.rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=self.border_radius)
            pygame.draw.rect(screen, DARK_BROWN if self.rect.collidepoint(mouse_pos) else BROWN, self.rect, border_radius=self.border_radius)
            text_surface = button_font.render(self.text, True, WHITE)
            screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

        def is_clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

    def show_menu(self):
        self.screen.fill(self.LIGHT_BROWN)

        # Inner Background
        center_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        self.draw_blurred_shadow(self.screen, center_rect, blur_radius=15, offset_x=4, offset_y=4, border_radius=12)
        pygame.draw.rect(self.screen, self.DARK_BROWN, center_rect, border_radius=12)

        # Title Bar
        title_rect = pygame.Rect(160, 70, 480, 85)
        self.draw_blurred_shadow(self.screen, title_rect, blur_radius=10, offset_x=6, offset_y=6, border_radius=12)
        pygame.draw.rect(self.screen, self.BROWN, title_rect, border_radius=12)
        self.screen.blit(self.title_font.render("8-BIT BARISTA", True, self.WHITE), self.title_font.render("8-BIT BARISTA", True, self.WHITE).get_rect(center=title_rect.center))

        # Mouse Tracking
        mouse_pos = pygame.mouse.get_pos()

        # Draw Buttons
        for button in self.buttons:
            button.draw(self.screen, mouse_pos, self.button_font, self.draw_blurred_shadow, self.DARK_BROWN, self.BROWN, self.WHITE)

        # Draw Coffee Cup
        if self.coffee_img:
            image_x = (self.WIDTH - self.coffee_img.get_width()) - 45
            image_y = (self.HEIGHT - self.coffee_img.get_height()) - 60
            self.screen.blit(self.coffee_img, (image_x, image_y))

    def run(self):
        running = True
        options_menu = OptionsMenu(gameInstance=self.currentGameInstance)  # Create an instance of OptionsMenu
        advanced_menu = AdvancedMenu()
        controls_menu = ControlsMenu()
        credits = CreditsScreen()  # Create an instance of CreditsScreen
        from character_selection import CharacterSelector  # Import CharacterSelector
        character_selector = CharacterSelector(self.username)  # Create an instance of CharacterSelector
        while running:
            events = pygame.event.get()
            self.screen.fill(self.LIGHT_BROWN)

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Handle screen transitions
            if self.current_screen == self.MENU:
                self.show_menu()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in self.buttons:
                            if button.is_clicked(pygame.mouse.get_pos()):
                                if button.action:
                                    self.current_screen = button.action
                                if button.text == "EXIT":
                                    running = False
                                print(f"{button.text} button clicked!")
                    
                                if button.text == "CONTINUE":
                                    print(f"{button.text} button clicked!")

                                    conn = sqlite3.connect('mydatabase.db')

                                    # Use account username to load correct save
                                    loaded_game_state = GameState.load_from_db(conn, self.username)
                                    conn.close()

                                    if loaded_game_state:
                                        if loaded_game_state.selected_character is None:
                                            print("No character found. Redirecting to character selection.")
                                            self.current_screen = self.CHARACTER_SELECTION
                                        else:
                                            print(
                                                loaded_game_state.house,
                                                loaded_game_state.pet,
                                                loaded_game_state.name,
                                                loaded_game_state.selected_character,
                                                loaded_game_state.current_day,
                                                loaded_game_state.current_weather,
                                                loaded_game_state.time_hour,
                                                loaded_game_state.time_minute,
                                                loaded_game_state.GameData,
                                                self.username
                                            )

                                            from first_page import Game
                                            loadSave = Game(
                                                chosen_building=loaded_game_state.house,
                                                petChoice=loaded_game_state.pet,
                                                name=loaded_game_state.name,
                                                selected_character=loaded_game_state.selected_character,
                                                current_day=loaded_game_state.current_day,
                                                current_weather=loaded_game_state.current_weather,
                                                time_hour=loaded_game_state.time_hour,
                                                time_minute=loaded_game_state.time_minute,
                                                fromPriorMenu=loaded_game_state.fromPriorMenu,
                                                gameData=loaded_game_state.GameData,
                                                username=self.username
                                            )
                                            loadSave.run()
                                            running = False
                                    else:
                                        print("No save data found for this user.")

            elif self.current_screen == self.OPTIONS:
                new_screen = options_menu.show_options(events)
                if new_screen == "menu":
                    self.current_screen = self.MENU
                elif new_screen == "controls":
                    self.current_screen = self.CONTROLS
                elif new_screen == "advanced":
                    self.current_screen = self.ADVANCED

            elif self.current_screen == self.CREDITS:
                new_screen = credits.show_credits(self.screen, events)  # Store return value      
                if new_screen == "menu":  # If "BACK" is clicked in credits.py
                    self.current_screen = self.MENU  # Switch back to start menu

            elif self.current_screen == self.CHARACTER_SELECTION:
                character_selector.run()  # Run the character selection screen
                self.current_screen = self.MENU  # After character selection, return to menu

            elif self.current_screen == self.ADVANCED:
                advanced_button_callback = advanced_menu.run()
                if advanced_button_callback == "options": self.current_screen = self.OPTIONS

            elif self.current_screen == self.CONTROLS:
                controls_button_callback = controls_menu.run()
                if controls_button_callback == "options": self.current_screen = self.OPTIONS

            pygame.display.flip()  # Update screen

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
 start_menu = StartMenu()
 start_menu.run()