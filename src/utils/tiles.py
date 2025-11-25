
from ..data import local_data
import pygame, csv, os
import json

# Try to import Excel reading libraries (optional dependencies)
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        #print (x,y)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0 ,0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def change_me(self ,x ,y):  # a tjh test
        print ('my data' ,local_data.mapx)
        print('mycell' ,local_data.mapx[y][x])

        local_data.mapx[y][x] = 1


    def read_csv(self, filename):
        map = []

        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        # local_data.mapx=map
        # print(local_data.mapx) # which is in form list of lists
        #print ('map in read-csv' ,map)
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        local_data.mapx = map # hughes addition

        x, y = 0, 0
        # for row in map:
        for row in local_data.mapx: # hughes mod
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('beach.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('rocks.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('calm.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('land.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('northsouth.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '6':
                    tiles.append(Tile('gulf.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '7':
                    tiles.append(Tile('eastwest.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '8':
                    tiles.append(Tile('westeast.png', x * self.tile_size, y * self.tile_size, self.spritesheet))



                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        #print('self tile size' ,self.tile_size)
        #print('map in load_tiles', map)
        # print(tiles)
        return tiles

    def load_tiles_mod(self):
        tiles = []
        # map = self.read_csv(filename)
        # local_data.mapx = map  # hughes addition

        x, y = 0, 0
        # for row in local data:
        for row in local_data.mapx:  # hughes mod
            x = 0
            for tile in row:
                if tile == '0':
                    pass
                    # self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append('beach.png')
                elif tile == '2':
                    tiles.append('beach.png')
                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        # self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

        return tiles

    def write_csv(self):
        with open('output.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data
            writer.writerows(local_data.mapx)

        return

###########from spritesheet

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        #sprite.set_colorkey((0,0,0))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image


def auto_generate_regions_mapping(excel_path, output_path):
    """
    Auto-generate regions_mapping.json from Excel file if it doesn't exist.
    This function is called automatically by TileMap2 if the mapping file is missing.
    
    Args:
        excel_path: Path to SeaAreas.xlsx
        output_path: Path where regions_mapping.json should be created
        
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(excel_path):
        return False
    
    def read_excel_openpyxl(filepath):
        """Read Excel file using openpyxl."""
        wb = openpyxl.load_workbook(filepath, data_only=True)
        ws = wb.active  # Get first worksheet
        
        mapping = {}
        # Assume first row is header, data starts from row 2
        # Expected format: Column A = Tile ID, Column B = Region Name
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is not None and row[1] is not None:
                tile_id = str(int(row[0])) if isinstance(row[0], (int, float)) else str(row[0])
                region_name = str(row[1]).strip()
                if tile_id and region_name:
                    mapping[tile_id] = region_name
        return mapping
    
    def read_excel_pandas(filepath):
        """Read Excel file using pandas."""
        df = pd.read_excel(filepath)
        mapping = {}
        
        # If columns are unnamed, use indices
        if df.columns[0] == 0 or 'Tile ID' in str(df.columns[0]):
            id_col = df.columns[0]
            name_col = df.columns[1]
        else:
            # Try to find columns by name
            id_col = 'Tile ID' if 'Tile ID' in df.columns else df.columns[0]
            name_col = 'Region Name' if 'Region Name' in df.columns else df.columns[1]
        
        for _, row in df.iterrows():
            tile_id = str(int(row[id_col])) if pd.notna(row[id_col]) else None
            region_name = str(row[name_col]).strip() if pd.notna(row[name_col]) else None
            if tile_id and region_name:
                mapping[tile_id] = region_name
        return mapping
    
    # Try openpyxl first, then pandas
    mapping = None
    if HAS_OPENPYXL:
        try:
            mapping = read_excel_openpyxl(excel_path)
            if mapping:
                print(f"  Successfully read {len(mapping)} mappings using openpyxl")
        except Exception as e:
            print(f"  Error reading Excel with openpyxl: {e}")
            mapping = None
    
    if mapping is None and HAS_PANDAS:
        try:
            mapping = read_excel_pandas(excel_path)
            if mapping:
                print(f"  Successfully read {len(mapping)} mappings using pandas")
        except Exception as e:
            print(f"  Error reading Excel with pandas: {e}")
            mapping = None
    
    if mapping is None or len(mapping) == 0:
        if not HAS_OPENPYXL and not HAS_PANDAS:
            print(f"  ERROR: Neither openpyxl nor pandas is installed!")
            print(f"  Please install one: python -m pip install openpyxl")
        else:
            print(f"  ERROR: Could not read any mappings from Excel file")
            print(f"  Check that SeaAreas.xlsx has data in columns A (Tile ID) and B (Region Name)")
        return False
    
    # Write JSON file
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


class TileMap2():
    """
    Second tilemap for regions lookup.
    Loads regions CSV and mapping JSON to provide region name lookups.
    """
    def __init__(self, csv_filename, mapping_json_filename, spritesheet=None):
        """
        Initialize regions tilemap.
        
        Args:
            csv_filename: Path to regions CSV file (e.g., newmapNov2025seareas_Water.csv)
            mapping_json_filename: Path to regions_mapping.json
            spritesheet: Optional spritesheet for rendering (not required for lookup only)
        """
        self.tile_size = 16
        self.spritesheet = spritesheet
        self.map_data = self.read_csv(csv_filename)
        self.regions_mapping = self.load_mapping(mapping_json_filename)
        
        # Calculate map dimensions
        if self.map_data:
            self.map_h = len(self.map_data)
            self.map_w = len(self.map_data[0]) if self.map_data[0] else 0
        else:
            self.map_w, self.map_h = 0, 0
    
    def read_csv(self, filename):
        """Read CSV file and return as list of lists."""
        map_data = []
        try:
            with open(os.path.join(filename)) as data:
                reader = csv.reader(data, delimiter=',')
                for row in reader:
                    map_data.append(list(row))
            if map_data:
                print(f"Loaded regions CSV: {len(map_data)} rows, {len(map_data[0]) if map_data[0] else 0} columns")
            else:
                print(f"Warning: CSV file {filename} is empty")
        except FileNotFoundError:
            print(f"ERROR: CSV file not found: {filename}")
        except Exception as e:
            print(f"ERROR reading CSV file {filename}: {e}")
        return map_data
    
    def load_mapping(self, mapping_json_filename):
        """Load regions mapping from JSON file. Auto-generates if missing or empty."""
        mapping = {}
        # Use the filename as-is (it's already a path)
        mapping_path = mapping_json_filename
        
        # Check if mapping file exists and is valid
        file_exists = os.path.exists(mapping_path)
        mapping_is_empty = False
        
        # If mapping file exists, try to load it first
        if file_exists:
            try:
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    mapping = json.load(f)
                    # Check if the loaded mapping is empty
                    if not mapping or len(mapping) == 0:
                        mapping_is_empty = True
                        print(f"Warning: {mapping_json_filename} exists but is empty.")
            except json.JSONDecodeError as e:
                print(f"Error: {mapping_json_filename} contains invalid JSON: {e}")
                mapping_is_empty = True
            except Exception as e:
                print(f"Error reading mapping JSON {mapping_json_filename}: {e}")
                mapping_is_empty = True
        
        # If file doesn't exist OR is empty, try to auto-generate it
        if not file_exists or mapping_is_empty:
            # Try to find the Excel file in the same directory
            mapping_dir = os.path.dirname(mapping_path)
            excel_path = os.path.join(mapping_dir, "SeaAreas.xlsx")
            
            if os.path.exists(excel_path):
                if not file_exists:
                    print(f"regions_mapping.json not found. Auto-generating from {excel_path}...")
                else:
                    print(f"regions_mapping.json is empty. Auto-generating from {excel_path}...")
                
                if auto_generate_regions_mapping(excel_path, mapping_path):
                    print(f"Successfully auto-generated {mapping_path}")
                    # Reload the newly generated mapping
                    try:
                        with open(mapping_path, 'r', encoding='utf-8') as f:
                            mapping = json.load(f)
                            print(f"Loaded {len(mapping)} region mappings from {mapping_path}")
                    except Exception as e:
                        print(f"Error reloading auto-generated mapping: {e}")
                else:
                    print(f"Warning: Could not auto-generate mapping file. Region tracking disabled.")
                    if not HAS_OPENPYXL and not HAS_PANDAS:
                        print(f"  Required packages not installed. Please install: openpyxl or pandas")
                    return mapping
            else:
                if not file_exists:
                    print(f"Warning: Mapping JSON file not found: {mapping_json_filename}")
                else:
                    print(f"Warning: Mapping JSON file is empty: {mapping_json_filename}")
                print(f"  Excel file also not found at: {excel_path}")
                print(f"  Region tracking will be disabled.")
                return mapping
        
        # If we successfully loaded a non-empty mapping, report it
        if mapping and len(mapping) > 0:
            print(f"Loaded {len(mapping)} region mappings from {mapping_path}")
        
        return mapping
    
    def get_region_name(self, x, y):
        """
        Get region name at pixel coordinates (x, y).
        
        Args:
            x: X coordinate in pixels
            y: Y coordinate in pixels
            
        Returns:
            Region name string, or None if not found or no region at that location
        """
        if not self.map_data or not self.regions_mapping:
            return None
        
        # Convert pixel coordinates to tile coordinates
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        
        # Check bounds
        if tile_y < 0 or tile_y >= len(self.map_data):
            return None
        if tile_x < 0 or tile_x >= len(self.map_data[tile_y]):
            return None
        
        # Get tile ID from CSV
        tile_id_str = str(self.map_data[tile_y][tile_x]).strip()
        
        # Handle -1 (empty/no region) and 0
        if tile_id_str == '-1' or tile_id_str == '0' or not tile_id_str:
            return None
        
        # Look up region name in mapping
        region_name = self.regions_mapping.get(tile_id_str)
        
        return region_name
    
    def get_region_name_from_tile(self, tile_x, tile_y):
        """
        Get region name at tile coordinates (tile_x, tile_y).
        
        Args:
            tile_x: X coordinate in tiles (not pixels)
            tile_y: Y coordinate in tiles (not pixels)
            
        Returns:
            Region name string, or None if not found
        """
        if not self.map_data or not self.regions_mapping:
            return None
        
        # Check bounds
        if tile_y < 0 or tile_y >= len(self.map_data):
            return None
        if tile_x < 0 or tile_x >= len(self.map_data[tile_y]):
            return None
        
        # Get tile ID from CSV
        tile_id_str = str(self.map_data[tile_y][tile_x]).strip()
        
        # Handle -1 (empty/no region) and 0
        if tile_id_str == '-1' or tile_id_str == '0' or not tile_id_str:
            return None
        
        # Look up region name in mapping
        region_name = self.regions_mapping.get(tile_id_str)
        
        return region_name




