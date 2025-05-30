# FST File Setup Guide

## Overview

ChemFST uses Finite State Transducer (FST) files for high-performance chemical name searching. **FST files (.fst) are not distributed with the package** and must be generated from source text files.

## Why FST Files Are Not Distributed

1. **Generated Content**: FST files are compiled indexes created from source data
2. **Size Considerations**: FST files can be large depending on the dataset
3. **Customization**: Users typically want to use their own chemical name datasets
4. **License Clarity**: Source text files may have different licensing than generated indexes

## Required Files

### Source File: `data/chemical_names.txt`
- **Required**: Must exist to generate FST files
- **Format**: One chemical name per line, UTF-8 encoded
- **Included**: The repository includes a sample file with 32+ chemical names
- **Example content** (from included file):
  ```
  acetaminophen
  acetylsalicylic acid
  acetic acid
  acetone
  acetonitrile
  benzene
  benzoic acid
  ...
  ```

### Generated File: `data/chemical_names.fst`
- **Generated**: Created by ChemFST from the source text file
- **Not tracked**: Ignored by git (see `.gitignore`)
- **Not distributed**: Must be built locally

## Building FST Files

### Python API
```python
from chemfst import build_fst

# Build FST index from text file
build_fst("data/chemical_names.txt", "data/chemical_names.fst")
```

### Rust API
```rust
use chemfst::build_fst_set;

// Build FST index from text file
build_fst_set("data/chemical_names.txt", "data/chemical_names.fst")?;
```

## Automated Testing

The test suite automatically handles FST file generation:

1. **Source File Check**: Tests verify `data/chemical_names.txt` exists
2. **Auto-Generation**: FST files are built automatically during testing if missing
3. **Session Scope**: FST generation is cached across test sessions for efficiency
4. **Cleanup**: Generated files are properly ignored by version control

## Git Configuration

The repository is configured to ignore FST files:

```gitignore
# Generated FST files (not distributed with package)
data/chemical_names.fst
*.fst
```

## Troubleshooting

### Missing Source File
**Error**: `Chemical names text file not found at data/chemical_names.txt`

**Solution**: The repository includes a sample `data/chemical_names.txt` file. If missing, create the source file with chemical names (one per line) or restore it from version control.

### Permission Issues
**Error**: Cannot write FST file

**Solution**: Ensure write permissions for the data directory

### Empty Results
**Error**: Search returns no results

**Solution**: Verify source file contains the expected chemical names

## Best Practices

1. **Use Existing Data**: The repository includes a curated `chemical_names.txt` file with sample data
2. **Backup Source Files**: Keep `chemical_names.txt` in version control (already included)
3. **Ignore Generated Files**: Never commit `.fst` files to version control
4. **Document Data Sources**: Include attribution for chemical name datasets
5. **Test Locally**: Always test FST generation before deployment
6. **Automation**: Include FST building in deployment scripts
7. **Customize Data**: Replace the sample data with your own chemical names as needed

## Performance Notes

- **Build Time**: FST generation is fast (typically milliseconds for small datasets)
- **Memory Usage**: FST files are memory-mapped for efficient loading
- **Search Speed**: FST searches are optimized for sub-millisecond response times
- **Preloading**: Use the preload functionality for even better performance

## Examples

See `python/examples/demo.py` for a comprehensive example that:
1. Builds FST from source file
2. Loads the generated FST
3. Demonstrates search functionality
4. Shows performance characteristics
