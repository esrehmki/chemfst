#!/usr/bin/env python3
"""
Shared pytest fixtures for ChemFST tests.

This module provides shared fixtures for testing ChemFST functionality.
The key requirement is that FST files (.fst) are NOT distributed with the package
and must be built from source text files during testing.

Key fixtures:
- chemical_names_txt: Provides path to source chemical names text file
- fst_file: Builds FST file from source if needed (session-scoped for efficiency)
- fst_instance: Provides fresh ChemicalFST instance for each test
"""

import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def chemical_names_txt():
    """Fixture to provide path to chemical names text file"""
    path = Path("data/chemical_names.txt")
    if not path.exists():
        pytest.fail(f"Chemical names text file not found at {path}")
    return path


@pytest.fixture(scope="session")
def fst_file(chemical_names_txt):
    """Fixture to provide FST file, building it if necessary"""
    import chemfst

    fst_path = Path("data/chemical_names.fst")

    # Build FST if it doesn't exist
    if not fst_path.exists():
        chemfst.build_fst(str(chemical_names_txt), str(fst_path))

    return fst_path


@pytest.fixture
def fst_instance(fst_file):
    """Fixture to provide fresh ChemicalFST instance"""
    import chemfst
    return chemfst.ChemicalFST(str(fst_file))
