"""
Script to generate regions_mapping.json from Excel spreadsheet.
Reads SeaAreas.xlsx and creates a mapping of tile IDs to region names.
"""
import json
import os
import sys

# Try to import openpyxl (for .xlsx files)
try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("Warning: openpyxl not installed. Install with: pip install openpyxl")

# Try to import pandas as alternative
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

def read_excel_openpyxl(filepath):
    """Read Excel file using openpyxl."""
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active  # Get first worksheet
    
    mapping = {}
    
    # Assume first row is header, data starts from row 2
    # Adjust column indices based on your Excel structure
    # Expected format: Column A = Tile ID, Column B = Region Name
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is not None and row[1] is not None:
            tile_id = str(int(row[0])) if isinstance(row[0], (int, float)) else str(row[0])
            region_name = str(row[1]).strip()
            if tile_id and region_name:
                mapping[tile_id] = region_name
                print("40 in openpyxl",region_name,tile_id)
    
    return mapping

def read_excel_pandas(filepath):
    """Read Excel file using pandas."""
    df = pd.read_excel(filepath)
    
    # Assume first column is Tile ID, second is Region Name
    # Adjust column names if your Excel has headers
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
            print("67 in excel",region_name,tile_id)
    return mapping

def generate_regions_mapping(excel_path, output_path):
    """Generate regions_mapping.json from Excel file."""
    
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return False
    
    print(f"Reading Excel file: {excel_path}")
    
    # Try openpyxl first, then pandas
    mapping = None
    if HAS_OPENPYXL:
        try:
            mapping = read_excel_openpyxl(excel_path)
            print(f"Successfully read Excel using openpyxl. Found {len(mapping)} mappings.")
        except Exception as e:
            print(f"Error reading with openpyxl: {e}")
            mapping = None
    
    if mapping is None and HAS_PANDAS:
        try:
            mapping = read_excel_pandas(excel_path)
            print(f"Successfully read Excel using pandas. Found {len(mapping)} mappings.")
        except Exception as e:
            print(f"Error reading with pandas: {e}")
            mapping = None
    
    if mapping is None:
        print("Error: Could not read Excel file. Please install openpyxl: pip install openpyxl")
        return False
    
    # Write JSON file
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated: {output_path}")
    print(f"Total mappings: {len(mapping)}")
    print("\nSample mappings:")
    for i, (tile_id, region) in enumerate(list(mapping.items())[:5]):
        print(f"  {tile_id}: {region}")
    if len(mapping) > 5:
        print(f"  ... and {len(mapping) - 5} more")
    
    return True

if __name__ == "__main__":
    # Paths relative to project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(project_root, "src", "assets", "data", "SeaAreas.xlsx")
    output_path = os.path.join(project_root, "src", "assets", "data", "regions_mapping.json")
    
    success = generate_regions_mapping(excel_path, output_path)
    print("125 map",success)
    if not success:
        print("\nTroubleshooting:")
        print("1. Make sure SeaAreas.xlsx exists in src/assets/data/")
        print("2. Install openpyxl: pip install openpyxl")
        print("3. Or install pandas: pip install pandas openpyxl")
        print("4. Check that Excel file has Tile ID in first column and Region Name in second column")
        sys.exit(1)

