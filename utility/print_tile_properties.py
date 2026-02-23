import pytmx
"""
This script extracts and prints tile properties and layer data from a TMX map file.
Functions:
    print_tile_properties(map_file, output_file):
        Extracts tile properties and layer data from the specified TMX map file and writes them to an output file.
        - Initializes a minimal pygame display to avoid errors when loading the TMX file.
        - Iterates through all tile GIDs to retrieve their properties.
        - Iterates through visible layers to retrieve tile positions and their corresponding GIDs.
        - Outputs the data to a text file for easier inspection of tile GIDs and other map properties that are hard to find.
Usage:
    Run the script directly to process a TMX map file located in the "assets/map" directory and output the results to "tile_properties_output.txt".
"""
import os
import pygame  # Import pygame to initialize display


def print_tile_properties(map_file, output_file):
    # Initialize pygame display to avoid errors
    pygame.init()
    pygame.display.set_mode((1, 1))  # Create a minimal display

    tmx_data = pytmx.load_pygame(map_file)

    with open(output_file, "w") as file:
        file.write("Tile Properties:\n")
        for gid in range(tmx_data.maxgid):
            properties = tmx_data.get_tile_properties_by_gid(gid)
            if properties:
                file.write(f"  GID: {gid}, Properties: {properties}\n")

        file.write("\nLayer Data:\n")
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                file.write(f"Layer: {layer.name}\n")
                for x, y, gid in layer:
                    if gid != 0:  # Skip empty tiles
                        file.write(f"  Tile at ({x}, {y}) - GID: {gid}\n")

    # Quit pygame after processing
    pygame.quit()


if __name__ == "__main__":
    # Adjusted paths since the script and output file are now in the "utility" directory
    map_file = os.path.join(os.path.dirname(__file__), "..", "assets", "map", "map.tmx")
    output_file = os.path.join(os.path.dirname(__file__), "tile_properties_output.txt")
    print_tile_properties(map_file, output_file)
    print(f"Tile properties written to {output_file}")
