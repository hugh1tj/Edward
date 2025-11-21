"""
Script to generate spritesheet JSON for regions tileset.
Reads the regions tileset image and creates a JSON mapping similar to spritesheet.json
"""
import json
import os
import sys

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL/Pillow not installed. Install with: pip install Pillow")

def generate_spritesheet_json(tileset_image_path, tile_width, tile_height, output_json_path, tile_name_prefix="region_"):
    """
    Generate spritesheet JSON for a tileset image.
    
    Args:
        tileset_image_path: Path to the tileset PNG image
        tile_width: Width of each tile (e.g., 16)
        tile_height: Height of each tile (e.g., 16)
        output_json_path: Where to save the JSON file
        tile_name_prefix: Prefix for tile names (e.g., "region_")
    """
    
    if not HAS_PIL:
        print("Error: PIL/Pillow is required. Install with: pip install Pillow")
        return False
    
    if not os.path.exists(tileset_image_path):
        print(f"Error: Tileset image not found at {tileset_image_path}")
        return False
    
    print(f"Reading tileset image: {tileset_image_path}")
    
    # Get image dimensions
    img = Image.open(tileset_image_path)
    img_width, img_height = img.size
    
    print(f"Image size: {img_width}x{img_height} pixels")
    print(f"Tile size: {tile_width}x{tile_height} pixels")
    
    # Calculate how many tiles fit
    tiles_per_row = img_width // tile_width
    tiles_per_col = img_height // tile_height
    
    print(f"Tiles per row: {tiles_per_row}, Tiles per column: {tiles_per_col}")
    print(f"Total tiles: {tiles_per_row * tiles_per_col}")
    
    frames = {}
    tile_index = 0
    
    # Generate frame data for each tile
    for row in range(tiles_per_col):
        for col in range(tiles_per_row):
            x = col * tile_width
            y = row * tile_height
            
            # Name tiles with index
            tile_name = f"{tile_name_prefix}{tile_index}.png"
            
            frames[tile_name] = {
                "frame": {"x": x, "y": y, "w": tile_width, "h": tile_height},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": tile_width, "h": tile_height},
                "sourceSize": {"w": tile_width, "h": tile_height}
            }
            
            tile_index += 1
    
    # Create output structure matching spritesheet.json format
    output = {
        "frames": frames,
        "meta": {
            "app": "https://www.codeandweb.com/texturepacker",
            "version": "1.0",
            "image": os.path.basename(tileset_image_path),
            "format": "RGBA8888",
            "size": {"w": img_width, "h": img_height},
            "scale": "1"
        }
    }
    
    # Write JSON file
    output_dir = os.path.dirname(output_json_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSuccessfully generated: {output_json_path}")
    print(f"Generated {tile_index} tile definitions")
    
    return True

if __name__ == "__main__":
    # Paths relative to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # You'll need to specify the path to your regions tileset image
    # This is a placeholder - adjust based on your actual tileset location
    tileset_image_path = os.path.join(project_root, "src", "assets", "images", "regions_tileset.png")
    output_json_path = os.path.join(project_root, "src", "assets", "data", "regions_spritesheet.json")
    
    # Default tile size (adjust if different)
    tile_width = 16
    tile_height = 16
    
    # Check if tileset image exists, if not, prompt user
    if not os.path.exists(tileset_image_path):
        print(f"Tileset image not found at: {tileset_image_path}")
        print("\nPlease specify the path to your regions tileset image:")
        print("1. Update tileset_image_path in this script, or")
        print("2. Pass it as a command line argument")
        print("\nExample usage:")
        print(f"  python {sys.argv[0]} path/to/regions_tileset.png")
        
        if len(sys.argv) > 1:
            tileset_image_path = sys.argv[1]
        else:
            sys.exit(1)
    
    success = generate_spritesheet_json(
        tileset_image_path, 
        tile_width, 
        tile_height, 
        output_json_path,
        tile_name_prefix="region_"
    )
    
    if not success:
        sys.exit(1)

