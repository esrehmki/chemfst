#!/usr/bin/env python3
"""
Simple test to verify that logging is working correctly with ChemFST.
"""

import logging
import tempfile
import os
import pytest

def test_logging():
    # Configure logging to capture all messages
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        force=True
    )

    logger = logging.getLogger('chemfst')
    logger.info("Starting logging test")

    try:
        import chemfst
    except ImportError:
        pytest.fail("chemfst module not found. Build the extension first: cd chemfst-py && maturin develop")

    # Create temporary test data
    test_data = ["acetone", "benzene", "ethanol", "methanol"]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        input_file = f.name
        for chemical in test_data:
            f.write(f"{chemical}\n")

    fst_file = input_file.replace('.txt', '.fst')

    try:
        # Test 1: Building FST (should log)
        print("Testing FST building...")
        chemfst.build_fst(input_file, fst_file)
        assert os.path.exists(fst_file), "FST file should be created"

        # Test 2: Loading FST (should log)
        print("Testing FST loading...")
        fst = chemfst.ChemicalFST(fst_file)
        assert fst is not None, "FST should load successfully"

        # Test 3: Search operations (should log)
        print("Testing search operations...")
        results = fst.prefix_search("eth", 5)
        print(f"Prefix search found: {results}")
        assert isinstance(results, list), "Prefix search should return a list"
        assert len(results) == 1, "Should find 1 result for 'eth'"
        assert "ethanol" in results, "Should find 'ethanol'"

        results = fst.substring_search("ol", 5)
        print(f"Substring search found: {results}")
        assert isinstance(results, list), "Substring search should return a list"
        assert len(results) == 2, "Should find 2 results for 'ol'"
        assert "ethanol" in results, "Should find 'ethanol'"
        assert "methanol" in results, "Should find 'methanol'"

        # Test 4: Preload (should log)
        print("Testing preload...")
        count = fst.preload()
        print(f"Preloaded {count} entries")
        assert isinstance(count, int), "Preload should return an integer count"
        assert count == 4, "Should preload 4 entries"

        print("All tests completed successfully!")

        # Release the FST instance before cleanup
        del fst

    finally:
        # Clean up
        if os.path.exists(input_file):
            os.remove(input_file)
        if os.path.exists(fst_file):
            os.remove(fst_file)

    logger.info("Logging test completed successfully")

def test_logging_error_cases():
    """Test that error cases generate appropriate log messages."""
    # Configure logging to capture all messages
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        force=True
    )

    logger = logging.getLogger('chemfst')

    try:
        import chemfst
    except ImportError:
        pytest.fail("chemfst module not found")

    # Test 1: File not found error during build
    with pytest.raises(FileNotFoundError):
        chemfst.build_fst("nonexistent_file.txt", "output.fst")

    # Test 2: File not found error during load
    with pytest.raises(FileNotFoundError):
        chemfst.ChemicalFST("nonexistent.fst")

    logger.info("Error case logging test completed successfully")


def test_logging_levels():
    """Test that different log levels work correctly."""
    import chemfst
    import tempfile
    import os

    # Create test data
    test_data = ["benzene", "toluene"]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        input_file = f.name
        for chemical in test_data:
            f.write(f"{chemical}\n")

    fst_file = input_file.replace('.txt', '.fst')

    try:
        # Build FST
        chemfst.build_fst(input_file, fst_file)
        fst = chemfst.ChemicalFST(fst_file)

        # Test with INFO level (should not show DEBUG messages)
        logging.getLogger('chemfst').setLevel(logging.INFO)
        results = fst.prefix_search("benz", 5)
        assert len(results) == 1
        assert "benzene" in results

        # Test with DEBUG level (should show DEBUG messages)
        logging.getLogger('chemfst').setLevel(logging.DEBUG)
        results = fst.prefix_search("tol", 5)
        assert len(results) == 1
        assert "toluene" in results

        # Test with WARNING level (should show minimal messages)
        logging.getLogger('chemfst').setLevel(logging.WARNING)
        results = fst.substring_search("ene", 5)
        assert len(results) == 2

        # Release the FST instance before cleanup
        del fst

    finally:
        # Clean up
        if os.path.exists(input_file):
            os.remove(input_file)
        if os.path.exists(fst_file):
            os.remove(fst_file)


if __name__ == "__main__":
    test_logging()
    test_logging_error_cases()
    test_logging_levels()
    print("\n[SUCCESS] All logging tests passed!")
