#!/usr/bin/env python3
"""
Test import script for ChemFST Python bindings.
This script attempts to import the ChemFST module in different ways
to see which imports work.
"""

import sys
import os

def test_imports():
    """Test various import patterns to see what works"""
    print("Python version:", sys.version)
    print("Current directory:", os.getcwd())
    print("\nTrying various import patterns:")

    modules_to_try = [
        "chemfst",
        "chemfst_py",
        "chemfst.chemfst_py"
    ]

    for module in modules_to_try:
        try:
            print(f"\nAttempting to import '{module}'...")
            exec(f"import {module}")
            print(f"✅ SUCCESS: '{module}' imported successfully")
            # Try to see what's in the module
            try:
                print(f"   Contents of {module}:")
                exec(f"for item in dir({module}): print(f'   - {{item}}')")
            except Exception as e:
                print(f"   Could not list contents: {e}")
        except ImportError as e:
            print(f"❌ FAILED: Could not import '{module}': {e}")

    # Try to import specific items
    for module in ["chemfst", "chemfst_py"]:
        for item in ["ChemicalFST", "build_fst"]:
            try:
                print(f"\nAttempting to import {item} from {module}...")
                exec(f"from {module} import {item}")
                print(f"✅ SUCCESS: '{item}' imported from '{module}'")
            except ImportError as e:
                print(f"❌ FAILED: Could not import '{item}' from '{module}': {e}")

if __name__ == "__main__":
    test_imports()