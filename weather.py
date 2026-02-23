import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set a display mode (Fixes "No video mode has been set" error)
screen = pygame.display.set_mode((800, 600))

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RAIN_COUNT = 50
FLOOR_DROP_COUNT = 15  
RAIN_SPEED_X = -18  
RAIN_SPEED_Y = 26 
RAIN_COLOR = (80, 150, 255, 150)  # Blueish with transparency (RGBA)
RAIN_OPACITY = 150  # 150 out of 255 (semi-transparent)
DROP_SIZE = (8, 16)  # Raindrop size
CLOUDY_OPACITY = 100  # Opacity for the cloudy effect (0-255)

# Asset Directory
BASE_DIR = os.path.dirname(__file__)
RAIN_ASSET_DIR = os.path.join(BASE_DIR, "assets", "rain")

# Load Rain Drop Sprites
RAIN_SPRITES = [
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "drop_1.png")).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "drop_2.png")).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "drop_3.png")).convert_alpha(),
]

# Load Floor Drop Sprites
FLOOR_SPRITES = [
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "floor_1.png")).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "floor_2.png")).convert_alpha(),
    pygame.image.load(os.path.join(BASE_DIR, "assets", "rain", "floor_3.png")).convert_alpha(),
]

# Function to load, resize, and apply color & opacity to raindrop images
def load_and_modify_raindrop(image_path):
    """Loads, resizes, and applies color & opacity to a raindrop"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Raindrop image not found: {image_path}")

    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, DROP_SIZE)  # Resize

    # Create a new transparent surface
    colored_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    colored_image.fill(RAIN_COLOR)  # Apply color with transparency
    image.blit(colored_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Blend color
    return image

# Function to load, proportionally scale, and apply opacity to floor splashes
def load_and_modify_floor(image_path):
    """Loads floor splash image, scales it, and applies opacity"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Floor splash image not found: {image_path}")

    image = pygame.image.load(image_path).convert_alpha()
    
    # Maintain aspect ratio while making it fit within the raindrop's height
    original_width, original_height = image.get_size()
    scale_factor = DROP_SIZE[1] / original_height  # Scale based on height (10px)
    
    new_width = int(original_width * scale_factor)  # Maintain width proportion
    new_height = int(original_height * scale_factor)  # Should match raindrop height
    image = pygame.transform.scale(image, (new_width, new_height))

    # Create a semi-transparent surface
    transparent_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    transparent_surface.fill((255, 255, 255, RAIN_OPACITY))  # Apply opacity
    image.blit(transparent_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # Blend transparency
    return image

class Raindrop(pygame.sprite.Sprite):
    """Falling raindrop class"""
    def __init__(self, rain_sprites):
        super().__init__()

        # Ensure correct sprite selection
        self.image = random.choice(rain_sprites).copy()  

        # Adjust size to match weather.py behavior
        self.image = pygame.transform.scale(self.image, (8, 16))  # ✅ Set correct raindrop size

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH * 2)
        self.rect.y = random.randint(-SCREEN_HEIGHT * 2, 0)
        self.speed_x = RAIN_SPEED_X + random.randint(-2, 2)
        self.speed_y = RAIN_SPEED_Y + random.randint(-3, 3)

    def update(self, cam_x, cam_y, floor_group, floor_sprites):
        """Move raindrop diagonally and check for ground collision"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # If the raindrop reaches the ground, create a splash at its final X position
        if self.rect.y > SCREEN_HEIGHT:
            if random.random() < 0.4:  # 40% chance to create a floor splash
                screen_x = self.rect.x - cam_x  # Convert world to screen position
                screen_y = random.randint(0, SCREEN_HEIGHT)  # Fully random Y position

                # Pick a valid image
                selected_sprite = random.choice(floor_sprites)

                # Ensure it's copied before passing
                selected_sprite = selected_sprite.copy()
                floor_group.add(FloorDrop(screen_x, screen_y, selected_sprite))

            # Reset raindrop position after it falls
            self.rect.y = random.randint(-SCREEN_HEIGHT * 2, 0)
            self.rect.x = random.randint(0, SCREEN_WIDTH * 2)

class FloorDrop(pygame.sprite.Sprite):
    """Raindrop splash effect that stays FIXED in place."""
    def __init__(self, screen_x, screen_y, floor_sprite):
        super().__init__()

        # Apply transparency correction
        self.image = floor_sprite.copy().convert_alpha()
        self.image.set_colorkey((0, 0, 0))  # Set black as transparent (or adjust based on your asset)

        self.rect = self.image.get_rect()
        self.rect.x = max(0, min(screen_x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(screen_y, SCREEN_HEIGHT - self.rect.height))

        self.lifetime = 60  # Frames before disappearing
        self.alpha = 200  # Initial opacity

    def update(self):
        """Reduce lifetime of splash and gradually fade out."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Remove when expired

        self.alpha -= 8
        if self.alpha < 0:
            self.alpha = 0

        self.image.set_alpha(self.alpha)

class Rain:
    """Manages raindrops and floor splashes"""
    def __init__(self, rain_sprites=None, floor_sprites=None):
        self.raindrops = pygame.sprite.Group()
        self.floor_splashes = pygame.sprite.Group()

        # Load default sprites if not provided
        self.rain_sprites = rain_sprites or [
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "drop_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "drop_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "drop_3.png")).convert_alpha(),
        ]

        self.floor_sprites = floor_sprites or [
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "floor_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "floor_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(RAIN_ASSET_DIR, "floor_3.png")).convert_alpha(),
        ]

        for _ in range(RAIN_COUNT):
            self.raindrops.add(Raindrop(self.rain_sprites))

    def update(self, cam_x, cam_y):
        """Update rain movement relative to camera"""
        self.raindrops.update(cam_x, cam_y, self.floor_splashes, self.floor_sprites)
        self.floor_splashes.update()

    def draw(self, surface):
        """Draw floor splashes first, then falling raindrops."""
        self.floor_splashes.draw(surface)  # Draw floor splashes first
        self.raindrops.draw(surface)  # Then draw falling raindrops

class Cloudy:
    """Manages the cloudy weather effect"""
    def __init__(self):
        self.cloudy_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.cloudy_surface.fill((0, 0, 0, CLOUDY_OPACITY))  # Darken the screen with semi-transparency

    def draw(self, surface):
        """Draw the cloudy effect over the screen"""
        surface.blit(self.cloudy_surface, (0, 0))

# Example usage (for testing)
if __name__ == "__main__":
    clock = pygame.time.Clock()
    rain = Rain()
    cloudy = Cloudy()

    running = True
    while running:
        screen.fill((30, 30, 30))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        rain.update(0, 0)  
        rain.draw(screen)
        cloudy.draw(screen)  # Draw the cloudy effect

        pygame.display.flip()
        clock.tick(30)  

    pygame.quit()
