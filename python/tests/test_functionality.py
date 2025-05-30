#!/usr/bin/env python3
"""
Pytest unit tests for ChemFST functionality testing.
"""

import pytest


class TestChemFSTFunctionality:
    """Test class for ChemFST core functionality"""

    def test_build_fst_functionality(self, chemical_names_txt, tmp_path):
        """Test that build_fst creates a valid FST file"""
        import chemfst

        # Create temporary FST file path
        temp_fst = tmp_path / "test.fst"

        # Build FST
        chemfst.build_fst(str(chemical_names_txt), str(temp_fst))

        # Verify FST file was created
        assert temp_fst.exists()
        assert temp_fst.stat().st_size > 0

        # Verify FST can be loaded and used
        fst = chemfst.ChemicalFST(str(temp_fst))
        results = fst.prefix_search("a", max_results=1)
        assert isinstance(results, list)

    def test_chemfst_instance_creation(self, fst_file):
        """Test that ChemicalFST instance can be created"""
        import chemfst
        fst = chemfst.ChemicalFST(str(fst_file))
        assert fst is not None

    def test_prefix_search_functionality(self, fst_instance):
        """Test that prefix search returns results"""
        results = fst_instance.prefix_search("eth", 5)
        assert isinstance(results, list)
        assert len(results) <= 5

        # All results should start with the prefix
        for result in results:
            assert isinstance(result, str)
            assert result.lower().startswith("eth")

    def test_substring_search_functionality(self, fst_instance):
        """Test that substring search returns results"""
        results = fst_instance.substring_search("benz", 5)
        assert isinstance(results, list)
        assert len(results) <= 5

        # All results should contain the substring
        for result in results:
            assert isinstance(result, str)
            assert "benz" in result.lower()

    def test_prefix_search_empty_results(self, fst_instance):
        """Test prefix search with non-existent prefix"""
        results = fst_instance.prefix_search("xyzzyx", 5)
        assert isinstance(results, list)
        assert len(results) == 0

    def test_substring_search_empty_results(self, fst_instance):
        """Test substring search with non-existent substring"""
        results = fst_instance.substring_search("xyzzyx", 5)
        assert isinstance(results, list)
        assert len(results) == 0

    def test_max_results_parameter(self, fst_instance):
        """Test that max_results parameter is respected"""
        results_3 = fst_instance.prefix_search("a", 3)
        results_10 = fst_instance.prefix_search("a", 10)

        assert len(results_3) <= 3
        assert len(results_10) <= 10

        if len(results_10) >= 3:
            assert len(results_3) <= len(results_10)

    def test_preload_functionality(self, fst_instance):
        """Test that preload function works and returns count"""
        count = fst_instance.preload()
        assert isinstance(count, int)
        assert count > 0


if __name__ == "__main__":
    pytest.main([__file__])
