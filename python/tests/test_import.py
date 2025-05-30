#!/usr/bin/env python3
"""
Pytest unit tests for ChemFST Python bindings import functionality.
"""

import pytest

class TestChemFSTImports:
    """Test class for ChemFST module imports"""

    def test_chemfst_module_import(self):
        """Test that the main chemfst module can be imported"""
        try:
            import chemfst
            assert hasattr(chemfst, '__name__')
        except ImportError:
            pytest.fail("Failed to import chemfst module")

    def test_chemical_fst_class_import(self):
        """Test that ChemicalFST class can be imported from chemfst"""
        try:
            from chemfst import ChemicalFST
            assert ChemicalFST is not None
            assert callable(ChemicalFST)
        except ImportError:
            pytest.fail("Failed to import ChemicalFST from chemfst")

    def test_build_fst_function_import(self):
        """Test that build_fst function can be imported from chemfst"""
        try:
            from chemfst import build_fst
            assert build_fst is not None
            assert callable(build_fst)
        except ImportError:
            pytest.fail("Failed to import build_fst from chemfst")

    def test_chemfst_module_contents(self):
        """Test that chemfst module has expected attributes"""
        import chemfst

        expected_attributes = ['ChemicalFST', 'build_fst']
        for attr in expected_attributes:
            assert hasattr(chemfst, attr), f"chemfst module missing expected attribute: {attr}"

if __name__ == "__main__":
    pytest.main([__file__])
