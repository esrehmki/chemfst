#!/usr/bin/env python3

import sys
import importlib

print("Python version:", sys.version)

try:
    # Try to import directly from the compiled module
    module = importlib.import_module("chemfst")
    print("Successfully imported chemfst module!")
    print("Available attributes:", dir(module))

    # Check if ChemicalFST class exists
    if hasattr(module, "ChemicalFST"):
        print("\nTesting ChemicalFST class:")
        try:
            # Create an instance of ChemicalFST
            fst = module.ChemicalFST("data/chemical_names.fst")
            print("✅ Successfully created ChemicalFST instance")

            # Try a prefix search
            results = fst.prefix_search("eth", 5)
            print(f"Prefix search for 'eth' returned {len(results)} results:")
            for item in results:
                print(f"  - {item}")

            # Try a substring search
            results = fst.substring_search("benz", 5)
            print(f"\nSubstring search for 'benz' returned {len(results)} results:")
            for item in results:
                print(f"  - {item}")
        except Exception as e:
            print(f"❌ Error using ChemicalFST: {e}")
    else:
        print("❌ ChemicalFST class not found in module")

    # Check if build_fst function exists
    if hasattr(module, "build_fst"):
        print("\nFound build_fst function")
    else:
        print("❌ build_fst function not found in module")

except ImportError as e:
    print(f"❌ Failed to import chemfst: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
