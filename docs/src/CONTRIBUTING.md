# Contributing to ChemFST

Thank you for considering contributing to ChemFST! This document provides guidelines and instructions to help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How to Contribute

### Reporting Issues

- Check if the issue has already been reported.
- Use the issue template when creating a new issue.
- Include a clear title and description.
- Add steps to reproduce the issue and expected behavior.
- Include version information (Rust version, OS, etc.).

### Submitting Changes

1. **Fork the Repository**
   - Create your own fork of the repository.

2. **Create a Branch**
   - Create a branch for your feature or bugfix: `git checkout -b feature/your-feature-name`

3. **Make Your Changes**
   - Follow the coding style and guidelines.
   - Write tests for new features.
   - Keep commits focused and with clear messages.

4. **Run Tests**
   - Ensure all tests pass: `cargo test`
   - Run the linter: `cargo clippy`
   - Format your code: `cargo fmt`

5. **Submit a Pull Request**
   - Push your changes to your fork: `git push origin feature/your-feature-name`
   - Open a pull request against the `main` branch.
   - Describe your changes and reference any related issues.

## Development Guidelines

### Code Style

- Follow the Rust official style guide.
- Use `cargo fmt` before committing.
- Address all `clippy` warnings.

### Testing

- Write tests for new functionality.
- Ensure existing tests pass with your changes.
- Integration tests go in the `tests/` directory.
- Unit tests go within the module they're testing.

### Documentation

- Keep documentation up-to-date.
- Document all public APIs with doc comments.
- Include examples where appropriate.

### Commit Messages

- Use clear and meaningful commit messages.
- Start with a short summary line (50 chars or less).
- Optionally, follow with a blank line and a more detailed explanation.

## Release Process

1. Version numbers follow [Semantic Versioning](https://semver.org/).
2. Update CHANGELOG.md with notable changes.
3. Create a git tag for the new version.
4. Publish the crate using `cargo publish`.

## Getting Help

If you need help with contributing, feel free to:

- Open an issue with questions.
- Reach out to maintainers directly.

Thank you for contributing to ChemFST!
