import pygame
from pygame import mixer
import sqlite3
from config_logIn import *

from screens.Loading import LoadingScreen
from screens.start_menu import StartMenu
import bcrypt
from screens.registration import RegistrationApp





import pygame
from pygame import mixer
import sqlite3
import bcrypt

class LoginScreen:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.db = sqlite3.connect("mydatabase.db")
        self.cursor = self.db.cursor()

        self.WIDTH, self.HEIGHT = 500, 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Login Screen")
        self.font = pygame.font.Font(None, 36)

        self.username_box = pygame.Rect(200, 100, 200, 40)
        self.password_box = pygame.Rect(200, 160, 200, 40)
        self.login_button = pygame.Rect(self.WIDTH//2 - 160, 230, 140, 50)
        self.new_user_button = pygame.Rect(self.WIDTH//2 + 20, 230, 140, 50)

        self.username = ""
        self.password = ""
        self.active_box = None
        self.password_hidden = True

        self.load_assets()
        self.play_music()

    def load_assets(self):
        self.sky = pygame.transform.scale(
            pygame.image.load("assets/images/others/sky.png").convert_alpha(), (self.WIDTH, self.HEIGHT)
        )
        self.grass = pygame.transform.scale(
            pygame.image.load("assets/images/others/grass.png"), (700, 75)
        )
        self.tree_left = pygame.transform.scale(
            pygame.image.load("assets/images/others/tree.png"), (150, 150)
        )

        self.title_text = pygame.transform.scale(
            pygame.image.load("assets/images/others/title.png"), (150, 40)
        )
        self.username_text = pygame.transform.scale(
            pygame.image.load("assets/images/others/username.png"), (150, 40)
        )
        self.password_text = pygame.transform.scale(
            pygame.image.load("assets/images/others/password.png"), (150, 40)
        )

    def play_music(self):
        mixer.music.load("assets/sounds/LogInTrack.mp3")
        mixer.music.play()

    def check_username(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()[0] > 0

    def check_password(self, entered_password, stored_hash):
        return bcrypt.checkpw(entered_password.encode(), stored_hash)

    def draw(self):
        self.screen.fill((255, 255, 255))  # WHITE

        self.screen.blit(self.sky, (0, 0))
        self.screen.blit(self.grass, (0, 325))  # GRASS_LOC_LOGIN
        self.screen.blit(self.tree_left, (0, 250))

        pygame.draw.rect(self.screen, (180, 140, 255) if self.active_box == "username" else (200, 200, 200), self.username_box, 2)  # LIGHT_PURPLE / GRAY
        pygame.draw.rect(self.screen, (180, 140, 255) if self.active_box == "password" else (200, 200, 200), self.password_box, 2)
        pygame.draw.rect(self.screen, (100, 0, 100), self.login_button)
        pygame.draw.rect(self.screen, (100, 0, 100), self.new_user_button)  # DARK_PURPLE

        self.screen.blit(self.title_text, (175, 30))  # TITLE_TEXT_LOC
        self.screen.blit(self.username_text, (30, 100))  # USERNAME_TEXT_LOC
        self.screen.blit(self.password_text, (30, 160))  # PASSWORD_TEXT_LOC

        username_surface = self.font.render(self.username, True, (0, 0, 0))
        self.screen.blit(username_surface, (self.username_box.x + 10, self.username_box.y + 10))

        password_display = "*" * len(self.password) if self.password_hidden else self.password
        password_surface = self.font.render(password_display, True, (0, 0, 0))
        self.screen.blit(password_surface, (self.password_box.x + 10, self.password_box.y + 10))

        login_text = self.font.render("Log In", True, (255, 255, 255))
        self.screen.blit(login_text, (self.login_button.x + 40, self.login_button.y + 10))

        new_user_text = self.font.render("New User", True, (255, 255, 255))
        self.screen.blit(new_user_text, (self.new_user_button.x + 10, self.new_user_button.y + 10))

        pygame.display.flip()

    def try_login(self):
        print(f"Logging in with:\nUsername: {self.username}\nPassword: {self.password}")
        if not self.check_username(self.username):
            from screens.ErrorScreen import ErrorScreen
            Error_Screen = ErrorScreen("invalid Username")
            Error_Screen.run()
            self.running = False
            
            print("Invalid username!")
            return

        self.cursor.execute("SELECT password FROM users WHERE username = ?", (self.username,))
        result = self.cursor.fetchone()
        if result:
            stored_hash = result[0]
            if self.check_password(self.password, stored_hash):
                print("Login successful!")
                start_menu = StartMenu(username=self.username)
                loading_screen = LoadingScreen(start_menu.run)
                loading_screen.run()
            else:
                print("Invalid password!")
                from screens.ErrorScreen import ErrorScreen
                Error_Screen = ErrorScreen("Incorrect password")
                Error_Screen.run()
                self.running = False
        else:
            print("Username not found in DB.")

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.username_box.collidepoint(event.pos):
                        self.active_box = "username"
                    elif self.password_box.collidepoint(event.pos):
                        self.active_box = "password"
                    elif self.login_button.collidepoint(event.pos):
                        self.try_login()
                    elif self.new_user_button.collidepoint(event.pos):
                     registration_page = RegistrationApp()  # You can define this class elsewhere
                     registration_page.run()  # You can define this screen class elsewhere
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
                            self.try_login()
                        else:
                            self.password += event.unicode

            self.draw()

        pygame.quit()


if __name__ == "__main__":
    login_screen = LoginScreen()
    login_screen.run()