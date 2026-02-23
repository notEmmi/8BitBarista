import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Controls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)
header_font = pygame.font.Font(None, 48)

# Instructions Data
instructions = {
    "Farming": [
        "1 - Choose the hoe tool",
        "2 - Choose tomato seed",
        "3 - Open seed pouch",
        "4 - Open bag"
    ],
    "Cafe": [
        "Click - Clicking does everything"
    ]
}

def draw_controls_screen():
    screen.fill(WHITE)
    
    title_text = header_font.render("Controls", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    y_offset = 150
    for category, commands in instructions.items():
        # Draw category header
        category_text = font.render(category, True, BLACK)
        screen.blit(category_text, (100, y_offset))
        y_offset += 40
        
        # Draw instructions
        for command in commands:
            command_text = font.render(command, True, BLACK)
            screen.blit(command_text, (120, y_offset))
            y_offset += 30
    
    pygame.display.flip()

def main():
    running = True
    show_controls = False
    
    while running:
        screen.fill(GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_controls = not show_controls
        
        if show_controls:
            draw_controls_screen()
        else:
            default_text = font.render("Press ESC to view controls", True, BLACK)
            screen.blit(default_text, (WIDTH // 2 - default_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
