#!/usr/bin/env python3
"""
Example demonstrating logging with ChemFST Python bindings.

This example shows how to configure Python's logging system to capture
log messages from the Rust ChemFST library via pyo3-log.
"""

import logging
import sys
import os

# Add the parent directory to the path to import chemfst
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def setup_logging(level=logging.INFO):
    """Configure logging with a nice format."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a logger specifically for chemfst
    logger = logging.getLogger('chemfst')
    logger.setLevel(level)

    return logger

def main():
    print("ChemFST Logging Example")
    print("=" * 50)

    # Setup logging at INFO level
    logger = setup_logging(logging.INFO)
    logger.info("Starting ChemFST logging example")

    try:
        import chemfst

        # Example 1: Building an FST (this will generate logs)
        print("\n1. Building FST from sample data...")

        # Create sample data
        sample_data = [
            "acetone",
            "acetaldehyde",
            "acetic acid",
            "benzene",
            "benzoic acid",
            "ethanol",
            "methanol",
            "propanol"
        ]

        input_file = "/tmp/sample_chemicals.txt"
        fst_file = "/tmp/sample_chemicals.fst"

        with open(input_file, 'w') as f:
            for chemical in sample_data:
                f.write(f"{chemical}\n")

        # This will log the building process
        chemfst.build_fst(input_file, fst_file)

        # Example 2: Loading FST (this will generate logs)
        print("\n2. Loading FST...")
        fst = chemfst.ChemicalFST(fst_file)

        # Example 3: Performing searches with different log levels
        print("\n3. Performing searches...")

        # Prefix search (will log at INFO level)
        results = fst.prefix_search("acet", 5)
        print(f"Prefix search results: {results}")

        # Substring search (will log at INFO level)
        results = fst.substring_search("acid", 3)
        print(f"Substring search results: {results}")

        # Example 4: Preloading (will generate logs)
        print("\n4. Preloading FST...")
        count = fst.preload()
        print(f"Preloaded {count} entries")

        # Example 5: Enable DEBUG logging to see more details
        print("\n5. Enabling DEBUG logging for more detailed output...")
        logging.getLogger('chemfst').setLevel(logging.DEBUG)

        # Now these searches will show DEBUG logs too
        print("   Notice the DEBUG messages below:")
        results = fst.prefix_search("benz", 2)
        print(f"   Debug search results: {results}")

        # Also demonstrate substring search with DEBUG logging
        results = fst.substring_search("eth", 2)
        print(f"   Debug substring results: {results}")

        # Clean up
        os.remove(input_file)
        os.remove(fst_file)

        logger.info("ChemFST logging example completed successfully")

    except ImportError:
        print("Error: chemfst module not found. Make sure to build the Python extension first.")
        print("Run: cd chemfst-py && maturin develop")
    except Exception as e:
        logger.error(f"Error during example: {e}")
        raise

if __name__ == "__main__":
    main()
