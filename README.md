# ChemFST

ChemFST is a high-performance chemical name search library using Finite State Transducers (FSTs) to provide efficient searches of systematic and trivial names of chemical compounds in milliseconds. It's particularly useful for autocomplete features and searching through large chemical compound databases.

## Features

- Memory-efficient indexing using Finite State Transducers
- Extremely fast prefix-based searches (autocomplete)
- Case-insensitive substring searches
- Memory-mapped file access for optimal performance
- Simple API with just a few functions

## Setup

### Prerequisites

- [Rust](https://www.rust-lang.org/tools/install) 1.56.0 or higher
- Cargo (comes with Rust)

### Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
chemfst = { path = "path/to/chemfst" }
```

For a real-world application, you would publish the crate to [crates.io](https://crates.io/) and then specify:

```toml
[dependencies]
chemfst = "0.1.0"
```

## Using the Library

### Basic Usage

```rust
use chemfst::{build_fst_set, load_fst_set, prefix_search, substring_search};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // Step 1: Create an index from a list of chemical names (one term per line)
    let input_path = "chemical_names.txt";
    let fst_path = "chemical_names.fst";
    build_fst_set(input_path, fst_path)?;
    
    // Step 2: Load the index into memory
    let set = load_fst_set(fst_path)?;
    
    // Step 3: Perform searches
    
    // Prefix search (autocomplete)
    let prefix_results = prefix_search(&set, "acet", 10); // Find up to 10 terms starting with "acet"
    
    // Substring search
    let substring_results = substring_search(&set, "benz", 10)?; // Find up to 10 terms containing "benz"
    
    Ok(())
}
```

### API Reference

#### `build_fst_set(input_path: &str, fst_path: &str) -> Result<(), Box<dyn Error>>`

Creates an FST set from a list of chemical names in a text file.

- `input_path`: Path to a text file with one chemical name per line
- `fst_path`: Path where the FST index will be saved

#### `load_fst_set(fst_path: &str) -> Result<Set<Mmap>, Box<dyn Error>>`

Loads a previously created FST set from disk using memory mapping.

- `fst_path`: Path to the FST index file
- Returns: A memory-mapped FST Set

#### `prefix_search(set: &Set<Mmap>, prefix: &str, max_results: usize) -> Vec<String>`

Performs a prefix-based search (autocomplete).

- `set`: The FST Set to search through
- `prefix`: The prefix to search for
- `max_results`: Maximum number of results to return
- Returns: A vector of matching chemical names

#### `substring_search(set: &Set<Mmap>, substring: &str, max_results: usize) -> Result<Vec<String>, Box<dyn Error>>`

Performs a case-insensitive substring search.

- `set`: The FST Set to search through
- `substring`: The substring to search for
- `max_results`: Maximum number of results to return
- Returns: A vector of matching chemical names

## Development

### Project Structure

- `src/lib.rs` - Core library functionality
- `src/main.rs` - Example binary that demonstrates the library
- `tests/` - Integration tests

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd chemfst
   ```

2. Build the project:
   ```bash
   cargo build
   ```

3. Run the example:
   ```bash
   cargo run
   ```

### Running Tests

Run all tests:
```bash
cargo test
```

### Adding New Tests

Add new integration tests to the `tests/fst_search_tests.rs` file or create additional test files in the `tests` directory.

### Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run the tests (`cargo test`)
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

## Performance Considerations

- FST sets are immutable. If your chemical database changes, you'll need to rebuild the index.
- For large chemical databases, consider building the index as an offline process.
- Memory-mapped files provide excellent performance but require care when the underlying file changes.

## License

[MIT License](LICENSE)

## Credits

This project uses the following key dependencies:
- [fst](https://crates.io/crates/fst) - Finite State Transducer implementation
- [memmap2](https://crates.io/crates/memmap2) - Memory mapping functionality