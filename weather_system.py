import pygame
import random
from datetime import datetime

class WeatherSystem:
    def __init__(self):
        self.current_weather = "sunny"
        self.day_counter = 1
        self.last_update_day = 0

    def update_weather(self, game_hour, game_minute):
        # Convert game time to total minutes
        total_minutes = game_hour * 60 + game_minute
        
        # Calculate current day (days start at 6:00 AM)
        current_day = (total_minutes - 360) // (24 * 60) + 1
        
        if current_day > self.day_counter:
            self.day_counter = current_day
            if self.day_counter == 1:
                self.current_weather = "sunny"
            else:
                self.current_weather = random.choice(["sunny", "cloudy", "rainy"])
            return True
        return False