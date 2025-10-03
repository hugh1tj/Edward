#!/usr/bin/env python3
"""
Edward Lloyd's Coffeehouse - Ship Insurance Simulation Game
Main entry point for the game.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.main import main_menu

if __name__ == "__main__":
    main_menu()
