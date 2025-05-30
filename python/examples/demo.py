#!/usr/bin/env python3
"""
ChemFST Examples: Comprehensive demonstration of Python bindings

This script demonstrates how to use the ChemFST Python bindings for high-performance
chemical name searching using Finite State Transducers (FSTs). It includes basic usage,
performance testing, and preloading demonstrations.
"""

import time
import sys
import os
from pathlib import Path
# from examples.utils.cross_platform_symbols import safe_checkmark, safe_crossmark


def check_imports():
    """Import chemfst module and handle import errors"""
    try:
        import chemfst
        print(f"[OK] Successfully imported chemfst module (version: {getattr(chemfst, '__version__', 'unknown')})")
        return chemfst
    except ImportError as e:
        print(f"[FAIL] Error importing chemfst module: {e}")
        print("INFO: Make sure you've built and installed the Python bindings.")
        sys.exit(1)


def setup_file_paths():
    """Setup and validate file paths"""
    input_path = Path("data/chemical_names.txt")
    fst_path = Path("data/chemical_names.fst")

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Please create a data/chemical_names.txt file with one chemical name per line.")
        sys.exit(1)

    return input_path, fst_path

def build_fst_index(chemfst, input_path, fst_path):
    """Build FST index from source file (always required)"""
    print("\n1. Building FST index from source file")
    print("--------------------------------------")
    print(f"Building FST index from {input_path}...")
    print("Note: The FST file is not distributed with the package and must be built from the source data.")

    start = time.time()
    chemfst.build_fst(str(input_path), str(fst_path))
    build_time = time.time() - start
    print(f"[OK] Built FST index in {build_time:.3f} seconds")
    print(f"FST index saved to {fst_path}")


def load_and_preload_fst(chemfst, fst_path):
    """Load FST and preload it into memory"""
    # Load FST
    print(f"\n2. Loading FST index from {fst_path}")
    print("-----------------------------------")
    start = time.time()
    fst = chemfst.ChemicalFST(os.fspath(fst_path))
    load_time = time.time() - start
    print(f"[OK] FST loaded in {load_time:.3f} seconds")

    # Preload FST
    print("\n3. Preloading FST into memory")
    print("----------------------------")
    print("Preloading forces all pages of the FST into memory, improving search performance.")
    start = time.time()
    count = fst.preload()
    preload_time = time.time() - start
    print(f"[OK] Preloaded {count} keys in {preload_time:.6f} seconds")

    return fst


def demonstrate_prefix_search(fst):
    """Demonstrate prefix search functionality"""
    print("\n4. Prefix search (autocomplete)")
    print("------------------------------")
    prefixes = ["eth", "meth", "prop", "benz"]

    for prefix in prefixes:
        print(f"\nSearching for chemicals starting with '{prefix}':")
        start = time.time()
        results = fst.prefix_search(prefix, max_results=5)
        search_time = time.time() - start

        if results:
            for chemical in results:
                print(f"  {chemical}")
            print(f"Found {len(results)} results in {search_time:.6f} seconds")
        else:
            print("  No matching chemicals found")


def demonstrate_substring_search(fst):
    """Demonstrate substring search functionality"""
    print("\n5. Substring search")
    print("-----------------")
    substrings = ["acid", "ol", "ene", "chlor"]

    for substring in substrings:
        print(f"\nSearching for chemicals containing '{substring}':")
        start = time.time()
        results = fst.substring_search(substring, max_results=5)
        search_time = time.time() - start

        if results:
            for chemical in results:
                print(f"  {chemical}")
            print(f"Found {len(results)} results in {search_time:.6f} seconds")
        else:
            print("  No matching chemicals found")


def run_performance_tests(fst):
    """Run performance testing"""
    print("\n6. Performance Benchmark")
    print("=======================")
    test_prefix = "a"
    iterations = 100

    print(f"Performing {iterations} prefix searches for '{test_prefix}'...")
    start = time.time()
    for _ in range(iterations):
        fst.prefix_search(test_prefix, max_results=10)

    total_time = time.time() - start
    avg_time = total_time / iterations

    print(f"Total time: {total_time:.3f} seconds")
    print(f"Average time per search: {avg_time:.6f} seconds")
    if avg_time == 0:
        print("Searches per second: inf (avg_time is zero)")
    else:
        print(f"Searches per second: {1/avg_time:.1f}")


def demonstrate_preloading_effect(chemfst, fst_path):
    """Demonstrate the effect of preloading on search performance"""
    print("\n7. Effect of Preloading on Search Latency")
    print("----------------------------------------")
    print("To demonstrate the effect of preloading, we'll measure the first search")
    print("time for each letter of the alphabet. This simulates a 'cold start'")
    print("scenario where different parts of the FST need to be loaded from disk.")
    print("\nNote: In a real application, this effect would be more noticeable with a much larger FST.")

    # Create a new FST instance without preloading
    fresh_fst = chemfst.ChemicalFST(str(fst_path))
    letters = list("abcdefghijklmnopqrstuvwxyz")

    # Test without preloading
    first_search_times = []
    print("\nTesting first-time searches for each letter without preloading:")
    for letter in letters:
        start = time.time()
        results = fresh_fst.prefix_search(letter, 10)
        search_time = time.time() - start
        first_search_times.append(search_time)
        print(f"  Letter '{letter}': {search_time*1000:.3f}ms ({len(results)} results)")

    avg_without_preload = sum(first_search_times) / len(first_search_times) * 1000
    max_without_preload = max(first_search_times) * 1000

    # Test with preloading
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

    if avg_without_preload == 0:
        improvement = float('inf')
    else:
        improvement = (avg_without_preload - avg_with_preload) / avg_without_preload * 100

    if max_without_preload == 0:
        max_improvement = float('inf')
    else:
        max_improvement = (max_without_preload - max_with_preload) / max_without_preload * 100

    print("\nPreloading Performance Impact:")
    print(f"  Without preloading: avg={avg_without_preload:.3f}ms, max={max_without_preload:.3f}ms")
    print(f"  With preloading:    avg={avg_with_preload:.3f}ms, max={max_with_preload:.3f}ms")
    if improvement == float('inf'):
        print("  Improvement:        inf% faster on average (avg_without_preload is zero)")
    else:
        print(f"  Improvement:        {improvement:.1f}% faster on average, {max_improvement:.1f}% faster for worst case")


def main():
    """Run comprehensive examples demonstrating ChemFST capabilities"""
    print("ChemFST Python Bindings - Comprehensive Examples")
    print("===============================================\n")

    # Setup
    chemfst = check_imports()
    input_path, fst_path = setup_file_paths()

    # Build FST index
    build_fst_index(chemfst, input_path, fst_path)

    # Load and preload FST
    fst = load_and_preload_fst(chemfst, fst_path)

    # Run demonstrations
    demonstrate_prefix_search(fst)
    demonstrate_substring_search(fst)
    run_performance_tests(fst)
    demonstrate_preloading_effect(chemfst, fst_path)

    print("\n[OK] ChemFST examples completed successfully!")
    print("\nNext steps:")
    print("- Try modifying the search terms in the examples")
    print("- Experiment with different max_results values")
    print("- Add your own chemical names to data/chemical_names.txt and rebuild the index")
    print("- Note: The .fst file is generated and not included in the package distribution")


if __name__ == "__main__":
    main()
