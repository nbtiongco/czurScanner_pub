#!/usr/bin/env python3
"""
Entry point for PyInstaller build.
Place this file in the root directory of your project.
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Now import and run
from document_scanner.main import main

if __name__ == "__main__":
    main()