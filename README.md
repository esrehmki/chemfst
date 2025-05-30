# ChemFST

[![Python CI](https://github.com/esrehmki/chemfst/actions/workflows/python.yml/badge.svg)](https://github.com/esrehmki/chemfst/actions/workflows/python.yml)
[![Rust CI](https://github.com/esrehmki/chemfst/actions/workflows/rust.yml/badge.svg)](https://github.com/esrehmki/chemfst/actions/workflows/rust.yml)
[![Docs](https://img.shields.io/badge/docs-mdBook-blue)](https://esrehmki.github.io/chemfst/)

ChemFST is a high-performance chemical name search library using Finite State Transducers (FSTs) for efficient search and autocomplete of chemical compound names. The project provides both a native Rust library and Python bindings.

- **Rust library:** Fast, memory-efficient, and suitable for large-scale chemical name search and autocomplete.
- **Python bindings:** Easy integration with Python projects, powered by the same Rust core.

For detailed usage, API reference, and in-depth explanations, please see the [ChemFST Documentation (mdBook)](https://esrehmki.github.io/chemfst/).

---

## Development

### Project Structure

- `src/` – Rust library source code
- `python/` – Python bindings and packaging
- `docs/` – Documentation (mdBook sources)
- `tests/` – Integration and unit tests

### Local Setup

#### Rust

1. Install [Rust](https://www.rust-lang.org/tools/install) (1.56.0 or higher).
2. Clone the repository:
   ```bash
   git clone https://github.com/esrehmki/chemfst.git
   cd chemfst
   ```
3. Build the project:
   ```bash
   cargo build
   ```
4. Run tests:
   ```bash
   cargo test
   ```

#### Python

1. Requires Python 3.11 or higher.
2. Install [maturin](https://github.com/PyO3/maturin) for building the Python bindings:
   ```bash
   pip install maturin
   ```
3. Build and install the Python package:
   ```bash
   cd python
   maturin develop
   ```
4. Run Python tests:
   ```bash
   pytest
   ```

### Continuous Integration

- GitHub Actions workflows for both Rust and Python ensure cross-platform compatibility and code quality.
- See `.github/workflows/` for workflow definitions.

### Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and add tests.
4. Run all tests to ensure nothing is broken.
5. Commit and push your changes.
6. Open a Pull Request.

### License

[MIT License](LICENSE)

---

For all usage instructions, API details, and advanced topics, please visit the [ChemFST Documentation (mdBook)](https://esrehmki.github.io/chemfst/).
