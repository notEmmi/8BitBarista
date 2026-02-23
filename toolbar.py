import pygame
import os

class Toolbox:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TOOLS_PATH = os.path.join(self.BASE_DIR, "assets", "images", "tools")
        
        self.tools = {
            "hoe": pygame.image.load(os.path.join(self.TOOLS_PATH, "hoe.png")),
            "seedpouch": pygame.image.load(os.path.join(self.TOOLS_PATH, "seedpouch.png")),
            "watercan": pygame.image.load(os.path.join(self.TOOLS_PATH, "watercan.png")),
            "shears": pygame.image.load(os.path.join(self.TOOLS_PATH, "shears.png"))
        }
        self.selected_tool = 0  # Index of the selected tool
        
        # Colors for the brown theme
        self.background_color = (139, 69, 19)  # Medium brown for background
        self.slot_color = (101, 67, 33)  # Dark brown for slots
        self.highlight_color = (255, 248, 220)  # Cream-white for selection highlight
        
        # Layout configuration
        self.rows = 1  # Change to 1 row
        self.cols = 4  # Adjust the number of columns to fit the remaining tools
        self.slot_width = 50
        self.slot_height = 50  # Make the height equal to the width to form a square
        self.slot_margin = 10
        self.corner_radius = 10  # For rounded corners

        self.seed_inventory_open = False
        self.selected_seed = None  # Track the selected seed
        self.seed_slots = ["wheat", "tomato"]  # Example seed list
        self.seed_icons = {
            "wheat": pygame.image.load(os.path.join(self.BASE_DIR, "assets", "images", "plants", "wheat1.png")),
            "tomato": pygame.image.load(os.path.join(self.BASE_DIR, "assets", "images", "plants", "tomato1.png"))
        }

    def select_tool(self, index):
        if self.seed_inventory_open and list(self.tools.keys())[self.selected_tool] == "seedpouch":
            # If seed pouch is open, only allow deselecting it
            if index == self.selected_tool:
                self.selected_tool = -1  # Deselect the seed pouch
                self.close_seed_inventory()
            return

        if 0 <= index < len(self.tools):
            if self.selected_tool == index:
                self.selected_tool = -1  # Deselect the tool if it's already selected
                if list(self.tools.keys())[index] == "seedpouch":
                    self.close_seed_inventory()  # Close inventory if seed pouch is deselected
            else:
                self.selected_tool = index  # Change to the new selected tool
                if list(self.tools.keys())[index] == "seedpouch":
                    self.open_seed_inventory()  # Open inventory if seed pouch is selected

    def open_seed_inventory(self):
        # Placeholder for opening the seed inventory
        print("Seed inventory opened")
        self.seed_inventory_open = True

    def close_seed_inventory(self):
        # Close the seed inventory
        print("Seed inventory closed")
        self.seed_inventory_open = False

    def draw(self, surface):
        screen_width, screen_height = surface.get_size()
        
        # Calculate toolbox dimensions
        box_width = (self.slot_width + self.slot_margin) * self.cols + self.slot_margin
        box_height = (self.slot_height + self.slot_margin) * self.rows + self.slot_margin
        
        # Center the toolbox at the bottom of the screen
        box_x = (screen_width - box_width) // 2
        box_y = screen_height - box_height - 20  # 20px padding from bottom
        
        # Draw the background
        pygame.draw.rect(surface, self.background_color, 
                        (box_x, box_y, box_width, box_height), 
                        border_radius=self.corner_radius)
        
        # Draw the seed inventory if open
        if self.seed_inventory_open:
            inventory_height = box_height  # Same height as the toolbar
            inventory_y = box_y - inventory_height - 10  # 10px padding above the toolbar
            
            # Calculate inventory width dynamically based on seed slots
            inventory_width = (self.slot_width + self.slot_margin) * len(self.seed_slots) + self.slot_margin
            pygame.draw.rect(surface, self.background_color, 
                            (box_x, inventory_y, inventory_width, inventory_height), 
                            border_radius=self.corner_radius)
            
            # Draw seed slots
            for i, seed in enumerate(self.seed_slots):
                slot_x = box_x + self.slot_margin + i * (self.slot_width + self.slot_margin)
                slot_y = inventory_y + self.slot_margin
                
                # Draw slot background
                pygame.draw.rect(surface, self.slot_color, 
                                (slot_x, slot_y, self.slot_width, self.slot_height),
                                border_radius=self.corner_radius)
                
                font = pygame.font.Font(None, 14)

                text_surface = font.render(str(i+1), True, (255, 255, 255))
                font_x = slot_x + self.slot_width - text_surface.get_width() - 5
                font_y = slot_y + 5
                
                surface.blit(text_surface, (font_x, font_y))
                
                # Highlight selected seed
                if self.selected_seed == i:
                    pygame.draw.rect(surface, self.highlight_color, 
                                    (slot_x - 2, slot_y - 2, self.slot_width + 4, self.slot_height + 4), 
                                    width=3, border_radius=self.corner_radius)
                
                # Draw the seed icon
                scaled_seed_icon = pygame.transform.scale(self.seed_icons[seed], (self.slot_width - 20, self.slot_height - 20))
                surface.blit(scaled_seed_icon, (slot_x + 10, slot_y + 10))
        
        # Draw the tool slots
        tool_list = list(self.tools.items())
        for i in range(min(self.rows * self.cols, len(tool_list))):
            row = i // self.cols
            col = i % self.cols
            
            # Calculate slot position
            slot_x = box_x + self.slot_margin + col * (self.slot_width + self.slot_margin)
            slot_y = box_y + self.slot_margin + row * (self.slot_height + self.slot_margin)
            
            # Draw slot background
            pygame.draw.rect(surface, self.slot_color, 
                            (slot_x, slot_y, self.slot_width, self.slot_height),
                            border_radius=self.corner_radius)

            #Render Slot Number
            font = pygame.font.Font(None, 14)

            text_surface = font.render(str(i+1), True, (255, 255, 255))
            font_x = slot_x + self.slot_width - text_surface.get_width() - 5
            font_y = slot_y + 5
            
            surface.blit(text_surface, (font_x, font_y))

            # Highlight selected tool only if a tool is selected
            if self.selected_tool != -1 and i == self.selected_tool:
                pygame.draw.rect(surface, self.highlight_color, 
                                (slot_x - 2, slot_y - 2, self.slot_width + 4, self.slot_height + 4), 
                                width=3, border_radius=self.corner_radius)
            
            # Draw the tool icon
            if i < len(tool_list):
                tool_name, tool_image = tool_list[i]
                # Scale the image to fit in the slot with some padding
                scaled_image = pygame.transform.scale(tool_image, (self.slot_width - 20, self.slot_height - 20))
                surface.blit(scaled_image, (slot_x + 10, slot_y + 10))

    def select_seed(self, index):
        if 0 <= index < len(self.seed_slots):
            self.selected_seed = index if self.selected_seed != index else None
