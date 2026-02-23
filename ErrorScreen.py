import pygame
import settingsdata
from pygame import mixer
from Log_In import LoginScreen


class ErrorScreen:
    def __init__(self, message="An error occurred"):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.RED = (200, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 40

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Error Screen")
        self.clock = pygame.time.Clock()

        self.message = message
        self.font = pygame.font.Font(None, self.FONT_SIZE)
        self.small_font = pygame.font.Font(None, 28)

        self.darkbg = pygame.image.load("assets/images/others/darkbg.png")
        self.darkbg = pygame.transform.scale(self.darkbg, (self.WIDTH, self.HEIGHT))

        self.errorsign = pygame.image.load("assets/images/others/errorsign_transparent.png")
        self.errorsign = pygame.transform.scale(self.errorsign, (250, 400))

        self.cloud = pygame.image.load("assets/images/others/rain_transparent.png")
        self.cloud = pygame.transform.scale(self.cloud, (100, 100))

        mixer.init()
        mixer.music.load("assets/sounds/error.mp3")
        mixer.music.set_volume(settingsdata.volumes[0] * settingsdata.volumes[1])
        mixer.music.play()

    def run(self):
     running = True
     while running:
        self.screen.blit(self.darkbg, (0, 0))
        self.screen.blit(self.errorsign, ((self.WIDTH / 2) - 125, (self.HEIGHT / 2) - 100))
        self.screen.blit(self.cloud, ((self.WIDTH / 2) - 50, (self.HEIGHT / 2) - 250))
        self.screen.blit(self.cloud, ((self.WIDTH / 2) - 250, (self.HEIGHT / 2) - 250))
        self.screen.blit(self.cloud, ((self.WIDTH / 2) + 150, (self.HEIGHT / 2) - 250))

        # Render error message
        message_surface = self.font.render(self.message, True, self.WHITE)
        message_rect = message_surface.get_rect(center=(self.WIDTH / 2, self.HEIGHT - 400))

        # Add padding to the background box
        padding_x = 20
        padding_y = 10
        box_rect = pygame.Rect(
            message_rect.left - padding_x,
            message_rect.top - padding_y,
            message_rect.width + 2 * padding_x,
            message_rect.height + 2 * padding_y
        )

        # Draw shadow (bottom-right)
        shadow_rect = box_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (50, 50, 50), shadow_rect, border_radius=10)

        # Draw highlight (top-left)
        highlight_rect = box_rect.copy()
        highlight_rect.x -= 2
        highlight_rect.y -= 2
        pygame.draw.rect(self.screen, (255, 255, 255), highlight_rect, border_radius=10)

        # Draw main box
        pygame.draw.rect(self.screen, self.RED, box_rect, border_radius=10)

        # Blit the message text on top
        self.screen.blit(message_surface, message_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    login_screen = LoginScreen()
                    login_screen.run()
                    running = False

        self.clock.tick(30)
        pygame.display.flip()

    pygame.quit()