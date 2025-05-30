# ChemFST

[![PyPI version](https://badge.fury.io/py/chemfst.svg)](https://badge.fury.io/py/chemfst)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-mdBook-blue)](https://esrehmki.github.io/chemfst/)

Python bindings for ChemFST: a high-performance chemical name search library using Finite State Transducers (FSTs).

## Features

- **Memory-efficient indexing** using Finite State Transducers
- **Extremely fast prefix searches** for autocomplete functionality
- **Case-insensitive substring searches** for finding chemical names
- **Memory-mapped file access** for optimal performance
- **Native Rust implementation** with Python bindings

## Installation

```bash
pip install chemfst
```

Requires Python 3.11 or higher.

## Quick Start

```python
from chemfst import ChemicalFST, build_fst

# Build an FST index from a list of chemical names (required - not distributed)
# Note: The .fst file is generated and not included in the package
build_fst("data/chemical_names.txt", "data/chemical_names.fst")

# Load the FST for searching
fst = ChemicalFST("data/chemical_names.fst")

# Prefix search (autocomplete)
matches = fst.prefix_search("acet", max_results=10)
print(f"Chemicals starting with 'acet': {matches}")

# Substring search
matches = fst.substring_search("benz", max_results=10)
print(f"Chemicals containing 'benz': {matches}")
```

## Input Format

The input file should contain one chemical name per line:

```
acetone
benzene
methanol
ethanol
...
```

## API Reference

### `build_fst(input_path, output_path)`

Create an FST index from a list of chemical names in a text file. The resulting .fst file is generated and not distributed with the package.

- **input_path**: Path to text file containing chemical names (one per line)
- **output_path**: Path where the FST index will be saved (not distributed with package)

### `ChemicalFST(fst_path)`

Initialize a chemical name search engine.

- **fst_path**: Path to the FST index file

#### Methods

- **`prefix_search(prefix, max_results=100)`**:
  Find chemical names starting with a specified prefix

- **`substring_search(substring, max_results=100)`**:
  Find chemical names containing a specified substring

## Performance

ChemFST uses memory mapping and Finite State Transducers to achieve excellent performance:

- **Fast loading**: The FST is memory-mapped, not fully loaded into memory
- **Low memory usage**: Compact FST representation uses minimal RAM
- **Quick prefix searches**: Typically < 1ms for prefix searches
- **Efficient substring searches**: Faster than regex or database lookups

## Building from Source

```bash
git clone https://github.com/username/ChemFST
cd ChemFST
pip install maturin
maturin develop
```

## License

MIT

## Credits

ChemFST is built using the [fst](https://github.com/BurntSushi/fst) Rust crate by BurntSushi for the Finite State Transducer implementation.
