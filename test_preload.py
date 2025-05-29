#!/usr/bin/env python3
"""
Test script for demonstrating the preloading functionality in ChemFST

This script compares the performance of FST searches with and without preloading
to show the impact on search latency, especially for first-time searches.
"""

import time
import random
import string
import sys
from pathlib import Path

def measure_search_performance(fst_path, iterations=100, with_preload=False):
    """Measure search performance with or without preloading"""
    try:
        import chemfst
    except ImportError:
        print("Error: chemfst module not found. Make sure it's installed.")
        sys.exit(1)
        
    # Load the FST
    load_start = time.time()
    fst = chemfst.ChemicalFST(str(fst_path))
    load_time = time.time() - load_start
    print(f"FST loaded in {load_time:.6f} seconds")
    
    # Preload if requested
    if with_preload:
        print("Preloading FST into memory...")
        preload_start = time.time()
        key_count = fst.preload()
        preload_time = time.time() - preload_start
        print(f"Preloaded {key_count} keys in {preload_time:.6f} seconds")
    
    # Generate test prefixes covering different parts of the alphabet
    prefixes = list(string.ascii_lowercase)
    # Generate test substrings
    substrings = ['ol', 'ene', 'acid', 'yl', 'eth', 'meth', 'carb']
    
    # Test prefix search performance
    print("\n=== Prefix Search Performance ===")
    first_search_times = []
    subsequent_times = []
    
    for i, prefix in enumerate(prefixes):
        # Test first search for each prefix
        start = time.time()
        results = fst.prefix_search(prefix, max_results=100)
        search_time = time.time() - start
        first_search_times.append(search_time)
        
        # Print some stats for the first few prefixes
        if i < 5 or i >= len(prefixes) - 5:
            print(f"Prefix '{prefix}': found {len(results)} results in {search_time*1000:.3f}ms")
        elif i == 5:
            print("...")
        
        # Do 3 more searches with the same prefix to test subsequent search speed
        for _ in range(3):
            start = time.time()
            fst.prefix_search(prefix, max_results=100)
            subsequent_times.append(time.time() - start)
    
    # Test substring search performance
    print("\n=== Substring Search Performance ===")
    sub_first_times = []
    sub_subsequent_times = []
    
    for substring in substrings:
        # Test first search for each substring
        start = time.time()
        results = fst.substring_search(substring, max_results=100)
        search_time = time.time() - start
        sub_first_times.append(search_time)
        
        print(f"Substring '{substring}': found {len(results)} results in {search_time*1000:.3f}ms")
        
        # Do 3 more searches with the same substring
        for _ in range(3):
            start = time.time()
            fst.substring_search(substring, max_results=100)
            sub_subsequent_times.append(time.time() - start)
    
    # Calculate statistics
    avg_first = sum(first_search_times) / len(first_search_times) * 1000  # ms
    max_first = max(first_search_times) * 1000  # ms
    avg_subsequent = sum(subsequent_times) / len(subsequent_times) * 1000  # ms
    
    avg_sub_first = sum(sub_first_times) / len(sub_first_times) * 1000  # ms
    max_sub_first = max(sub_first_times) * 1000  # ms
    avg_sub_subsequent = sum(sub_subsequent_times) / len(sub_subsequent_times) * 1000  # ms
    
    # Print performance summary
    print("\n=== Performance Summary ===")
    print(f"Prefix search (first time): avg={avg_first:.3f}ms, max={max_first:.3f}ms")
    print(f"Prefix search (subsequent): avg={avg_subsequent:.3f}ms")
    print(f"Substring search (first time): avg={avg_sub_first:.3f}ms, max={max_sub_first:.3f}ms")
    print(f"Substring search (subsequent): avg={avg_sub_subsequent:.3f}ms")
    
    return {
        "avg_first_prefix": avg_first,
        "max_first_prefix": max_first,
        "avg_subsequent_prefix": avg_subsequent,
        "avg_first_substring": avg_sub_first,
        "max_first_substring": max_sub_first,
        "avg_subsequent_substring": avg_sub_subsequent,
    }

def main():
    """Run preload testing"""
    print("ChemFST Preloading Performance Test")
    print("==================================")
    
    fst_path = Path("chemical_names.fst")
    if not fst_path.exists():
        print(f"Error: FST file not found at {fst_path}")
        print("Please build the FST first using ChemFST")
        sys.exit(1)
    
    # Test without preloading
    print("\n--- Without Preloading ---")
    no_preload_stats = measure_search_performance(fst_path, with_preload=False)
    
    # Add a separator to distinguish runs
    print("\n" + "="*50 + "\n")
    
    # Test with preloading
    print("\n--- With Preloading ---")
    preload_stats = measure_search_performance(fst_path, with_preload=True)
    
    # Calculate improvements
    prefix_first_improvement = (no_preload_stats["avg_first_prefix"] - preload_stats["avg_first_prefix"]) / no_preload_stats["avg_first_prefix"] * 100
    prefix_max_improvement = (no_preload_stats["max_first_prefix"] - preload_stats["max_first_prefix"]) / no_preload_stats["max_first_prefix"] * 100
    prefix_subsequent_improvement = (no_preload_stats["avg_subsequent_prefix"] - preload_stats["avg_subsequent_prefix"]) / no_preload_stats["avg_subsequent_prefix"] * 100
    
    substring_first_improvement = (no_preload_stats["avg_first_substring"] - preload_stats["avg_first_substring"]) / no_preload_stats["avg_first_substring"] * 100
    substring_max_improvement = (no_preload_stats["max_first_substring"] - preload_stats["max_first_substring"]) / no_preload_stats["max_first_substring"] * 100
    substring_subsequent_improvement = (no_preload_stats["avg_subsequent_substring"] - preload_stats["avg_subsequent_substring"]) / no_preload_stats["avg_subsequent_substring"] * 100
    
    # Print comparison
    print("\n=== Performance Improvement Summary ===")
    print(f"Prefix search (first time):    {prefix_first_improvement:.1f}% faster")
    print(f"Prefix search (worst case):    {prefix_max_improvement:.1f}% faster")
    print(f"Prefix search (subsequent):    {prefix_subsequent_improvement:.1f}% faster")
    print(f"Substring search (first time): {substring_first_improvement:.1f}% faster")
    print(f"Substring search (worst case): {substring_max_improvement:.1f}% faster")
    print(f"Substring search (subsequent): {substring_subsequent_improvement:.1f}% faster")

if __name__ == "__main__":
    main()