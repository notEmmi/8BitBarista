import pygame
import sqlite3

class GameState:
    def __init__(self, house="", pet="", name="", selected_character="", current_day=1, current_weather="", time_hour=6, time_minute=0, fromPriorMenu=False, GameData=None):
        self.house = house
        self.pet = pet
        self.name = name  # character's in-game name
        self.selected_character = selected_character
        self.current_day = current_day
        self.current_weather = current_weather
        self.time_hour = time_hour
        self.time_minute = time_minute
        self.fromPriorMenu = fromPriorMenu
        self.GameData = GameData

    def save_to_db(self, conn, username):
        cursor = conn.cursor()

        # Ensure 'saves' table exists and has the right structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                character TEXT,
                building TEXT,
                pet TEXT,
                day INTEGER DEFAULT 1,
                weather TEXT DEFAULT 'sunny',
                hour INTEGER DEFAULT 6,
                minute INTEGER DEFAULT 0,
                name TEXT,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        # Check if this user already has a save
        cursor.execute("SELECT id FROM saves WHERE username = ?", (username,))
        exists = cursor.fetchone()

        if exists:
            # Update existing save
            cursor.execute('''
                UPDATE saves
                SET character = ?, building = ?, pet = ?, day = ?, weather = ?, hour = ?, minute = ?, name = ?
                WHERE username = ?
            ''', (
                self.selected_character,
                self.house,
                self.pet,
                self.current_day,
                self.current_weather,
                self.time_hour,
                self.time_minute,
                self.name,
                username
            ))
        else:
            # Create a new save entry
            cursor.execute('''
                INSERT INTO saves (username, character, building, pet, day, weather, hour, minute, name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                username,
                self.selected_character,
                self.house,
                self.pet,
                self.current_day,
                self.current_weather,
                self.time_hour,
                self.time_minute,
                self.name
            ))

        conn.commit()

    @classmethod
    def load_from_db(cls, conn, username):
        cursor = conn.cursor()
        cursor.execute('''
            SELECT building, pet, name, character, day, weather, hour, minute 
            FROM saves WHERE username = ?
        ''', (username,))
        row = cursor.fetchone()

        if row:
            building, pet, name, character, day, weather, hour, minute = row
            return cls(
                house=building,
                pet=pet,
                name=name,
                selected_character=character,
                current_day=day,
                current_weather=weather,
                time_hour=hour,
                time_minute=minute,
                fromPriorMenu=True,
                GameData=None
            )
        else:
            print(f"[DEBUG] No save found for user: {username}")
            return None