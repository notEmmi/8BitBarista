import pygame
import pygame
from pygame import mixer
import settingsdata
from screens.pet_selector import PetSelector

class BuildingCongratzScreen:
    def __init__(self, image_path, playername, selected_character, username):
        pygame.init()
        mixer.init()

        self.img_path = image_path
        self.playername = playername
        self.selected_character = selected_character
        self.username = username
        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Start Adventure")

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BUTTON_COLOR = (245, 173, 66)
        self.BUTTON_HOVER = (255, 193, 86)
        self.BANNER_COLOR = (255, 226, 179)

        # Fonts
        self.font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 32)
        self.banner_font = pygame.font.Font(pygame.font.match_font("Irish Grover"), 36)

        # Load background and building image
        self.background = pygame.image.load("images/pinksky.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.building = pygame.image.load(self.img_path).convert_alpha()
        self.building_rect_size = 200
        self.building = pygame.transform.scale(self.building, (self.building_rect_size, self.building_rect_size))
        self.building_rect = self.building.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))

        # Button setup
        self.button_text = "Start Your Adventure"
        self.button_surface = self.font.render(self.button_text, True, self.BLACK)
        self.button_width = self.button_surface.get_width() + 40
        self.button_height = self.button_surface.get_height() + 20
        self.button_rect = pygame.Rect(
            self.WIDTH // 2 - self.button_width // 2,
            self.HEIGHT // 2 + 100,
            self.button_width,
            self.button_height
        )

        # Banner setup
        self.banner_height = 60
        self.banner_rect = pygame.Rect(0, 0, self.WIDTH, self.banner_height)
        self.banner_text = "ENJOY YOUR NEW HOME!"
        self.banner_surface = self.banner_font.render(self.banner_text, True, self.BLACK)
        self.banner_text_rect = self.banner_surface.get_rect(center=(self.WIDTH // 2, self.banner_height // 2))

        # Start music
        mixer.music.load("tracks/06 - Victory!.mp3")
        mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
        mixer.music.play()

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.building, self.building_rect.topleft)

            # Draw banner
            pygame.draw.rect(self.screen, self.BANNER_COLOR, self.banner_rect)
            self.screen.blit(self.banner_surface, self.banner_text_rect)

            # Draw button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.button_rect.collidepoint(mouse_pos)
            button_color = self.BUTTON_HOVER if is_hovering else self.BUTTON_COLOR

            pygame.draw.rect(self.screen, button_color, self.button_rect, border_radius=10)
            self.screen.blit(self.button_surface, (self.button_rect.centerx - self.button_surface.get_width() // 2,
                                                   self.button_rect.centery - self.button_surface.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        pet_selector = PetSelector(self.img_path, self.playername, self.selected_character, self.username)
                        pet_selector.run()
                        running = False

            pygame.display.flip()

        pygame.quit()
