import pygame

pygame.init()

class CreditsScreen:
    def __init__(self):
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BROWN = (139, 69, 19)

        # Fonts
        self.font = pygame.font.Font(pygame.font.match_font("courier"), 50)

        # Back Button
        self.back_button = pygame.Rect(320, 500, 160, 50)  # Centered back button

    def show_credits(self, screen, events):
        screen.fill(self.BLACK)

        # Draw "CREDITS" Title
        credits_text = self.font.render("CREDITS", True, self.WHITE)
        screen.blit(credits_text, (400 - credits_text.get_width() // 2, 250))

        # Draw Back Button
        pygame.draw.rect(screen, self.BROWN, self.back_button, border_radius=10)
        back_text = self.font.render("BACK", True, self.WHITE)
        screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        # Handle Events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(pygame.mouse.get_pos()):
                    return "menu"  # Correct way: return a value

        return "credits"  # Stay on credits screen

# Example usage:
# credits = CreditsScreen()
# state = credits.show_credits(screen, events)
