import pygame
import sqlite3
import bcrypt
import sys

class RegistrationApp:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Register New User")
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.running = True

        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.PURPLE = (100, 0, 200)
        self.BLACK = (0, 0, 0)

        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()
        self.conn.commit()

        self.username = ""
        self.password = ""
        self.active_box = None
        self.message = ""

        self.username_box = pygame.Rect(270, 80, 200, 32)
        self.password_box = pygame.Rect(270, 130, 200, 32)
        self.register_button = pygame.Rect(190, 190, 100, 40)
        self.back_button = pygame.Rect(320, 190, 170, 40)
        
    

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def register_user(self):
        username = self.username.strip()
        password = self.password.strip()

        if not username or not password:
            self.message = "Please fill in both fields!"
            return

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            self.message = "Username already taken!"
            return

        encrypted_password = self.hash_password(password)
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))

        # Add initial save entry
        self.cursor.execute("""
            INSERT INTO saves (username, character, building, pet, day, weather, hour, minute)
            VALUES (?, ?, ?, ?, 1, 'sunny', 6, 0)
        """, (username, None, None, None))

        self.conn.commit()
        self.message = f"User '{username}' registered!"
        self.username = ""
        self.password = ""

    def draw(self):
        self.screen.fill(self.WHITE)

        background = pygame.image.load("images/reg_page_background.png")
        pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
        self.screen.blit(background, (0, 0))

        # Labels
        username_lbl = self.font.render("Username:", True, self.WHITE)
        password_lbl = self.font.render("Password:", True, self.WHITE)
        self.screen.blit(username_lbl, (150, 85))
        self.screen.blit(password_lbl, (150, 135))

        # Input boxes
        

        pygame.draw.rect(self.screen, self.GRAY if self.active_box != "username" else self.PURPLE, self.username_box, 2)
        pygame.draw.rect(self.screen, self.GRAY if self.active_box != "password" else self.PURPLE, self.password_box, 2)

        username_surf = self.font.render(self.username, True, self.BLACK)
        password_surf = self.font.render("*" * len(self.password), True, self.BLACK)

        self.screen.blit(username_surf, (self.username_box.x + 5, self.username_box.y + 5))
        self.screen.blit(password_surf, (self.password_box.x + 5, self.password_box.y + 5))

        # Buttons
        pygame.draw.rect(self.screen, self.PURPLE, self.register_button)
        pygame.draw.rect(self.screen, self.PURPLE, self.back_button)

        register_text = self.font.render("Register", True, self.WHITE)
        back_text = self.font.render("Already a User", True, self.WHITE)

        self.screen.blit(register_text, (self.register_button.x + 10, self.register_button.y + 5))
        self.screen.blit(back_text, (self.back_button.x + 5, self.back_button.y + 5))

        # Message
        message_surf = self.font.render(self.message, True, self.BLACK)
        self.screen.blit(message_surf, (150, 260))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_box.collidepoint(event.pos):
                        self.active_box = "username"
                    elif self.password_box.collidepoint(event.pos):
                        self.active_box = "password"
                    elif self.register_button.collidepoint(event.pos):
                        self.register_user()
                        from Log_In import LoginScreen  # Local import to avoid circular import
                        login_screen = LoginScreen()
                        login_screen.run()
                        self.running = False
                    elif self.back_button.collidepoint(event.pos):
                        from Log_In import LoginScreen  # Local import to avoid circular import
                        login_screen = LoginScreen()
                        login_screen.run()
                        self.running = False
                    else:
                        self.active_box = None

                elif event.type == pygame.KEYDOWN:
                    if self.active_box == "username":
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.active_box = "password"
                        else:
                            self.username += event.unicode
                    elif self.active_box == "password":
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.register_user()
                            from Log_In import LoginScreen  # Local import to avoid circular import
                            login_screen = LoginScreen()
                            login_screen.run()
                            self.running = False
                        else:
                            self.password += event.unicode

            self.draw()

        self.conn.close()
        pygame.quit()
        sys.exit()

# Test directly
if __name__ == "__main__":
    app = RegistrationApp()
    app.run()
