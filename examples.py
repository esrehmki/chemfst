#!/usr/bin/env python3
"""
ChemFST Examples: Demonstration of Python bindings for chemical name searching

This script demonstrates how to use the ChemFST Python bindings for high-performance
chemical name searching using Finite State Transducers (FSTs).
"""

import os
import time
import sys
from pathlib import Path


def main():
    """Run comprehensive examples demonstrating ChemFST capabilities"""
    print("ChemFST Python Bindings Demonstration")
    print("====================================\n")

    try:
        import chemfst
        print(f"Successfully imported chemfst module (version: {getattr(chemfst, '__version__', 'unknown')})")
    except ImportError as e:
        print(f"Error importing chemfst module: {e}")
        print("Make sure you've built and installed the Python bindings.")
        sys.exit(1)

    # Paths for our example files
    input_path = Path("chemical_names.txt")
    fst_path = Path("chemical_names.fst")

    # Example 1: Building an FST index
    print("\n1. Building an FST index")
    print("------------------------")
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Please create a chemical_names.txt file with one chemical name per line.")
        sys.exit(1)
    
    if fst_path.exists():
        print(f"FST index already exists at {fst_path}")
        print("Using existing FST index. (Set rebuild=True to rebuild)")
    else:
        print(f"Building FST index from {input_path}...")
        start = time.time()
        chemfst.build_fst(str(input_path), str(fst_path))
        build_time = time.time() - start
        print(f"✅ Built FST index in {build_time:.3f} seconds")

    # Example 2: Loading an FST
    print("\n2. Loading an FST index")
    print("----------------------")
    start = time.time()
    fst = chemfst.ChemicalFST(str(fst_path))
    load_time = time.time() - start
    print(f"✅ Loaded FST index in {load_time:.3f} seconds")

    # Example 3: Prefix Search (Autocomplete)
    print("\n3. Prefix search (autocomplete)")
    print("------------------------------")
    prefixes = ["eth", "meth", "prop", "benz", "chlor", "a"]
    
    for prefix in prefixes:
        print(f"\nSearching for chemicals starting with '{prefix}':")
        start = time.time()
        results = fst.prefix_search(prefix, 10)
        search_time = time.time() - start
        
        if results:
            for i, chemical in enumerate(results, 1):
                print(f"  {i}. {chemical}")
            total = len(results)
            print(f"✅ Found {total} result{'s' if total != 1 else ''} in {search_time:.6f} seconds")
        else:
            print("  No matching chemicals found")

    # Example 4: Substring Search
    print("\n4. Substring search")
    print("-----------------")
    substrings = ["acid", "ol", "ene", "hydr", "carb"]
    
    for substring in substrings:
        print(f"\nSearching for chemicals containing '{substring}':")
        start = time.time()
        results = fst.substring_search(substring, 10)
        search_time = time.time() - start
        
        if results:
            for i, chemical in enumerate(results, 1):
                print(f"  {i}. {chemical}")
            total = len(results)
            print(f"✅ Found {total} result{'s' if total != 1 else ''} in {search_time:.6f} seconds")
        else:
            print("  No matching chemicals found")

    # Example 5: Performance Testing
    print("\n5. Performance Testing")
    print("--------------------")
    iterations = 100
    test_prefix = "a"
    test_substring = "ol"
    
    print(f"Running {iterations} prefix searches for '{test_prefix}'...")
    start = time.time()
    for _ in range(iterations):
        fst.prefix_search(test_prefix, 10)
    prefix_time = time.time() - start
    
    print(f"Running {iterations} substring searches for '{test_substring}'...")
    start = time.time()
    for _ in range(iterations):
        fst.substring_search(test_substring, 10)
    substring_time = time.time() - start
    
    print("\nPerformance results:")
    print(f"  Prefix search:    {prefix_time:.3f}s total, {prefix_time/iterations*1000:.3f}ms per operation")
    print(f"  Substring search: {substring_time:.3f}s total, {substring_time/iterations*1000:.3f}ms per operation")

    print("\n✅ ChemFST demonstration completed successfully!")


if __name__ == "__main__":
    main()