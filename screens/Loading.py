import pygame
import config
import math

class LoadingScreen:
    def __init__(self, next_page):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.CLOUDX = 25
        self.CLOUDY = 150

        # Set up display
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Loading Screen")
        self.clock = pygame.time.Clock()

        self.TIMER_EVENT_STAR = pygame.USEREVENT + 1
        self.TIMER_EVENT_CLOUD = pygame.USEREVENT + 2
        self.TIMER_EVENT_FADEOUT = pygame.USEREVENT + 3

        pygame.time.set_timer(self.TIMER_EVENT_STAR, 150)
        pygame.time.set_timer(self.TIMER_EVENT_CLOUD, 100)
        pygame.time.set_timer(self.TIMER_EVENT_FADEOUT, 2000)

        # Load images
        self.tree = pygame.image.load("assets/images/others/tree.png")
        self.tree = pygame.transform.scale(self.tree, config.TREE_SIZE)

        self.grass = pygame.image.load("assets/images/others/grass.png")
        self.grass = pygame.transform.scale(self.grass, config.GRASS_SIZE)

        self.star = pygame.image.load("assets/images/others/star.png")
        self.star = pygame.transform.scale(self.star, config.STARSIZE)

        self.loading = pygame.image.load("assets/images/others/loading.png")
        self.loading = pygame.transform.scale(self.loading, config.LOADING_SIZE)

        self.cloud = pygame.image.load("assets/images/others/cloud.png")
        self.cloud = pygame.transform.scale(self.cloud, config.CLOUD_SIZE)

        self.next_page = next_page

    def updateCloud(self, dx, dy):
        if self.CLOUDX >= 700:
            self.CLOUDX = 25

        self.CLOUDX += dx
        self.CLOUDY += dy

        return self.CLOUDX, self.CLOUDY

    def run(self):
        running = True
        while running:
            self.screen.fill(config.LIGHT_PURPLE)  # Fill screen with light purple

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.TIMER_EVENT_STAR:
                    config.updateStar(config.STARDX, config.STARDY)

                time = pygame.time.get_ticks()
                CLOUD_DX = 10
                CLOUD_DY = math.trunc(math.sin(time) * 10)

                if event.type == self.TIMER_EVENT_CLOUD:
                    self.updateCloud(CLOUD_DX, CLOUD_DY)

                if event.type == self.TIMER_EVENT_FADEOUT:
                    self.next_page()
                    running = False

            self.screen.blit(self.star, (config.STARX, config.STARY))
            self.screen.blit(self.cloud, (self.CLOUDX, self.CLOUDY))
            self.screen.blit(self.grass, config.GRASS_LOC)
            self.screen.blit(self.tree, config.TREE_LOC)
            self.screen.blit(self.loading, config.LOADING_LOC)

            pygame.display.flip()  # Update display
            self.clock.tick(30)

        pygame.quit()

##xample usage:

# loading_screen = LoadingScreen(start_menu.run)
# loading_screen.run()



