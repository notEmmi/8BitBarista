import pygame
import pytmx
import os
import time
from weather import Rain, Raindrop, FloorDrop, Cloudy
from toolbar import Toolbox
import interactions
import customers
import store
import inventory
import random
import screens.start_menu as start_menu
import subprocess
import settingsdata
import subprocess
from pygame_gui import UI_BUTTON_PRESSED
from fish import run_fishing_minigame
from screens.music_selector import MusicSelector
import sqlite3
from GameState import GameState
from fish import run_fishing_minigame
import inventorydata

class Game:
    def __init__(self, chosen_building, petChoice, name, selected_character="boy1", current_day = 1, current_weather="sunny", time_hour=None, time_minute=None, fromPriorMenu = False, gameData = None, username=None):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        # Screen Size
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600

        # initializing rain
        self.rain = Rain()
        self.raining = False

        # Initalize cloudy weather
        self.cloudy = Cloudy()
        self.cloudy_weather = False
        
        
        self.house = chosen_building
        self.pet = petChoice
        self.playername = name
        self.username = username

        self.shop = store.ShopUI(self)
        self.selected_character = selected_character
        self.current_weather = current_weather
        self.apply_weather_effects()
        self.time_hour = time_hour
        self.time_minute = time_minute

        if self.time_hour is not None and self.time_minute is not None:
            self.resume_start_minutes = self.time_hour * 60 + self.time_minute
        else:
            self.resume_start_minutes = 6 * 60  # fallback to default

            self.game_start_time = time.time()  # Reset base time reference
            self.last_game_time = self.game_start_time  # For pause/resume support

    
        # Create Dark Rain Overlay
       
       
        self.rain_overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rain_overlay.fill((0, 0, 0, 100))  # Semi-transparent black layer (100/255 opacity)

        # Day transition
        self.current_day = current_day
        self.last_processed_day = 0
        self.weather_icons = {
            "sunny": pygame.image.load(os.path.join("assets", "icons", "sunny.png")).convert_alpha(),
            "cloudy": pygame.image.load(os.path.join("assets", "icons", "cloudy.png")).convert_alpha(),
            "rainy": pygame.image.load(os.path.join("assets", "icons", "rainy.png")).convert_alpha(),
            "moon": pygame.image.load(os.path.join("assets", "icons", "moon.png")).convert_alpha()
        }
        self.is_paused = False
        self.show_new_day_prompt = False
        self.confirm_new_day = False
        self.last_game_time = time.time()

        # Camera Zoom Factor (2x Zoom)
        self.ZOOM_FACTOR = 2.0

        # Adjusted Screen Size for the Camera View
        self.CAMERA_WIDTH = int(self.SCREEN_WIDTH / self.ZOOM_FACTOR)
        self.CAMERA_HEIGHT = int(self.SCREEN_HEIGHT / self.ZOOM_FACTOR)

        # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("8-Bit Barista")

        # File Paths
        self.BASE_DIR = os.path.dirname(__file__)
        self.MAP_PATH = os.path.join(self.BASE_DIR, "assets", "map")
        self.SOUND_PATH = os.path.join(self.BASE_DIR, "assets", "sounds")

        # Load TMX Map
        self.load_map(os.path.join(self.MAP_PATH, "map.tmx"))

        # Extract Tile Size
        self.TILE_WIDTH = self.tmx_data.tilewidth
        self.TILE_HEIGHT = self.tmx_data.tileheight
        self.MAP_WIDTH = self.tmx_data.width * self.TILE_WIDTH
        self.MAP_HEIGHT = self.tmx_data.height * self.TILE_HEIGHT

        # Player Constants
        self.PLAYER_SPEED = 2

        # Load Rain Drop Sprites
        self.RAIN_SPRITES = [
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "drop_3.png")).convert_alpha(),
        ]

        # Load Floor Drop Sprites
        self.FLOOR_SPRITES = [
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_1.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_2.png")).convert_alpha(),
            pygame.image.load(os.path.join(self.BASE_DIR, "assets", "rain", "floor_3.png")).convert_alpha(),
        ]

        for sprite in self.FLOOR_SPRITES:
            sprite.set_colorkey((0, 0, 0))  # Remove black background for transparency

        # Initialize Rain system with loaded textures
        self.rain = Rain(rain_sprites=self.RAIN_SPRITES, floor_sprites=self.FLOOR_SPRITES)

        # Characters list
        characters = ["boy1", "boy2", "boy3", "girl1", "girl2", "girl3"]

        # Load char from DB
        self.selected_character = self.load_selected_character_from_db()
        print(f"Loaded character: {self.selected_character}")
        
        self.SPRITE_PATH = os.path.join(self.BASE_DIR, "assets", "images", "character-selection")

        # Manually load sprite sheets for all characters
        self.ANIMATION_FRAMES = {}
        for character in characters:
            self.ANIMATION_FRAMES[character] = {
                "down": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "down_1.png")).convert_alpha(),
                         pygame.image.load(os.path.join(self.SPRITE_PATH, character, "down_2.png")).convert_alpha()],
                "up": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "up_1.png")).convert_alpha(),
                       pygame.image.load(os.path.join(self.SPRITE_PATH, character, "up_2.png")).convert_alpha()],
                "left": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "left_1.png")).convert_alpha(),
                         pygame.image.load(os.path.join(self.SPRITE_PATH, character, "left_2.png")).convert_alpha()],
                "right": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "right_1.png")).convert_alpha(),
                          pygame.image.load(os.path.join(self.SPRITE_PATH, character, "right_2.png")).convert_alpha()],
                "idle_down": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "down_idle.png")).convert_alpha()],
                "idle_up": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "up_idle.png")).convert_alpha()],
                "idle_left": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "left_idle.png")).convert_alpha()],
                "idle_right": [pygame.image.load(os.path.join(self.SPRITE_PATH, character, "right_idle.png")).convert_alpha()],
            }

        # Get sprite size
        self.SPRITE_WIDTH, self.SPRITE_HEIGHT = self.ANIMATION_FRAMES[self.selected_character]["down"][0].get_width(), self.ANIMATION_FRAMES[self.selected_character]["down"][0].get_height()

        # Player Setup (Start in the middle of the map)
        self.player_x, self.player_y = self.MAP_WIDTH // 2, self.MAP_HEIGHT // 2
        self.player_direction = "idle_down"  # Default idle position
        self.animation_index = 0
        self.animation_timer = 0

        # Camera Position (Starts Centered)
        self.camera_x, self.camera_y = self.player_x - self.CAMERA_WIDTH // 2, self.player_y - self.CAMERA_HEIGHT // 2

        # Create a surface for rendering with zoom applied
        self.camera_surface = pygame.Surface((self.CAMERA_WIDTH, self.CAMERA_HEIGHT))

        # Game Time System (Stardew Valley Timing)
        self.SECONDS_PER_GAME_MINUTE = 0.7  # 10 minutes = 7 seconds in real life
        self.GAME_START_HOUR = 6  # 6:00 AM
        self.game_start_time = time.time()  # Real-world start time
        self.time_multiplier = 1  # Normal speed, increased when pressing ''
      
        self.backpack = pygame.Rect(0,0,0,0)

        #Initialize Water GID and Layer
        self.water_gids = [
            self.get_gid("Water", 0),
            self.get_gid("Water", 1),
            self.get_gid("Water", 2),
            self.get_gid("Water", 3)
        ]
        self.water_layer = self.tmx_data.get_layer_by_name("Water")

        #Gold
        self.gold = 100

        # Load and play background music
        self.background_music = os.path.join(self.SOUND_PATH, "1_new_life_master.mp3")
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)  # Play on repeat

        self.toolbox = Toolbox()
        self.toolbox.selected_tool = -1  # Ensure no tool is selected initially

        self.pauseButton = pygame.Rect(0, 0, 0, 0)

        self.gameData = gameData
        if fromPriorMenu and gameData: 
            self.loadGameState()

        

