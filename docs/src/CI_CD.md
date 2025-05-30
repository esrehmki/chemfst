# CI/CD Documentation for ChemFST

## Overview

ChemFST uses GitHub Actions for continuous integration and deployment, ensuring code quality and compatibility across multiple platforms and Python versions.

## Workflow Architecture

### 1. Rust CI Workflow (`rust.yml`)

**Triggers**: Push to `trunk`, Pull Requests to `trunk`

**Matrix Strategy**:
- **Operating Systems**: Ubuntu, macOS, Windows
- **Rust Versions**: stable, beta

**Jobs**:
- **Build & Test**: Compiles and tests Rust code
- **Linting**: Runs clippy for code quality
- **Formatting**: Checks code formatting with rustfmt
- **Coverage**: Generates code coverage reports using tarpaulin

### 2. Python CI Workflow (`python.yml`)

**Triggers**: Push to `trunk`, Pull Requests to `trunk`

**Matrix Strategy**:
- **Operating Systems**: Ubuntu, macOS, Windows
- **Python Versions**: 3.11, 3.12, 3.13

**Jobs**:
- **Test**: Builds Python bindings and runs pytest
- **Coverage**: Generates Python code coverage

## Workflow Details

### Python Workflow Steps

1. **Environment Setup**
   - Checkout code
   - Install Python and Rust toolchains
   - Cache Rust dependencies for faster builds

2. **Dependency Installation**
   - Install maturin for Python-Rust bindings
   - Install pytest for testing

3. **Test Data Verification**
   - Verify `data/chemical_names.txt` exists in repository
   - Use existing chemical names from the tracked file

4. **Package Building**
   - Use maturin to build Python bindings from Rust code (wheel format)
   - Install built wheel with pip (avoids virtual environment requirement)

5. **Testing**
   - Run pytest suite with verbose output
   - Execute example scripts to validate functionality

6. **Coverage** (Ubuntu only)
   - Generate coverage reports
   - Upload to Codecov

### Key Features

#### Cross-Platform Compatibility
- Tests run on Linux, macOS, and Windows
- Platform-specific commands for file creation
- Handles path differences across operating systems

#### FST File Handling
- Uses existing `data/chemical_names.txt` from repository
- FST files are generated during CI, not stored in repository
- Consistent test data from the tracked source file

#### Caching Strategy
- Rust dependencies cached by Cargo.lock hash
- Reduces build times for subsequent runs
- Platform-specific cache keys

## Test Data Source

The workflows use the chemical names from the tracked `data/chemical_names.txt` file in the repository. This ensures:

- **Consistency**: All platforms use identical test data
- **Single Source of Truth**: Chemical names are maintained in one location
- **Easy Updates**: Modify the file to change test data across all workflows
- **Version Control**: Test data changes are tracked in git history

The file contains a curated list of chemical compounds used for testing all functionality including prefix search, substring search, and performance benchmarks.

## Local Development

### Pre-commit Validation

Use the validation script before pushing changes:

```bash
python scripts/validate_workflow.py
```

This script replicates the CI environment locally:
- Creates test data
- Builds the package
- Runs tests
- Validates examples

### Manual Testing

```bash
# Test Rust components
cargo test

# Build and install Python package
maturin build --manifest-path chemfst-py/Cargo.toml --out dist
pip install dist/*.whl

# Test Python components
pytest python/tests/ -v

# Test examples
python python/examples/demo.py
```

## Coverage Reporting

### Rust Coverage
- Uses `cargo-tarpaulin` for coverage analysis
- Generates XML reports for Codecov
- Runs only on Ubuntu for efficiency

### Python Coverage
- Uses `pytest-cov` for coverage analysis
- Covers Python bindings and test code
- Uploads to Codecov with platform identification

## Troubleshooting

### Common Issues

#### FST File Errors
- **Cause**: Missing or invalid test data
- **Solution**: Verify `data/chemical_names.txt` exists in repository and has content

#### Build Failures
- **Cause**: Rust toolchain issues or maturin virtual environment errors
- **Solution**: Check Rust installation and dependencies, use `maturin build` + `pip install` instead of `maturin develop`

#### Test Failures
- **Cause**: Platform-specific path or command issues
- **Solution**: Review platform-specific workflow steps

### Debugging Strategies

1. **Check Workflow Logs**: Review detailed logs in GitHub Actions
2. **Local Reproduction**: Use validation script to reproduce issues
3. **Platform Testing**: Test on specific platforms if issues are OS-specific
4. **Dependency Versions**: Verify Python and Rust version compatibility

## Security Considerations

### Secrets Management
- `CODECOV_TOKEN`: Used for coverage uploads
- Stored as GitHub repository secrets
- Access controlled through GitHub permissions

### Dependency Security
- Automated dependency updates through Dependabot
- Regular security audits of Rust and Python dependencies
- Pinned action versions for reproducibility

## Maintenance

### Updating Dependencies
- Monitor for new Python versions and add to matrix
- Update Rust toolchain versions as needed
- Keep GitHub Actions up to date

### Performance Optimization
- Monitor build times and optimize caching
- Consider parallel job execution
- Profile test execution times

## Future Enhancements

### Planned Improvements
- Add Windows-specific testing for path handling
- Implement benchmark regression testing
- Add documentation generation and deployment
- Consider adding nightly Rust builds for early issue detection

### Monitoring
- Track build success rates across platforms
- Monitor test execution times
- Coverage trend analysis
