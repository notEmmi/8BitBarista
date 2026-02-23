import pygame, settingsdata
from screens.music_selector import MusicSelector
import sqlite3
from GameState import GameState

class OptionsMenu:
    def __init__(self, gameInstance = None):
        # Initialize Pygame
        pygame.init()

        # Screen Configuration
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("OPTIONS MENU")

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.ACTIVE_COLOR = (160, 100, 80)

        # Fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.button_font = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # Sliders (Volume Controls)
        self.sliders = {
            "Master Volume": settingsdata.volumes[0]
        }
        self.slider_rects = {}
        self.active_slider = None

        # Texture Settings
        self.textures = ["Low", "Med", "High"]
        self.texture_rects = []  # Stores hitboxes for texture buttons
        self.selected_texture = "High"

        # Buttons
        self.buttons = {
            "CONTROLS": pygame.Rect(200, 420, 100, 35),
            "ADVANCED": pygame.Rect(500, 420, 100, 35),
            "BACK": pygame.Rect(self.WIDTH // 2 - 40, 485, 80, 30)
        }

        self.masterVolumeMuteButton = pygame.Rect((self.WIDTH // 2) - 40, (self.HEIGHT // 2) - 28, 80, 18)

        # Transparent Save Button
        raw_image = pygame.image.load("assets/buttons/save.png")
        self.save_button_img = pygame.Surface(raw_image.get_size(), pygame.SRCALPHA)
        self.save_button_img.blit(raw_image, (0, 0))
        self.save_button_rect = self.save_button_img.get_rect(topleft=(58, 50))

        # Transparent Save Button
        raw_image = pygame.image.load("assets/buttons/save.png")
        self.save_button_img = pygame.Surface(raw_image.get_size(), pygame.SRCALPHA)
        self.save_button_img.blit(raw_image, (0, 0))
        self.save_button_rect = self.save_button_img.get_rect(topleft=(58, 50))

        # Add "MUSIC TRACK" button only if gameInstance exists
        self.currentGameInstance = gameInstance
        if self.currentGameInstance:
            self.buttons["MUSIC TRACK"] = pygame.Rect(330, 420, 140, 35)
        else:
            # Move "CONTROLS" and "ADVANCED" closer together
            self.buttons["CONTROLS"].x = 250
            self.buttons["ADVANCED"].x = 400

    def draw_slider(self, name, y_pos, value):
        """Draw sliders with `+` and `-` buttons."""
        min_x, max_x = 280, 520
        slider_rect = pygame.Rect(min_x, y_pos, max_x - min_x, 5)
        handle_x = min_x + int(value * (max_x - min_x))
        self.slider_rects[name] = (min_x, max_x, y_pos)

        pygame.draw.rect(self.screen, self.WHITE, slider_rect)
        pygame.draw.circle(self.screen, (201, 125, 96), (handle_x, y_pos + 3), 8)
        text = self.button_font.render(name, True, self.WHITE)
        self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, y_pos - 25))

        # Draw `-` and `+` buttons
        pygame.draw.rect(self.screen, (201, 125, 96), pygame.Rect(min_x - 31, y_pos - 6, 18, 18), border_radius=3)
        pygame.draw.rect(self.screen, (201, 125, 96), pygame.Rect(max_x + 17, y_pos - 6, 18, 18), border_radius=3)
        minus_text = self.button_font.render("-", True, self.WHITE)
        plus_text = self.button_font.render("+", True, self.WHITE)
        self.screen.blit(minus_text, minus_text.get_rect(center=(min_x - 22, y_pos + 3)))
        self.screen.blit(plus_text, plus_text.get_rect(center=(max_x + 26, y_pos + 3)))

        if (name != "Master Volume"): return

        pygame.draw.rect(self.screen, (201, 125, 96), self.masterVolumeMuteButton, border_radius=3)
        if (settingsdata.volumes[0] == 0.0): 
            muteToggleText = self.button_font.render("Unmute", True, (255, 255, 255))
            self.screen.blit(muteToggleText, plus_text.get_rect(center=(self.WIDTH // 2 - 28, self.HEIGHT // 2 - 20)))
        else:
            muteToggleText = self.button_font.render("Mute", True, (255, 255, 255))
            self.screen.blit(muteToggleText, plus_text.get_rect(center=(self.WIDTH // 2 - 18, self.HEIGHT // 2 - 20)))

    def draw_textures(self):
        """Draw texture options."""
        self.texture_rects.clear()
        x_positions = [280, 400, 520]
        for i, texture in enumerate(self.textures):
            texture_rect = pygame.Rect(x_positions[i] - 9, 380, 17, 17)
            self.texture_rects.append(texture_rect)
            color = self.ACTIVE_COLOR if texture == self.selected_texture else self.GRAY
            pygame.draw.circle(self.screen, color, (x_positions[i], 385), 8)
            text = pygame.font.Font(pygame.font.match_font('courier'), 16).render(texture, True, self.WHITE)
            self.screen.blit(text, (x_positions[i] - text.get_width() // 2, 354))
    
    def findVolumeToUpdate(self, slider: str, volume):
        if slider == "Master Volume": settingsdata.updateMasterVolume(volume)
        # elif slider == "Music": settingsdata.updateMusicVolume(volume)
        # elif slider == "SFX": settingsdata.updateSFXVolume(volume)

    def show_options(self, events):
        """Show options menu."""
        self.screen.fill(self.LIGHT_BROWN)
        pygame.display.set_caption("OPTIONS MENU")

        # Draw Background Panels
        middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
        panel_rect = pygame.Rect(180, 50, 450, 500)
        pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)

        # Draw Title
        title_text = self.title_font.render("OPTIONS", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 85))

        # Draw Sliders
        y_offset = self.HEIGHT // 2 - 50
        for name, value in self.sliders.items():
            self.draw_slider(name, y_offset, value)
            y_offset += 50

        # Draw Texture Selection
        # texture_text = self.button_font.render("TEXTURES", True, self.WHITE)
        # self.screen.blit(texture_text, (self.WIDTH // 2 - texture_text.get_width() // 2, 310))
        # self.draw_textures()

        # Draw Buttons
        mouse_pos = pygame.mouse.get_pos()
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (201, 125, 96), rect, border_radius=14)
            text = self.button_font.render(name, True, self.WHITE)
            self.screen.blit(text, text.get_rect(center=rect.center))

        self.screen.blit(self.save_button_img, self.save_button_rect)

        # Handle Events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check Buttons
                if self.save_button_rect.collidepoint(mouse_pos):
                    print("[DEBUG] Save button clicked!")
                    conn = sqlite3.connect("mydatabase.db")
                    if self.currentGameInstance is None:
                        print("[Debug] Can't save - no game instance available.")
                    else:
                        curr_hour, curr_minute = self.currentGameInstance.get_game_time()
                        game_state = GameState(
                            self.currentGameInstance.house,
                            self.currentGameInstance.pet,
                            self.currentGameInstance.playername,
                            self.currentGameInstance.selected_character,
                            self.currentGameInstance.current_day,
                            self.currentGameInstance.current_weather,
                            curr_hour,
                            curr_minute,
                            False,
                            None
                        )
                        game_state.save_to_db(conn, self.currentGameInstance.username)
                        conn.close()
                if self.masterVolumeMuteButton.collidepoint(mouse_pos):
                    settingsdata.toggleMuteMasterVolume()
                    self.sliders["Master Volume"] = settingsdata.volumes[0]
                for name, rect in self.buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if name == "CONTROLS":
                            return "controls"
                        elif name == "MUSIC TRACK" and self.currentGameInstance:
                            music_selector = MusicSelector(
                                self.screen, self.WIDTH, self.HEIGHT,
                                current_track_index=0,  # Default to the first track
                                current_track_path=self.currentGameInstance.background_music  # Pass the current track
                            )
                            next_screen, selected_track = music_selector.run()
                            if selected_track:
                                self.currentGameInstance.background_music = selected_track  # Save the confirmed track
                            return next_screen
                        elif name == "ADVANCED":
                            return "advanced"
                        elif name == "BACK":
                            if self.currentGameInstance is None:
                                return "menu"
                            self.currentGameInstance.is_paused = False
                            self.currentGameInstance.run()

                # Check Sliders (`+` and `-` buttons)
                for name, (min_x, max_x, y_pos) in self.slider_rects.items():
                    if min_x - 30 < mouse_pos[0] < min_x - 10 and y_pos - 8 < mouse_pos[1] < y_pos + 12:
                        self.sliders[name] = max(0, self.sliders[name] - 0.1)
                    elif max_x + 10 < mouse_pos[0] < max_x + 30 and y_pos - 8 < mouse_pos[1] < y_pos + 12:
                        self.sliders[name] = min(1, self.sliders[name] + 0.1)
                    else:
                        handle_x = min_x + int(self.sliders[name] * (max_x - min_x))
                        if handle_x - 10 < mouse_pos[0] < handle_x + 10 and y_pos - 10 < mouse_pos[1] < y_pos + 10:
                            self.active_slider = name

                # Texture Selection (`Low, Med, High`)
                for i, texture_rect in enumerate(self.texture_rects):
                    if texture_rect.collidepoint(mouse_pos):
                        self.selected_texture = self.textures[i]

            elif event.type == pygame.MOUSEBUTTONUP:
                self.active_slider = None

            elif event.type == pygame.MOUSEMOTION and self.active_slider:
                min_x, max_x, y_pos = self.slider_rects[self.active_slider]
                self.sliders[self.active_slider] = max(0, min(1, (mouse_pos[0] - min_x) / (max_x - min_x)))

        return "options"

# Example Usage
# options_menu = OptionsMenu()
# options_menu.show_options(events)