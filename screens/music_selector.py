import pygame
import os

class MusicSelector:
    def __init__(self, screen, width, height, current_track_index=0, current_track_path=None):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height

        # Hardcoded music tracks with shortened names
        self.music_tracks = [
            ("New Life", "assets/sounds/1_new_life_master.mp3"),
            ("Working Time", "assets/sounds/4_working_time_master.mp3"),
            ("8-Bit Arcade", "assets/sounds/8-bit-arcade-mode-158814.mp3"),
            ("Cafe Avenue", "assets/sounds/2_cafe_avenue_master.mp3")
        ]

        # Determine the current track index based on the original track path
        self.current_track_index = next(
            (i for i, (_, path) in enumerate(self.music_tracks) if path == current_track_path),
            current_track_index  # Default to the provided index if no match is found
        )
        self.previewing_track = None  # Track currently being previewed
        self.original_track_path = current_track_path  # Store the original track path

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.ACTIVE_COLOR = (160, 100, 80)

        # Fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.button_font = pygame.font.Font(pygame.font.match_font('courier'), 18)

        # Buttons
        self.left_button = pygame.Rect(280, 300, 30, 30)
        self.right_button = pygame.Rect(490, 300, 30, 30)
        self.back_button = pygame.Rect(self.WIDTH // 2 - 40, 500, 80, 30)

        self.track_rects = []  # Store rectangles for each track for click detection

        # Confirmation Button
        self.confirm_button = pygame.Rect(self.WIDTH // 2 - 60, 450, 120, 35)

    def play_preview(self, track_path):
        """Play the selected track as a preview."""
        if self.previewing_track != track_path:
            pygame.mixer.music.stop()  # Stop any currently playing music
            pygame.mixer.music.load(track_path)  # Load the selected track
            pygame.mixer.music.play()  # Play the track once
            self.previewing_track = track_path  # Update the previewing track

    def draw(self):
        """Draw the music selector menu."""
        self.screen.fill(self.LIGHT_BROWN)

        # Draw Background Panels
        middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)
        panel_rect = pygame.Rect(180, 50, 450, 500)
        pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)

        # Draw Title
        title_text = self.title_font.render("MUSIC SELECTOR", True, self.WHITE)
        self.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 85))

        # Draw Music Tracks as a List with Uniform Borders
        self.track_rects.clear()
        y_offset = 170
        border_width, border_height = 200, 40  # Fixed size for all borders
        for i, (track_name, _) in enumerate(self.music_tracks):
            track_color = self.ACTIVE_COLOR if i == self.current_track_index else self.WHITE
            track_text = self.button_font.render(track_name, True, track_color)
            track_rect = track_text.get_rect(center=(self.WIDTH // 2, y_offset))

            # Draw Uniform Border
            border_rect = pygame.Rect(
                self.WIDTH // 2 - border_width // 2, y_offset - border_height // 2,
                border_width, border_height
            )
            pygame.draw.rect(self.screen, self.WHITE, border_rect, width=2)

            # Draw Track Text
            self.track_rects.append(border_rect)  # Use border_rect for click detection
            self.screen.blit(track_text, track_rect)
            y_offset += 50  # Increased spacing between options

        # Draw Confirmation Button
        pygame.draw.rect(self.screen, self.ACTIVE_COLOR, self.confirm_button, border_radius=5)
        confirm_text = self.button_font.render("CONFIRM", True, self.WHITE)
        self.screen.blit(confirm_text, confirm_text.get_rect(center=self.confirm_button.center))

        # Draw Back Button
        pygame.draw.rect(self.screen, self.ACTIVE_COLOR, self.back_button, border_radius=5)
        back_text = self.button_font.render("BACK", True, self.WHITE)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

    def handle_events(self, events):
        """Handle events for the music selector menu."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check Music Track Selection
                for i, track_rect in enumerate(self.track_rects):
                    if track_rect.collidepoint(mouse_pos):
                        self.current_track_index = i
                        self.play_preview(self.music_tracks[i][1])  # Play the selected track as a preview

                # Check Confirmation Button
                if self.confirm_button.collidepoint(mouse_pos):
                    selected_track = self.music_tracks[self.current_track_index][1]  # Return the full path
                    print(f"Confirmed Track: {selected_track}")
                    return "confirm", selected_track

                # Check Back Button
                if self.back_button.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Stop preview music
                    if self.original_track_path:  # Resume the original track
                        pygame.mixer.music.load(self.original_track_path)
                        pygame.mixer.music.play(-1)  # Play on repeat
                        self.previewing_track = self.original_track_path  # Update previewing track to original
                    return "back", None

        return None, None

    def run(self):
        """Run the music selector menu."""
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()  # Stop preview music on quit
                    if self.original_track_path:  # Resume the original track
                        pygame.mixer.music.load(self.original_track_path)
                        pygame.mixer.music.play(-1)  # Play on repeat
                        self.previewing_track = self.original_track_path  # Update previewing track to original
                    return "quit", None

            action, selected_track = self.handle_events(events)
            if action == "back":
                return "options", None
            elif action == "confirm":
                return "options", selected_track

            self.draw()
            pygame.display.flip()
