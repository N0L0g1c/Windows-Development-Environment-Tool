#!/usr/bin/env python3
"""
Windows Dev Setup GUI Launcher
Simple launcher for the dev setup GUI
"""

import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from dev_setup_gui import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Error importing GUI: {e}")
    print("Make sure all required packages are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting GUI: {e}")
    sys.exit(1)
