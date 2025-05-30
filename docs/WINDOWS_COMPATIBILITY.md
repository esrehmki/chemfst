# Windows Compatibility Guide

## Overview

ChemFST is fully compatible with Windows environments, including GitHub Actions runners. This document outlines the Windows-specific considerations and implementations.

## GitHub Actions Windows Support

### Matrix Strategy
The Python CI workflow includes `windows-latest` in the test matrix:
```yaml
matrix:
  os: [ubuntu-latest, macos-latest, windows-latest]
  python-version: ["3.11", "3.12", "3.13"]
```

### Platform-Specific Implementations

#### Cache Paths
**Unix/Linux/macOS:**
```yaml
path: |
  ~/.cargo/registry
  ~/.cargo/git
  target/
  chemfst-py/target/
```

**Windows:**
```yaml
path: |
  C:\Users\runneradmin\.cargo\registry
  C:\Users\runneradmin\.cargo\git
  target\
  chemfst-py\target\
```

#### File Verification Commands
**Unix (Bash):**
```bash
if [ ! -f "data/chemical_names.txt" ]; then
  echo "Error: data/chemical_names.txt not found"
  exit 1
fi
echo "✅ Found existing data/chemical_names.txt"
head -5 data/chemical_names.txt
echo "... ($(wc -l < data/chemical_names.txt) total lines)"
```

**Windows (PowerShell):**
```powershell
if (!(Test-Path "data\chemical_names.txt")) {
  Write-Host "Error: data\chemical_names.txt not found"
  exit 1
}
Write-Host "✅ Found existing data\chemical_names.txt"
Get-Content "data\chemical_names.txt" -Head 5
$lineCount = (Get-Content "data\chemical_names.txt" | Measure-Object -Line).Lines
Write-Host "... ($lineCount total lines)"
```

## Local Windows Development

### Prerequisites
1. **Rust Toolchain**: Install via [rustup.rs](https://rustup.rs/)
2. **Python 3.11+**: Install from [python.org](https://python.org)
3. **Git**: Install from [git-scm.com](https://git-scm.com/)
4. **Visual Studio Build Tools**: Required for Rust compilation

### Setup Commands
```cmd
# Clone repository
git clone <repository-url>
cd ChemFST

# Install Python dependencies
python -m pip install --upgrade pip maturin pytest

# Build Python package
maturin develop --manifest-path chemfst-py/Cargo.toml

# Run tests
python -m pytest python/tests/ -v

# Run examples
python python/examples/demo.py
```

### PowerShell Setup
```powershell
# Alternative setup using PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip maturin pytest
```

## Path Handling

### File Separators
- **Windows**: Uses backslash `\` as path separator
- **Cross-platform**: Python's `pathlib.Path` handles this automatically
- **Workflow**: Uses forward slashes `/` in cross-platform commands

### Example Implementation
```python
from pathlib import Path

# Works on all platforms
data_file = Path("data") / "chemical_names.txt"
fst_file = Path("data") / "chemical_names.fst"

# Platform-specific string representation
if platform.system() == "Windows":
    print(f"Windows path: {data_file}")  # data\chemical_names.txt
else:
    print(f"Unix path: {data_file}")     # data/chemical_names.txt
```

## Build Considerations

### Rust Compilation
- **MSVC**: Primary toolchain for Windows builds
- **GNU**: Alternative toolchain (less common)
- **Dependencies**: May require Visual Studio Build Tools

### Python Extension Modules
- **ABI**: Windows uses different ABI than Unix systems
- **File Extensions**: `.pyd` files on Windows vs `.so` on Unix
- **Maturin**: Handles cross-platform building automatically

## Testing on Windows

### Local Validation
```cmd
# Run the validation script
python scripts/validate_workflow.py
```

Expected output on Windows:
```
Operating System: Windows 10
✅ Windows PowerShell commands tested successfully
✅ Workflow should work on windows-latest
```

### GitHub Actions Testing
The workflow automatically tests on `windows-latest` with:
- Windows Server 2022
- PowerShell 5.1 and PowerShell Core
- MSVC build tools
- Python 3.11, 3.12, and 3.13

## Common Windows Issues

### Build Failures
**Issue**: Missing Visual Studio Build Tools
```
error: Microsoft Visual C++ 14.0 is required
```
**Solution**: Install Visual Studio Build Tools or Visual Studio Community

### Path Issues
**Issue**: Path separator conflicts
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/chemical_names.txt'
```
**Solution**: Use `pathlib.Path` for cross-platform compatibility

### PowerShell Execution Policy
**Issue**: Script execution disabled
```
execution of scripts is disabled on this system
```
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Long Path Support
**Issue**: Path length limitations (260 characters)
**Solution**: Enable long path support in Windows 10/11:
```
Computer Configuration > Administrative Templates > System > Filesystem > Enable Win32 long paths
```

## Performance Considerations

### File System Performance
- **NTFS**: Good performance for FST file operations
- **Windows Defender**: May impact build times (consider exclusions)
- **Antivirus**: Can slow down file operations

### Memory Mapping
- **Windows**: Full support for memory-mapped files
- **Performance**: Comparable to Unix systems for FST operations
- **Large Files**: Windows handles large FST files efficiently

## Best Practices

### Development Environment
1. Use Windows Subsystem for Linux (WSL) for Unix-like experience
2. Consider PowerShell Core for better cross-platform scripting
3. Use Windows Terminal for improved command-line experience

### CI/CD Integration
1. Test locally on Windows before pushing
2. Monitor Windows-specific build times
3. Use platform-specific caching strategies
4. Handle path separators consistently

### Deployment
1. Test Windows packages thoroughly
2. Consider Windows-specific packaging requirements
3. Document Windows-specific installation steps
4. Provide PowerShell scripts for automation

## Troubleshooting

### Debug Commands
```powershell
# Check Python installation
python --version
where python

# Check Rust installation
rustc --version
cargo --version

# Check file exists
Test-Path "data\chemical_names.txt"

# Show file content
Get-Content "data\chemical_names.txt" -Head 10

# Check build tools
where cl.exe
```

### Log Analysis
- GitHub Actions logs are available for 30 days
- Windows logs may include additional system information
- PowerShell errors include detailed stack traces

## Future Enhancements

### Planned Improvements
- Windows-specific performance optimizations
- Native Windows installer packages
- PowerShell module for ChemFST
- Windows-specific documentation

### Compatibility Targets
- Windows 10 (version 1903+)
- Windows 11
- Windows Server 2019+
- Windows Server 2022
