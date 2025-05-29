#!/usr/bin/env python3
"""
ChemFST Python Bindings Usage Examples

This script demonstrates how to use the ChemFST Python bindings for high-performance
chemical name searching using Finite State Transducers.
"""

import time
import sys
from pathlib import Path
from chemfst import ChemicalFST, build_fst


def main():
    """Run example ChemFST operations"""
    # Paths for our files
    input_path = Path("chemical_names.txt")
    fst_path = Path("chemical_names.fst")

    # Check if we need to build the FST index
    if not fst_path.exists():
        print(f"Building FST index from {input_path}...")
        if not input_path.exists():
            print(f"Error: Chemical names file not found at {input_path}")
            print("Please create a chemical_names.txt file with one chemical name per line")
            sys.exit(1)

        build_fst(input_path, fst_path)
        print(f"FST index built and saved to {fst_path}")

    print(f"Loading FST index from {fst_path}...")
    start = time.time()
    fst = ChemicalFST(fst_path)
    load_time = time.time() - start
    print(f"FST loaded in {load_time:.3f} seconds")

    # Example: Prefix search (autocomplete)
    prefixes = ["eth", "meth", "prop", "benz"]
    for prefix in prefixes:
        print(f"\nSearching for chemicals starting with '{prefix}':")
        start = time.time()
        results = fst.prefix_search(prefix, max_results=5)
        search_time = time.time() - start

        for chemical in results:
            print(f"  {chemical}")

        print(f"Found {len(results)} results in {search_time:.6f} seconds")

    # Example: Substring search
    substrings = ["acid", "ol", "ene", "chlor"]
    for substring in substrings:
        print(f"\nSearching for chemicals containing '{substring}':")
        start = time.time()
        results = fst.substring_search(substring, max_results=5)
        search_time = time.time() - start

        for chemical in results:
            print(f"  {chemical}")

        print(f"Found {len(results)} results in {search_time:.6f} seconds")

    # Performance benchmark
    print("\n=== Performance Benchmark ===")
    test_prefix = "a"
    iterations = 100
    start = time.time()

    for _ in range(iterations):
        fst.prefix_search(test_prefix, max_results=10)

    total_time = time.time() - start
    avg_time = total_time / iterations

    print(f"Performed {iterations} prefix searches")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Average time per search: {avg_time:.6f} seconds")


if __name__ == "__main__":
    main()
