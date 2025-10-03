# Project Structure Documentation

## Overview
This document describes the clean, organized structure of the Edward Lloyd's Coffeehouse project.

## Directory Structure

```
edward_lloyds_coffeehouse/
├── src/                          # Main source code
│   ├── core/                     # Core game logic
│   │   ├── __init__.py
│   │   └── main.py              # Main game entry point
│   │
│   ├── models/                   # Data models and classes
│   │   ├── __init__.py
│   │   └── subroutines.py       # Ship, Insurer, Weather classes
│   │
│   ├── ui/                       # User interface components
│   │   ├── menus/               # Menu screens
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   ├── screens/             # Game screens
│   │   │   ├── __init__.py
│   │   │   ├── premiums.py
│   │   │   ├── ships.py
│   │   │   ├── ports.py
│   │   │   ├── routes.py
│   │   │   ├── weather_hazards.py
│   │   │   ├── underwriter_preferences.py
│   │   │   ├── goinside.py
│   │   │   ├── ships_set_sail.py
│   │   │   ├── premiums_alt.py
│   │   │   └── premiums_return.py
│   │   └── components/          # Reusable UI components
│   │       └── __init__.py
│   │
│   ├── data/                     # Game data and configuration
│   │   ├── __init__.py
│   │   ├── local_data.py        # Ship data, port data, etc.
│   │   └── text_content.py      # Game text content
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── pathfinding.py       # A* algorithm (was astar.py)
│   │   ├── spritesheet.py       # Sprite handling
│   │   ├── tiles.py             # Tile management
│   │   └── hello.py             # Utility functions
│   │
│   └── assets/                   # Game assets
│       ├── images/              # All image files
│       ├── data/                # JSON/CSV data files
│       └── fonts/               # Custom fonts (if any)
│
├── build/                        # Build artifacts (PyInstaller)
├── dist/                         # Distribution files
├── docs/                         # Documentation
│   ├── project_structure.md     # This file
│   └── not required for compilation/  # Old documentation files
│
├── tests/                        # Unit tests
│   ├── test_models/
│   ├── test_utils/
│   └── test_ui/
│
├── scripts/                      # Build and utility scripts
│   ├── main.spec                # PyInstaller spec file
│   └── pyvenv.cfg               # Virtual environment config
│
├── main.py                       # Simple launcher
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
└── .gitignore                    # Git ignore rules
```

## Key Changes Made

### 1. **Modular Organization**
- Separated core logic, UI, data, and utilities into distinct modules
- Created proper Python packages with `__init__.py` files
- Organized UI components by type (menus, screens, components)

### 2. **Import Structure**
- Updated all import statements to use relative imports
- Fixed circular dependencies
- Made the project structure more maintainable

### 3. **Asset Organization**
- Moved all images to `src/assets/images/`
- Moved data files to `src/assets/data/`
- Updated image paths in code

### 4. **Documentation**
- Created comprehensive README.md
- Added project structure documentation
- Organized old documentation files

### 5. **Build System**
- Moved build artifacts to appropriate locations
- Created proper requirements.txt
- Added .gitignore for clean version control

## Benefits

1. **Maintainability**: Clear separation of concerns makes code easier to maintain
2. **Scalability**: Easy to add new features without cluttering
3. **Professional**: Follows Python best practices and industry standards
4. **Testable**: Clear structure for unit testing
5. **Collaborative**: Easy for multiple developers to work on different parts

## Running the Game

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Development

The project now follows modern Python packaging practices with a clean, modular structure that makes it easy to extend and maintain.
