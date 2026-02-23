from PIL import Image
import os

def slice_character_sheet(path, output_dir):
    sheet = Image.open(path)

    directions = ["down", "right", "left", "up"]
    movements = ["_1", "_idle", "_2"]

    sprite_width, sprite_height = 50, 50

    os.makedirs(output_dir, exist_ok=True)

    for row in range(4):
        for col in range(3):
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height
            sprite = sheet.crop((left, upper, right, lower))
            
            # Construct filename
            filename = f"{directions[row]}{movements[col]}.png"
            output_path = os.path.join(output_dir, filename)

            # Crop and save
            crop_character(sprite, output_path)


def slice_sprite_sheet(path, output_dir, rows, cols):
    sheet = Image.open(path)

    sprite_width = sheet.width // cols
    sprite_height = sheet.height // rows

    os.makedirs(output_dir, exist_ok=True)

    for row in range(rows):
        for col in range(cols):
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height
            sprite = sheet.crop((left, upper, right, lower))
            
            # Construct filename
            filename = f"sprite_{row}_{col}.png"
            output_path = os.path.join(output_dir, filename)

            # Crop and save
            crop_character(sprite, output_path)


def crop_character(sprite, output_path):
    # Convert to RGBA to detect transparency
    sprite = sprite.convert("RGBA")

    # Get the bounding box of non-transparent pixels
    bbox = sprite.getbbox()

    if bbox:
        # Crop to bounding box and save
        cropped_sprite = sprite.crop(bbox)
        cropped_sprite.save(output_path)
        print(f"Cropped sprite saved: {output_path}")
    else:
        print(f"Warning: No character detected in {output_path}")

# Example usage
sprite_sheet_path = "Basic_tools_and_meterials.png"
output_folder = "assets/images/tools"
slice_sprite_sheet(sprite_sheet_path, output_folder, 2, 3)
