# ChemFST Python

[![Python CI](https://github.com/esrehmki/chemfst/actions/workflows/python.yml/badge.svg)](https://github.com/esrehmki/chemfst/actions/workflows/python.yml)
[![PyPI version](https://badge.fury.io/py/chemfst.svg)](https://badge.fury.io/py/chemfst)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python bindings for ChemFST: a high-performance chemical name search library using Finite State Transducers (FSTs).

## Features

- **Memory-efficient indexing** using Finite State Transducers
- **Extremely fast prefix searches** for autocomplete functionality
- **Case-insensitive substring searches** for finding chemical names
- **Memory-mapped file access** for optimal performance
- **Native Rust implementation** with Python bindings
- **Comprehensive logging** integrated with Python's logging system

## Installation

```bash
pip install chemfst
```

Requires Python 3.11 or higher.

## Quick Start

```python
from chemfst import ChemicalFST, build_fst
import logging

# Optional: Configure logging to see operation details
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(levelname)s: %(message)s')

# Build an FST index from chemical names (one name per line)
build_fst("data/chemical_names.txt", "data/chemical_names.fst")

# Load the FST for searching
fst = ChemicalFST("data/chemical_names.fst")

# Prefix search (autocomplete)
matches = fst.prefix_search("acet", max_results=10)
print(f"Chemicals starting with 'acet': {matches}")

# Substring search
matches = fst.substring_search("benz", max_results=10)
print(f"Chemicals containing 'benz': {matches}")

# Preload for better performance
count = fst.preload()
print(f"Preloaded {count} entries")
```

## API Reference

### `build_fst(input_path, output_path)`

Create an FST index from a text file containing chemical names (one per line).

### `ChemicalFST(fst_path)`

Initialize a chemical name search engine from an FST file.

**Methods:**

- `prefix_search(prefix, max_results=100)` - Find names starting with prefix
- `substring_search(substring, max_results=100)` - Find names containing substring
- `preload()` - Load all data into memory for faster searches

## Logging

ChemFST integrates with Python's standard logging module to provide detailed operation insights.

### Basic Logging Setup

```python
import logging
import chemfst

logging.basicConfig(level=logging.INFO)
# ChemFST operations will now generate log messages
```

### Log Levels

- **ERROR**: File errors, operation failures
- **INFO**: Operation summaries, result counts, timing
- **DEBUG**: Detailed parameters, internal operations

### Advanced Logging

```python
# DEBUG level for development
logging.getLogger('chemfst').setLevel(logging.DEBUG)

# Custom formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    filename='chemfst.log'
)
```

### Example Log Output

```
2024-01-15 10:30:15 [chemfst] INFO: Building FST from input file: data/chemicals.txt
2024-01-15 10:30:15 [chemfst] INFO: Read 50000 chemical names from input file
2024-01-15 10:30:16 [chemfst] INFO: Successfully built FST with 50000 entries
2024-01-15 10:30:20 [chemfst] INFO: Prefix search for 'acet' found 3 results (checked 3 entries)
```

## Performance

- **Fast loading**: Memory-mapped FST files, no full loading required
- **Low memory usage**: Compact FST representation
- **Quick searches**: Typically < 1ms for prefix searches
- **Efficient substring searches**: Faster than regex or database lookups

Performance logging available at DEBUG level for optimization.

## Input Format

Chemical names file (one per line):

```
acetone
benzene
methanol
ethanol
```

## Development

### Building from Source

```bash
git clone https://github.com/username/ChemFST
cd ChemFST/chemfst-py
pip install maturin
maturin develop
```

### Running Tests

```bash
python -m pytest python/tests/ -v
```

### Examples

See `python/examples/` for complete usage examples including logging configuration.

## License

MIT
