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
    input_path = Path("data/chemical_names.txt")
    fst_path = Path("data/chemical_names.fst")

    # Example 1: Building an FST index
    print("\n1. Building an FST index")
    print("------------------------")
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Please create a data/chemical_names.txt file with one chemical name per line.")
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

    # Example 3: Preloading the FST for better performance
    print("\n3. Preloading FST into memory")
    print("----------------------------")
    print("Preloading forces all pages of the FST into memory, improving search performance.")
    start = time.time()
    count = fst.preload()
    preload_time = time.time() - start
    print(f"✅ Preloaded {count} keys in {preload_time:.6f} seconds")

    # Example 4: Prefix Search (Autocomplete)
    print("\n4. Prefix search (autocomplete)")
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

    # Example 5: Substring Search
    print("\n5. Substring search")
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

    # Example 6: Performance Testing
    print("\n6. Performance Testing")
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

    # Example 7: Compare Performance With and Without Preloading
    print("\n7. Effect of Preloading on Search Latency")
    print("----------------------------------------")
    print("To demonstrate the effect of preloading, we'll measure the first search")
    print("time for each letter of the alphabet. This simulates a 'cold start'")
    print("scenario where different parts of the FST need to be loaded from disk.")
    print("\nNote: In a real application, this effect would be more noticeable with a much larger FST.")

    # Create a new FST instance without preloading
    fresh_fst = chemfst.ChemicalFST(str(fst_path))

    # Test first search time for each letter
    first_search_times = []
    letters = list("abcdefghijklmnopqrstuvwxyz")

    print("\nTesting first-time searches for each letter without preloading:")
    for letter in letters:
        start = time.time()
        results = fresh_fst.prefix_search(letter, 10)
        search_time = time.time() - start
        first_search_times.append(search_time)
        print(f"  Letter '{letter}': {search_time*1000:.3f}ms ({len(results)} results)")

    avg_without_preload = sum(first_search_times) / len(first_search_times) * 1000
    max_without_preload = max(first_search_times) * 1000

    # Now preload and test again
    print("\nPreloading FST...")
    count = fresh_fst.preload()
    print(f"Preloaded {count} keys")

    preloaded_search_times = []
    print("\nTesting searches for each letter after preloading:")
    for letter in letters:
        start = time.time()
        results = fresh_fst.prefix_search(letter, 10)
        search_time = time.time() - start
        preloaded_search_times.append(search_time)
        print(f"  Letter '{letter}': {search_time*1000:.3f}ms ({len(results)} results)")

    avg_with_preload = sum(preloaded_search_times) / len(preloaded_search_times) * 1000
    max_with_preload = max(preloaded_search_times) * 1000

    improvement = (avg_without_preload - avg_with_preload) / avg_without_preload * 100
    max_improvement = (max_without_preload - max_with_preload) / max_without_preload * 100

    print("\nPreloading Performance Impact:")
    print(f"  Without preloading: avg={avg_without_preload:.3f}ms, max={max_without_preload:.3f}ms")
    print(f"  With preloading:    avg={avg_with_preload:.3f}ms, max={max_with_preload:.3f}ms")
    print(f"  Improvement:        {improvement:.1f}% faster on average, {max_improvement:.1f}% faster for worst case")

    print("\n✅ ChemFST demonstration completed successfully!")


if __name__ == "__main__":
    main()
