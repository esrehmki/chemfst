#!/usr/bin/env python3
"""
Pytest unit tests for ChemFST preloading functionality.
"""

import pytest
import time


class TestChemFSTPreload:
    """Test class for ChemFST preloading functionality"""

    def test_preload_returns_positive_count(self, fst_instance):
        """Test that preload returns a positive count of keys"""
        count = fst_instance.preload()
        assert isinstance(count, int)
        assert count > 0

    def test_search_consistency_after_preload(self, fst_instance):
        """Test that search results are consistent before and after preloading"""
        test_prefix = "eth"
        test_substring = "acid"

        # Get results before preloading
        prefix_results_before = fst_instance.prefix_search(test_prefix, max_results=10)
        substring_results_before = fst_instance.substring_search(test_substring, max_results=10)

        # Preload
        fst_instance.preload()

        # Get results after preloading
        prefix_results_after = fst_instance.prefix_search(test_prefix, max_results=10)
        substring_results_after = fst_instance.substring_search(test_substring, max_results=10)

        # Results should be identical
        assert prefix_results_before == prefix_results_after
        assert substring_results_before == substring_results_after

    def test_multiple_preloads(self, fst_instance):
        """Test that multiple preload calls work correctly"""
        count1 = fst_instance.preload()
        count2 = fst_instance.preload()

        # Both should return the same count
        assert count1 == count2
        assert count1 > 0


if __name__ == "__main__":
    pytest.main([__file__])