######## start of save data functions //////////////////////////////////
    
    def load_selected_character_from_db(self):
        conn = sqlite3.connect("mydatabase.db")
        game_state = GameState.load_from_db(conn, self.username)
        conn.close()

        if game_state is None:
            print(f"[DEBUG] No save found for user {self.username}, defaulting to selected_character from menu")
            return self.selected_character if hasattr(self, 'selected_character') else None

        return game_state.selected_character

################ end save data functions ###########################

    def load_map(self, map_file):
        """Load TMX map and extract collidable and building objects."""
        self.tmx_data = pytmx.load_pygame(map_file, load_all_tiles=True)
        self.collidable_objects = [
            pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.tmx_data.objects
            if obj.name == "Collisions" or obj.properties.get("collidable", False)
        ]
        self.buildings_object = {
            obj.properties.get("building"): pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.tmx_data.objects
            if obj.properties.get("building")
        }

        # Debug: Draw red circles around building objects
        for building_name, rect in self.buildings_object.items():
            pygame.draw.circle(self.screen, (255, 0, 0), (rect.centerx, rect.centery), 10, 2)

    def move_player(self, move_x, move_y):
        # Calculate new position and define player's hitbox
        new_x, new_y = self.player_x + move_x, self.player_y + move_y
        hitbox = pygame.Rect(new_x, new_y + 5, self.SPRITE_WIDTH, self.SPRITE_HEIGHT - 10)

        # Prevent movement if collision detected
        if any(hitbox.colliderect(obj) for obj in self.collidable_objects):
            return

        # Update position if no collision
        self.player_x, self.player_y = new_x, new_y

    def draw_map(self, surface, cam_x, cam_y):
        """Draws the visible map layers and objects within the camera view."""
        # Draw tile layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid:  # Skip empty tiles
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        tile_x, tile_y = x * self.TILE_WIDTH - cam_x, y * self.TILE_HEIGHT - cam_y
                        if -self.TILE_WIDTH <= tile_x < self.CAMERA_WIDTH and -self.TILE_HEIGHT <= tile_y < self.CAMERA_HEIGHT:
                            surface.blit(tile, (tile_x, tile_y))

        # Draw objects (e.g., trees, buildings)
        for obj in self.tmx_data.objects:
           target_id = 315
           target_id2 = 139  # ID of the object using house2.png
           obj_x = obj.x - cam_x
           obj_y = obj.y - cam_y

           if obj.id == target_id:
        # Always override this tile's image
              custom_path = self.house  # Your dynamic path
              custom_image = pygame.image.load(custom_path).convert_alpha()
              custom_image = pygame.transform.scale(custom_image, (int(obj.width), int(obj.height)))
              surface.blit(custom_image, (obj_x, obj_y))
              continue

           
           if obj.id == target_id2:
               custom_path2 = self.pet
               custom_image2 = pygame.image.load(custom_path2).convert_alpha()
               custom_image2 = pygame.transform.scale(custom_image2, (int(obj.width+15), int(obj.height+15))) 
               surface.blit(custom_image2, (obj_x, obj_y))
               continue
           else:
        # Default behavior
               image = self.tmx_data.get_tile_image_by_gid(obj.gid)
               if image:
                   surface.blit(image, (obj_x, obj_y))
        
        # Debug: Draw red collision boxes
        # for rect in self.collidable_objects:
        #     pygame.draw.rect(surface, (255, 0, 0), 
        #                     (rect.x - cam_x, rect.y - cam_y, rect.width, rect.height), 2)

    def get_game_time(self):
        """Converts real-time seconds to in-game hours and minutes."""
        if self.is_paused:
            # Freeze time
            elapsed_time = (self.last_game_time - self.game_start_time) * self.time_multiplier
        else:
            elapsed_time = (time.time() - self.game_start_time) * self.time_multiplier
            self.last_game_time = time.time()

        # How many game minutes have passed since start
        elapsed_game_minutes = int(elapsed_time / self.SECONDS_PER_GAME_MINUTE)

        # Use resume_start_minutes if it exists, otherwise fall back to GAME_START_HOUR
        if hasattr(self, "resume_start_minutes"):
            total_game_minutes = self.resume_start_minutes + elapsed_game_minutes
        else:
            total_game_minutes = self.GAME_START_HOUR * 60 + elapsed_game_minutes

        game_hour = (total_game_minutes // 60) % 24
        game_minute = total_game_minutes % 60

        return game_hour, game_minute
    
    def set_game_time(self, hour, minute):
        """
        Set the game time to a specific hour and minute.
        """
        # Calculate the total minutes since midnight
        total_minutes_since_midnight = hour * 60 + minute

        # Fully reset time
        self.resume_start_minutes = total_minutes_since_midnight
        self.game_start_time = time.time()
        self.last_game_time = self.game_start_time

    def is_night_time(self):
        """Returns True if the current game time is night (after 5:30 PM or before 6 AM)."""
        game_hour, game_minute = self.get_game_time()
        total_minutes = game_hour * 60 + game_minute  # Convert to total minutes since midnight

        return total_minutes >= 1050 or total_minutes < 360  # 1050 = 5:30 PM, 360 = 6:00 AM
   
    def draw_night_filter(self):
        """Applies a transparent gradient for nighttime effect without duplicating overlays."""
        game_hour, game_minute = self.get_game_time()
        total_minutes = game_hour * 60 + game_minute

        start_night_transition = 17 * 60 + 30  # 5:30 PM
        end_night_transition = 18 * 60  # 6:00 PM

        start_morning_transition = 5 * 60 + 30  # 5:30 AM
        end_morning_transition = 6 * 60  # 6:00 AM

        transition_progress = 0  # Default to no overlay

        # Determine transition progress
        if start_night_transition <= total_minutes <= end_night_transition:  
            # Nighttime transition (5:30 PM - 5:40 PM)
            transition_progress = (total_minutes - start_night_transition) / (end_night_transition - start_night_transition)
        elif start_morning_transition <= total_minutes <= end_morning_transition:  
            # Morning transition (5:50 AM - 6:00 AM) → Fade out night filter
            transition_progress = 1 - ((total_minutes - start_morning_transition) / (end_morning_transition - start_morning_transition))
        elif total_minutes > end_night_transition or total_minutes < start_morning_transition:
            # Fully dark at night
            transition_progress = 1

        # If fully daylight, return 0 alpha (no effect)
        if transition_progress == 0:
            return 0  

        # Calculate alpha value for overlay
        alpha_value = int(transition_progress * 180)  # Max opacity at night

        return alpha_value

    def apply_weather_effects(self):
        from weather import Rain, Cloudy  # Import here to avoid circular issues

        print(f"[DEBUG] Applying weather effects for: {self.current_weather}")

        if self.current_weather == "rainy":
            self.raining = True
            self.cloudy_weather = False
            self.rain = Rain()
            self.cloudy = None
        elif self.current_weather == "cloudy":
            self.raining = False
            self.cloudy_weather = True
            self.cloudy = Cloudy()
            self.rain = None
        else:
            self.raining = False
            self.cloudy_weather = False
            self.rain = None
            self.cloudy = None

    def check_new_day(self):
        game_hour, game_minute = self.get_game_time()
        total_game_minutes = game_hour * 60 + game_minute
        
        # Calculate current day based on time passed
        days_passed = (total_game_minutes - 330) // (24 * 60) + 1  # 330 = 5:30 AM
        
        if days_passed > self.current_day:
            self.current_day = days_passed
            # First day is always sunny, others random
            if self.current_day == 1:
                self.current_weather = "sunny"
            else:
                self.current_weather = random.choice(["sunny", "cloudy", "rainy"])
            
            # Set weather states based on new weather
            self.raining = self.current_weather == "rainy"
            self.cloudy_weather = self.current_weather == "cloudy"
            print(f"Day {self.current_day} - Weather: {self.current_weather}")
    
    def check_for_new_day_prompt(self):
        game_hour, game_minute = self.get_game_time()
        
        # Check if it's 2:00 AM and the prompt hasn't been shown yet
        if game_hour == 2 and game_minute == 0 and not self.show_new_day_prompt:
            self.is_paused = True  # Pause the game
            self.show_new_day_prompt = True  # Show the prompt
    
    def draw_new_day_prompt(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Dark semi-transparent overlay
        self.screen.blit(overlay, (0, 0))

        # Create a dialog box
        dialog_width = 500
        dialog_height = 150
        dialog_x = (self.SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (self.SCREEN_HEIGHT - dialog_height) // 2

        pygame.draw.rect(self.screen, (50, 50, 50), (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # Draw the prompt text
        prompt_text = self.font.render("Your character is exhausted.", True, (255, 255, 255))
        prompt_text2 = self.font.render("Press [Enter] to start a new day.", True, (255, 255, 255))

        text_rect = prompt_text.get_rect(center=(self.SCREEN_WIDTH // 2, dialog_y + 50))
        text_rect2 = prompt_text2.get_rect(center=(self.SCREEN_WIDTH // 2, dialog_y + 90))

        self.screen.blit(prompt_text, text_rect)
        self.screen.blit(prompt_text2, text_rect2)

    def draw_hud(self):
        """Displays 'Day X' on top, with the Weather Icon and Clock properly aligned at the top-right."""

       

        # Load a Smaller & Thinner Font
        clock_font = pygame.font.Font(None, 30)  # Smaller size & thinner weight
        day_font = pygame.font.Font(None, 25)  # Smaller size & thinner weight

        # Create HUD Panel Background
        """Displays 'Day X' on top, with the Weather Icon and Clock properly aligned at the top-right."""

        # Define Panel Dimensions & Styling
        panel_x_margin = 12  # Space between panel and screen edges
        panel_y_margin = 8
        panel_width = 150 # Unified width
        panel_height = 100  # Height to fit stacked elements
        border_radius = 8  # Rounded corners

        # Load a Smaller & Thinner Font
        clock_font = pygame.font.Font(None, 30)  # Smaller size & thinner weight
        day_font = pygame.font.Font(None, 25)
        name_font = pygame.font.Font(None, 25)  # Smaller size & thinner weight

        # Create HUD Panel Background
        hud_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(
            hud_surface, (99, 55, 44, 240), (0, 0, panel_width, panel_height), border_radius=border_radius
        )

        # "Day X" - Positioned at the top with internal padding
        day_text = day_font.render(f"Day {self.current_day}", True, (255, 255, 255))
        day_rect = day_text.get_rect(midtop=(panel_width // 2, panel_y_margin))  # Centered horizontally
        
        name_text = name_font.render(self.playername, True,(255, 255, 255))
        name_rect = name_text.get_rect(midtop=(panel_width // 2 + 600 , panel_y_margin +80))

        
        hud_surface.blit(day_text, day_rect.topleft)

        # Clock - Fixed Position (Independent)
        clock_text = f"{self.get_game_time()[0]:02}:{self.get_game_time()[1]:02}"
        time_surface = clock_font.render(clock_text, True, (255, 255, 255))
        pygame.draw.rect(
            hud_surface, (99, 55, 44, 240), (0, 0, panel_width, panel_height), border_radius=border_radius
        )

        # "Day X" - Positioned at the top with internal padding
        day_text = day_font.render(f"Day {self.current_day}", True, (255, 255, 255))
        day_rect = day_text.get_rect(midtop=(panel_width // 2, panel_y_margin))  # Centered horizontally
        hud_surface.blit(day_text, day_rect.topleft)

        # Determine if it's daytime (adjust if needed)
        current_hour = self.get_game_time()[0]
        is_daytime = 6 <= current_hour < 18

        # Dynamically select icon for sunny days (moon at night)
        icon_key = self.current_weather
        if self.current_weather == "sunny" and not is_daytime:
            icon_key = "moon"

        # Weather Icon - Adjust Position Based on Type
        if icon_key in self.weather_icons:
            weather_icon = pygame.transform.scale(self.weather_icons[icon_key], (28, 28))
            icon_x = 8  # Fixed left alignment

            # Adjust icon height based on type
            if icon_key == "sunny":
                icon_y = day_rect.bottom + 5
            elif icon_key in ["cloudy", "rainy"]:
                icon_y = day_rect.bottom + 2
            else:  # moon or fallback
                icon_y = day_rect.bottom + 5

            hud_surface.blit(weather_icon, (icon_x, icon_y))
        else:
            print(f"WARNING: Missing weather icon for {icon_key}")

        # Clock - Fixed Position (Independent)
        clock_text = f"{self.get_game_time()[0]:02}:{self.get_game_time()[1]:02}"
        time_surface = clock_font.render(clock_text, True, (255, 255, 255))
        
        clock_x = panel_width - 70  # Shift clock right, away from the icon
        clock_y = day_rect.bottom + 8  # Position slightly lower for visual balance

        hud_surface.blit(time_surface, (clock_x, clock_y))  # Now truly independent

        # Move Panel to the Top-Right of the Screen with Proper Margins
        screen_x = self.SCREEN_WIDTH - panel_width - panel_x_margin  # Fixed position
        screen_y = panel_y_margin  # Fixed vertical margin
        self.screen.blit(hud_surface, (screen_x, screen_y))
        clock_x = panel_width - 70  # Shift clock right, away from the icon
        clock_y = day_rect.bottom + 8  # Position slightly lower for visual balance

        hud_surface.blit(time_surface, (clock_x, clock_y))  # Now truly independent

        # Move Panel to the Top-Right of the Screen with Proper Margins
        screen_x = self.SCREEN_WIDTH - panel_width - panel_x_margin  # Fixed position
        screen_y = panel_y_margin  # Fixed vertical margin
        self.screen.blit(hud_surface, (screen_x, screen_y))
        self.screen.blit(name_text, name_rect.topleft )

    def handle_input(self):
        """Handles keyboard and mouse input, including time acceleration and tool usage."""
        keys = pygame.key.get_pressed()

        # Accelerate time with 'b', reset multiplier when released
        if not self.is_paused:
            new_multiplier = 10 if keys[pygame.K_b] else 1
            if new_multiplier != self.time_multiplier:
                elapsed_time = time.time() - self.game_start_time
                self.game_start_time = time.time() - (elapsed_time * self.time_multiplier / new_multiplier)
                self.time_multiplier = new_multiplier

        # Trigger interactions, customers, or shop with respective keys
        # The following keybinds have been replaced by left click
        # if keys[pygame.K_TAB]: 
        #     print("pressed TAB")
        #     conn = sqlite3.connect("mydatabase.db")
        #     curr_hour, curr_minute = self.get_game_time()
        #     game_state = GameState(self.house, self.pet, self.playername, self.selected_character, self.current_day, self.current_weather, curr_hour, curr_minute, False, None)
        #     game_state.save_to_db(conn)
        #     conn.close()
        # if keys[pygame.K_CAPSLOCK]: 
        #     customers_ui= customers.CustomerUI(self)
        #     customers_ui.run()
        # if keys[pygame.K_LSHIFT]: 
            # shop_ui = shop.ShopUI(self)
            # shop_ui.run()

        # Set specific times with 'n' (5 PM) and 'm' (1:30 AM)
        if keys[pygame.K_n] and not self.is_paused: self.set_game_time(17, 0)
        if keys[pygame.K_m] and not self.is_paused: self.set_game_time(1, 30)

        # open inventory
        if keys[pygame.K_e]: inventory.run(self)
        
        # Handle events (e.g., quitting, toggling weather, tool selection)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Toggle rain
                    self.raining = not self.raining
                    print(f"Rain Enabled: {self.raining}")
                if event.key == pygame.K_c:  # Toggle cloudy weather
                    self.cloudy_weather = not self.cloudy_weather
                    print(f"Cloudy Weather Enabled: {self.cloudy_weather}")
                if self.show_new_day_prompt and event.key == pygame.K_RETURN:  # Confirm new day
                    self.time_multiplier, self.confirm_new_day, self.show_new_day_prompt, self.is_paused = 1, True, False, False
                if pygame.K_1 <= event.key <= pygame.K_4:  # Tool or seed selection
                    if self.toolbox.seed_inventory_open:
                        selected_seed_index = event.key - pygame.K_1
                        if self.toolbox.selected_seed == selected_seed_index:
                            # Close seed inventory and deselect seed pouch
                            self.toolbox.close_seed_inventory()
                            self.toolbox.selected_tool = -1
                        else:
                            self.toolbox.select_seed(selected_seed_index)
                    else:
                        self.toolbox.select_tool(event.key - pygame.K_1)

            # Handle mouse input for tool usage and building interactions
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                if self.pauseButton.collidepoint(mouse_x, mouse_y): return self.pauseTheGame()
                elif self.backpack.collidepoint(mouse_x, mouse_y): return inventory.run(self)
                adjusted_x = (mouse_x // self.ZOOM_FACTOR) + self.camera_x
                adjusted_y = (mouse_y // self.ZOOM_FACTOR) + self.camera_y
                tile_x, tile_y = int(adjusted_x // self.TILE_WIDTH), int(adjusted_y // self.TILE_HEIGHT)
                print(f"Mouse: ({mouse_x}, {mouse_y}), Adjusted: ({adjusted_x}, {adjusted_y}), Tile: ({tile_x}, {tile_y})")

                clicked_gid = self.water_layer.data[tile_y][tile_x]
                if clicked_gid in self.water_gids:
                    print("Water tile clicked! Launching fishing game...")
                    self.gold += run_fishing_minigame()
                    # result = subprocess.Popen(["python", "fish.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # # Capture the output from the subprocess
                    # stdout, stderr = result.communicate()

                    # # Ensure no errors occurred and the output is not empty
                    # if result.returncode == 0 and stdout.strip():
                    #     try:
                    #         # Split the output by lines and get the last line, which should be the gold value
                    #         output_lines = stdout.strip().splitlines()

                    #         # If the output contains the Pygame version info or anything unexpected, filter it out
                    #         gold_value_str = None
                    #         for line in output_lines:
                    #             # Try to find a numeric line (this should be the gold value)
                    #             if line.isdigit():
                    #                 gold_value_str = line
                    #                 break

                    #         if gold_value_str:
                    #             # Try converting the last line to an integer
                    #             self.gold += int(gold_value_str)
                    #         else:
                    #             print(f"Error: No valid gold output found in '{stdout}'.")

                    #     except ValueError:
                    #         print(f"Error: The output '{stdout}' cannot be converted to an integer.")
                    # else:
                    #     if result.returncode != 0:
                    #         print("Error:", stderr)  # Handle any errors that occurred during execution of fish.py
                    #     else:
                    #         print("No valid gold output received from fish.py.")
                # Check if the mouse click is within any building rectangle first
                for building_name, rect in self.buildings_object.items():
                    if rect.collidepoint(adjusted_x, adjusted_y):
                        print(f"{building_name.capitalize()} clicked!")
                        if building_name == "cafe":
                            # Open the cafe UI
                            interactions_ui = interactions.InteractionsUI(self)
                            interactions_ui.run()
                            # customers_ui = customers.CustomerUI(self)
                            # customers_ui.run()
                        elif building_name == "store":
                            # Open the store UI
                            self.shop.run()
                        return  # Exit early if a building was clicked

                # If no building was clicked, use the tool
                self.use_tool(tile_x, tile_y)

    def place_tile(self, layer_name, tile_x, tile_y, tile_gid):
        """Places a tile with the given GID at the specified coordinates in the specified layer."""
        layer = self.tmx_data.get_layer_by_name(layer_name)
        if layer:
            layer.data[tile_y][tile_x] = tile_gid
            self.update_map(layer_name, layer.data)

    def get_tileset_by_name(self, tileset_name):
        """Finds a tileset by name in the TMX map."""
        return next((tileset for tileset in self.tmx_data.tilesets if tileset.name == tileset_name), None)

    def get_gid(self, tileset_name, tile_index):
        """Gets the GID (Global ID) of a tile from the given tileset and index."""
        tileset = self.get_tileset_by_name(tileset_name)
        if not tileset:
            print(f"Tileset '{tileset_name}' not found")
            return None
        return self.tmx_data.map_gid(tileset.firstgid + tile_index)[0][0]
    
    def use_tool(self, tile_x, tile_y):
        print(f"Using tool at tile ({tile_x}, {tile_y}) with selected tool {self.toolbox.selected_tool}")
        if self.toolbox.selected_tool == -1:
            print("No tool selected"); return

        if self.toolbox.selected_tool == 0:  # Hoe
            dirt_id = self.get_gid("Tilled_Dirt", 12)
            self.place_tile("Dirt", tile_x, tile_y, dirt_id)
            print(f"Tilled soil at ({tile_x}, {tile_y})")

        elif self.toolbox.selected_tool == 1:  # Seed pouch
            if self.toolbox.selected_seed is not None:
                seed_name = self.toolbox.seed_slots[self.toolbox.selected_seed]
                dirt_layer = self.tmx_data.get_layer_by_name("Dirt")
                plant_layer = self.tmx_data.get_layer_by_name("Plants")
                dirt_id = self.get_gid("Tilled_Dirt", 12)
                if dirt_layer.data[tile_y][tile_x] == dirt_id:  # Check if tile is tilled
                    if plant_layer.data[tile_y][tile_x] == 0:  # Check if tile is not occupied
                        seed_gid = self.get_seed_gid(seed_name)
                        self.place_tile("Plants", tile_x, tile_y, seed_gid)
                    else:
                        print(f"Tile ({tile_x}, {tile_y}) is already occupied.")

        elif self.toolbox.selected_tool == 2:  # Watering can
            dirt_layer = self.tmx_data.get_layer_by_name("Dirt")
            dirt_id, watered_id = self.get_gid("Tilled_Dirt", 12), self.get_gid("Tilled_Dirt", 56)
            if dirt_layer and dirt_layer.data[tile_y][tile_x] == dirt_id:  # Check if tile is tilled
                self.place_tile("Watered", tile_x, tile_y, watered_id)

        elif self.toolbox.selected_tool == 3:  # Harvesting tool
            plant_layer = self.tmx_data.get_layer_by_name("Plants")
            watered_layer = self.tmx_data.get_layer_by_name("Watered")
            if plant_layer:
                tile_gid = plant_layer.data[tile_y][tile_x]
                if tile_gid != 0:  # Check if there's a plant
                    tile_properties = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                    if tile_properties and tile_properties.get("harvest", False):
                        print(f"Harvested plant at ({tile_x}, {tile_y})")
                        plant_layer.data[tile_y][tile_x] = 0  # Remove the plant
                        self.update_map("Plants", plant_layer.data)
                        
                        # Remove watered soil if it was there
                        if watered_layer and watered_layer.data[tile_y][tile_x] != 0:
                            watered_layer.data[tile_y][tile_x] = 0
                            self.update_map("Watered", watered_layer.data)
                        
                        # Indicate the item was added to inventory
                        print("+++ Added to inventory +++")
                        source = tile_properties.get("source", "Unknown")
                        if (source != "Unknown"):
                            name = str.split(source, '/')[-1]
                            name = str.replace(name, ".png", "")
                            name = str.replace(name, "1", "")
                            name = str.replace(name, "2", "")
                            name = str.replace(name, "3", "")
                            name = str.replace(name, "4", "")
                            name = str.replace(name, "5", "")
                            name = str.replace(name, "6", "")
                            name = str.capitalize(name)
                            inventorydata.insertItemIntoSpareSlot((name, 1))

    def get_seed_gid(self, seed_name):
        # Map seed names to their initial GID in the tileset using get_gid
        seed_gid_map = {
            "wheat": self.get_gid("Plant_Objects", 1),
            "tomato": self.get_gid("Plant_Objects", 7)
            # Add other seeds here
        }
        return seed_gid_map.get(seed_name, 0)

    def grow_plants(self):
        """
        Updates plant growth stages based on the Plant_Objects tileset using object properties.
        Growth stops at the `last-1` stage for each plant. Growth speed is doubled if the tile is watered.
        Only updates the map if any changes occur for efficiency.
        """
        plant_layer = self.tmx_data.get_layer_by_name("Plants")
        watered_layer = self.tmx_data.get_layer_by_name("Watered")
        updated = False  # Track if any changes occur

        if plant_layer:
            for y in range(self.tmx_data.height):
                for x in range(self.tmx_data.width):
                    tile_gid = plant_layer.data[y][x]
                    if tile_gid != 0:  # Skip empty tiles
                        tile_properties = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                        if tile_properties:
                            # Check if the tile has a "growing" property
                            growing = tile_properties.get("growing", True)
                            next_stage_gid = tile_gid + 1

                            if growing and next_stage_gid:
                                # Check if the tile is watered
                                is_watered = watered_layer and watered_layer.data[y][x] != 0

                                # Advance growth stage
                                plant_layer.data[y][x] = next_stage_gid
                                updated = True

                                # If watered, advance an additional stage if possible
                                if is_watered:
                                    next_stage_gid += 1  # Advance an additional stage
                                    next_properties = self.tmx_data.get_tile_properties_by_gid(next_stage_gid)
                                    if next_properties and next_properties.get("growing", False):
                                        plant_layer.data[y][x] = next_stage_gid
                                        updated = True

            # Update the map only if changes occurred
            if updated:
                self.update_map("Plants", plant_layer.data)

    def update_map(self, layer_name, new_data):
        for layer in self.tmx_data.visible_layers:
            if layer.name == layer_name:
                layer.data = new_data
                break

    def drawPause(self) -> pygame.Rect:
        pauseButtonImage = pygame.image.load("assets/buttons/pause.png").convert_alpha()
        pauseButtonImage = pygame.transform.scale(pauseButtonImage, (65, 65))
        pauseButtonImage.set_colorkey((0, 0, 0))

        #pauseButtonImage = pygame.image.load("assets/buttons/pause.png").convert_alpha()
        #pauseButtonImage = pygame.transform.scale(pauseButtonImage, (64, 64))
        
        rect = pygame.Rect(16, 16, 65, 65)
        self.screen.blit(pauseButtonImage, rect)
        return rect
        
    def pauseTheGame(self):
        self.is_paused = True
        pauseMenu = start_menu.StartMenu(username=self.username, gameInstance=self)
        pauseMenu.current_screen = "options"
        pauseMenu.isFromGame = True
        pauseMenu.run()

    def loadGameState(self):
        print("loading game state")
        time = self.gameData[0]
        day = self.gameData[1]
        position = self.gameData[2]
        house = self.gameData[3]
        weather = self.gameData[4]
        character = self.gameData[5]
        direction = self.gameData[6]
        raining = self.gameData[7]
        cloudy = self.gameData[8]
        self.house = house
        self.player_x = position[0]
        self.player_y = position[1]
        self.set_game_time(time[0], time[1])
        self.current_weather = weather
        self.selected_character = character
        self.current_day = day
        self.player_direction = direction
        self.raining = raining
        self.cloudy_weather = cloudy
        self.pla
    
    def saveGameState(self):
        theGameTime = self.get_game_time()
        day = self.current_day
        position = (self.player_x, self.player_y)
        house = self.house
        weather = self.current_weather
        character = self.selected_character
        direction = self.player_direction
        raining = self.raining
        cloudy = self.cloudy_weather
        return (theGameTime, day, position, house, weather, character, direction, raining, cloudy)
    
    def draw_gold(self):
        # Draw gold in the top right corner with coin icon - Enhanced with shadow effect
        gold_bg = pygame.Rect(self.SCREEN_WIDTH - 280, 10, 100, 40)  # Moved further to the left
        
        # Draw shadow
        shadow_rect = gold_bg.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, (89, 40, 20), shadow_rect, border_radius=10)
        
        # Draw gold background
        pygame.draw.rect(self.screen, (201, 121, 77), gold_bg, border_radius=10)
        pygame.draw.rect(self.screen, (89, 40, 20), gold_bg, 2, border_radius=10)  # Border
        
        # Render gold text
        font = pygame.font.Font(None, 24)
        gold_surface = font.render(f"{self.gold}", True, (255, 215, 0))
        self.screen.blit(gold_surface, (gold_bg.x + 10, gold_bg.y + 10))  # Adjusted position to fit inside the box
        
        # Draw coin icon inside the box
        coin_icon = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(coin_icon, (255, 215, 0), (10, 10), 10)
        pygame.draw.circle(coin_icon, (89, 40, 20), (10, 10), 10, 1)  # Border
        self.screen.blit(coin_icon, (gold_bg.right - 30, gold_bg.y + 10))  # Positioned inside the box

    def run(self):
        # Main Game Loop
        running = True
        pygame.display.set_caption("8-Bit Barista")
        clock = pygame.time.Clock()
        FPS = 60

        last_grow_time = self.get_game_time()[0]  # Track the last hour plants were grown

        # Popup state and fade effect variables
        popup_shown = True  # Show popup initially

        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            self.handle_input()  # Handle key inputs

            # Check for new day prompt at 2:00 AM
            self.check_for_new_day_prompt()

            self.pause_game_time = False

            # If the user confirmed a new day, reset time and advance day
            if self.confirm_new_day:
                self.set_game_time(5, 30)  # Move time reset here
                self.current_day += 1
                self.current_weather = random.choice(["sunny", "cloudy", "rainy"])
                self.raining = self.current_weather == "rainy"
                self.cloudy_weather = self.current_weather == "cloudy"
                self.confirm_new_day = False  # Reset confirmation flag

                self.apply_weather_effects()
                print(f"New day started at 5:30 AM. Day {self.current_day} - Weather: {self.current_weather}")

            # Only update game logic if not paused
            if not self.is_paused:
                self.draw_map(self.camera_surface, self.camera_x, self.camera_y)

                # Handle Events
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]: self.pauseTheGame()
                moving = False

                # Movement Logic (Player Now Restricted to Map Bounds)
                move_x, move_y = 0, 0

                if keys[pygame.K_w]:  # Move Up
                    if self.player_y - self.PLAYER_SPEED >= 0:  # Prevent going above the map
                        move_y = -self.PLAYER_SPEED
                    self.player_direction = "up"
                    moving = True
                if keys[pygame.K_s]:  # Move Down
                    if self.player_y + self.PLAYER_SPEED + self.SPRITE_HEIGHT <= self.MAP_HEIGHT:  # Prevent going below the map
                        move_y = self.PLAYER_SPEED
                    self.player_direction = "down"
                    moving = True
                if keys[pygame.K_a]:  # Move Left
                    if self.player_x - self.PLAYER_SPEED >= 0:  # Prevent going left off the map
                        move_x = -self.PLAYER_SPEED
                    self.player_direction = "left"
                    moving = True
                if keys[pygame.K_d]:  # Move Right
                    if self.player_x + self.PLAYER_SPEED + self.SPRITE_WIDTH <= self.MAP_WIDTH:  # Prevent going right off the map
                        move_x = self.PLAYER_SPEED
                    self.player_direction = "right"
                    moving = True


                # Apply Movement (Player Now Restricted to Map Bounds)
                self.move_player(move_x, move_y)

                # Handle Idle Animations (When No Input is Given)
                if not moving:
                    if self.player_direction == "up":
                        self.player_direction = "idle_up"
                    elif self.player_direction == "down":
                        self.player_direction = "idle_down"
                    elif self.player_direction == "left":
                        self.player_direction = "idle_left"
                    elif self.player_direction == "right":
                        self.player_direction = "idle_right"

                # Update Animation (Only cycle between the two movement frames when moving)
                if moving:
                    self.animation_timer += 1
                    if self.animation_timer > 10:  # Adjust animation speed
                        self.animation_index = (self.animation_index + 1) % 2  # Always alternate between 0 and 1
                        self.animation_timer = 0
                else:
                    self.animation_index = 0  # Reset to first frame when idle

                # Camera Moves Freely Until It Hits the Map Edge
                new_camera_x = self.player_x - self.CAMERA_WIDTH // 2
                new_camera_y = self.player_y - self.CAMERA_HEIGHT // 2

                # Clamp Camera to Stay Within the Map Bounds
                self.camera_x = max(0, min(new_camera_x, self.MAP_WIDTH - self.CAMERA_WIDTH))
                self.camera_y = max(0, min(new_camera_y, self.MAP_HEIGHT - self.CAMERA_HEIGHT))

                # Draw Player at Correct Position Relative to Camera
                self.camera_surface.blit(self.ANIMATION_FRAMES[self.selected_character][self.player_direction][self.animation_index], 
                        (self.player_x - self.camera_x, self.player_y - self.camera_y))


                fade_alpha = None

                # **Popup and fade logic**
                if popup_shown:
                    # Load and display the WASD image
                    try:
                        wasd_image = pygame.image.load(
                            os.path.join(self.BASE_DIR, "assets", "images", "others", "fishing", "wasd_image.png")
                        ).convert_alpha()
                    except pygame.error as e:
                        print("Error loading image:", e)
                        wasd_image = pygame.Surface((200, 100))  # Temporary placeholder surface for debugging

                    # Resize the image to a reasonable size (e.g., 200x100)
                    wasd_image = pygame.transform.scale(wasd_image, (70, 40))  # Adjust size as needed

                    # Initialize the alpha value for fading (only once when the popup is shown)
                    if fade_alpha is None:  # Initialize fade_alpha only once when popup is shown
                        fade_alpha = 255  # Start with the image fully visible

                    # Calculate position of popup above the player's head
                    popup_x = self.player_x - (wasd_image.get_width() // 2) - self.camera_x + 9  # Centered relative to camera
                    popup_y = self.player_y - wasd_image.get_height() - 10 - self.camera_y  # 20 pixels above the player

                    # Ensure the image stays within the screen bounds
                    if popup_x < 0:
                        popup_x = 0
                    elif popup_x + wasd_image.get_width() > self.SCREEN_WIDTH:
                        popup_x = self.SCREEN_WIDTH - wasd_image.get_width()

                    if popup_y < 0:
                        popup_y = 0
                    elif popup_y + wasd_image.get_height() > self.SCREEN_HEIGHT:
                        popup_y = self.SCREEN_HEIGHT - wasd_image.get_height()

                    # Update the alpha value of the image to control its fading
                    wasd_image.set_alpha(fade_alpha)

                    # Blit the WASD image above the player's head, adjusted for camera movement
                    self.camera_surface.blit(wasd_image, (popup_x, popup_y))

                    # Check for WASD key press to start fading out
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
                    #     # Start the fade-out process once a WASD key is pressed
                    #     if fade_alpha > 0:
                    #         fade_alpha -= 5  # Adjust fade speed (decreases over time)

                    # # Optional: If you want to make sure the popup disappears completely when faded
                    # if fade_alpha <= 0:
                        popup_shown = False  # Hide the popup completely when it has faded out

                # Scale up the camera surface to the main screen
                zoomed_surface = pygame.transform.scale(self.camera_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                # Get nighttime alpha level
                night_alpha = self.draw_night_filter()  
                rain_alpha = 80 if self.raining else 0

                # Initialize overlay with full transparency by default
                overlay = pygame.Surface((zoomed_surface.get_size()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 0))  # Fully transparent by default

                # Apply overlay only when it's night or raining
                if self.is_night_time():
                    overlay.fill((0, 0, 0, night_alpha))  # Adjust opacity

                if self.raining:
                    rain_overlay = pygame.Surface((zoomed_surface.get_size()), pygame.SRCALPHA)
                    rain_overlay.fill((0,0,0, rain_alpha))
                    overlay.blit(rain_overlay, (0,0))
                
                if self.cloudy_weather:  # Draw the cloudy overlay if enabled
                    self.cloudy.draw(overlay)  # Draw the cloudy effect on the overlay

                # Now, overlay is always defined before blitting
                zoomed_surface.blit(overlay, (0, 0))  
                
                # Update & Draw Rain (Only if raining)
                if self.raining:
                    self.rain.update(self.camera_x, self.camera_y)
                    self.rain.draw(zoomed_surface)  # Draw all rain elements (drops + floor splashes)

                # Call grow_plants every in-game hour
                current_hour = self.get_game_time()[0]
                if current_hour != last_grow_time:
                    self.grow_plants()
                    last_grow_time = current_hour

            # Blit the final zoomed surface to the screen
            self.screen.blit(zoomed_surface, (0, 0))
            
            self.toolbox.draw(self.screen)
            self.backpack = inventory.drawBundle(self.screen)
                            
            # Draw HUD
            self.draw_hud()

            # Draw Gold
            self.draw_gold()

            #draw pause button
            self.pauseButton = self.drawPause()

            # Draw the new day prompt if active
            if self.show_new_day_prompt:
                self.draw_new_day_prompt()

            pygame.display.flip()  # Update display
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    image_path = "assets/map/house2.png"
    pet = "assets/images/pets/browncat.png"
    name = "jake"
    selected_character = "boy1"
    game = Game(image_path, pet, name, selected_character)
    game.run()