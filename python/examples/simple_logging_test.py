#!/usr/bin/env python3
"""
Simple test to verify ChemFST logging is working correctly.
"""

import logging
import sys
import os
import tempfile

# Add the parent directory to the path to import chemfst
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    # Configure logging at DEBUG level to see all messages
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger('chemfst')
    logger.setLevel(logging.DEBUG)

    print("Testing ChemFST logging...")
    print("Should see DEBUG, INFO, and ERROR messages below:")
    print("-" * 50)

    try:
        import chemfst

        # Test 1: Error case (file not found)
        print("\n1. Testing error logging - file not found:")
        try:
            chemfst.build_fst("nonexistent.txt", "output.fst")
        except FileNotFoundError:
            print("   Error caught as expected")

        # Test 2: Normal operations
        print("\n2. Testing normal operations with DEBUG logging:")

        # Create test data
        test_data = ["water", "ethanol"]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            input_file = f.name
            for chemical in test_data:
                f.write(f"{chemical}\n")

        fst_file = input_file.replace('.txt', '.fst')

        try:
            # Build FST
            print("   Building FST...")
            chemfst.build_fst(input_file, fst_file)

            # Load FST
            print("   Loading FST...")
            fst = chemfst.ChemicalFST(fst_file)

            # Search
            print("   Searching...")
            results = fst.prefix_search("eth", 5)
            print(f"   Found: {results}")

        finally:
            # Clean up
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(fst_file):
                os.remove(fst_file)

        print("\n[SUCCESS] Test completed successfully!")

    except ImportError:
        print("[ERROR] chemfst module not found. Run: cd chemfst-py && maturin develop")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

if __name__ == "__main__":
    main()
