#!/usr/bin/env python3
"""
Comprehensive demonstration of different logging levels with ChemFST Python bindings.

This example shows how different log levels (DEBUG, INFO, WARNING, ERROR) work
with the ChemFST library, demonstrating the logging bridge from Rust to Python.
"""

import logging
import sys
import os
import tempfile

# Add the parent directory to the path to import chemfst
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def setup_logging_with_level(level, level_name):
    """Configure logging with a specific level."""
    # Clear any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True  # Force reconfiguration
    )

    # Set the chemfst logger to the same level
    logger = logging.getLogger('chemfst')
    logger.setLevel(level)

    print(f"\n[CONFIG] Logging configured at {level_name} level")
    print("=" * 60)

    return logger

def demo_logging_level(level, level_name):
    """Demonstrate logging at a specific level."""
    logger = setup_logging_with_level(level, level_name)

    try:
        import chemfst

        # Create temporary test data
        test_data = ["acetone", "benzene", "toluene", "ethanol"]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            input_file = f.name
            for chemical in test_data:
                f.write(f"{chemical}\n")

        fst_file = input_file.replace('.txt', '.fst')

        try:
            print(f"[BUILD] Building FST (expect to see {level_name}+ messages):")
            chemfst.build_fst(input_file, fst_file)

            print(f"[LOAD] Loading FST:")
            fst = chemfst.ChemicalFST(fst_file)

            print(f"[SEARCH] Performing prefix search:")
            results = fst.prefix_search("eth", 2)
            print(f"   Results: {results}")

            print(f"[SEARCH] Performing substring search:")
            results = fst.substring_search("en", 3)
            print(f"   Results: {results}")

            print(f"[PRELOAD] Preloading FST:")
            count = fst.preload()
            print(f"   Preloaded: {count} entries")

        finally:
            # Clean up
            if os.path.exists(input_file):
                os.remove(input_file)
            if os.path.exists(fst_file):
                os.remove(fst_file)

    except ImportError:
        print("[ERROR] Error: chemfst module not found. Build it first: cd chemfst-py && maturin develop")
    except Exception as e:
        logger.error(f"[ERROR] Error during demo: {e}")

def demo_error_logging():
    """Demonstrate error logging."""
    print("\n[DEMO] ERROR LOGGING DEMONSTRATION")
    print("=" * 60)

    # Configure logging at DEBUG level to see all messages
    setup_logging_with_level(logging.DEBUG, "DEBUG")

    try:
        import chemfst

        print("[TEST] Attempting to build FST from non-existent file:")
        try:
            chemfst.build_fst("does_not_exist.txt", "output.fst")
        except FileNotFoundError as e:
            print(f"   Expected error caught: {e}")

        print("[TEST] Attempting to load non-existent FST:")
        try:
            fst = chemfst.ChemicalFST("does_not_exist.fst")
        except FileNotFoundError as e:
            print(f"   Expected error caught: {e}")

    except ImportError:
        print("[ERROR] Error: chemfst module not found.")

def main():
    print("[DEMO] ChemFST Logging Levels Demonstration")
    print("=" * 70)
    print("This demo shows how different logging levels affect message visibility.")
    print("Higher levels include all messages from lower levels.")
    print()

    # Demo each logging level
    demo_logging_level(logging.ERROR, "ERROR")
    demo_logging_level(logging.WARNING, "WARNING")
    demo_logging_level(logging.INFO, "INFO")
    demo_logging_level(logging.DEBUG, "DEBUG")

    # Demo error cases
    demo_error_logging()

    print("\n[SUCCESS] Logging demonstration completed!")
    print("\nSummary:")
    print("- ERROR level: Only shows error messages")
    print("- WARNING level: Shows warning and error messages")
    print("- INFO level: Shows info, warning, and error messages")
    print("- DEBUG level: Shows all messages including detailed debug info")

if __name__ == "__main__":
    main()
