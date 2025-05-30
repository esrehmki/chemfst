"""Python bindings for ChemFST: High-performance chemical name search library

This package provides Python bindings for ChemFST, a Rust library that uses
Finite State Transducers (FSTs) for efficient searching of chemical names.
"""

__version__ = "0.1.1"

# Import directly from the compiled module
from chemfst import ChemicalFST, build_fst

__all__ = ["ChemicalFST", "build_fst"]
