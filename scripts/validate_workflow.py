#!/usr/bin/env python3
"""
Workflow validation script for ChemFST Python CI.

This script validates that the GitHub workflow will work correctly by:
1. Creating test data files
2. Building the Python package
3. Running tests
4. Testing examples

Run this script locally to validate the workflow before pushing changes.
"""

import os
import sys
import subprocess
import tempfile
import platform
from pathlib import Path


def read_chemical_names(file_path):
    """Read chemical names from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"[WARN] Error reading {file_path}: {e}")
        return []


def run_command(cmd, description, cwd=None, shell_type="auto"):
    """Run a command and handle errors."""
    print(f"[RUN] {description}...")
    try:
        if shell_type == "powershell" and platform.system() == "Windows":
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                check=True, capture_output=True, text=True, cwd=cwd
            )
        else:
            result = subprocess.run(
                cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd
            )
        print(f"[OK] {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {description} - Failed")
        print(f"Command: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def create_test_data(data_dir, source_file=None):
    """Create test chemical names data file from existing source."""
    data_dir.mkdir(parents=True, exist_ok=True)
    test_file = data_dir / "chemical_names.txt"

    if source_file and source_file.exists():
        # Copy from existing source file
        import shutil
        shutil.copy2(source_file, test_file)
        print(f"[OK] Copied test data from {source_file} to: {test_file}")
    else:
      raise FileNotFoundError


    return test_file


def main():
    """Main validation function."""
    print("ChemFST Python Workflow Validation")
    print("===================================\n")

    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print(f"Project root: {project_root}")
    print(f"Python version: {sys.version}")
    print(f"Operating System: {platform.system()} {platform.release()}")

    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("[OK] Running in virtual environment")
    else:
        print("[WARN] Not running in virtual environment - this is recommended")

    # Ensure test data exists
    project_data = project_root / "data"
    project_data.mkdir(exist_ok=True)
    project_test_file = project_data / "chemical_names.txt"

    if not project_test_file.exists():
        # Create test data if it doesn't exist
        create_test_data(project_data)
        print(f"[OK] Created test data: {project_test_file}")
    else:
        print(f"[OK] Using existing test data: {project_test_file}")
        # Verify file has content and show info
        chemical_names = read_chemical_names(project_test_file)
        if not chemical_names:
            print("[WARN] Test data file is empty or unreadable, creating fallback data")
            create_test_data(project_data)
        else:
            print(f"   [INFO] Found {len(chemical_names)} chemical names")
            print(f"   [INFO] Sample: {', '.join(chemical_names[:3])}{'...' if len(chemical_names) > 3 else ''}")

    # Step 1: Install dependencies
    run_command(
        "python -m pip install --upgrade pip maturin pytest",
        "Installing Python dependencies"
    )

    # Step 2: Build Python package (using build + pip install like GitHub Actions)
    run_command(
        "maturin build --manifest-path chemfst-py/Cargo.toml --out dist",
        "Building Python package with maturin"
    )

    # Step 2b: Install the built wheel
    run_command(
        "python -m pip install dist/*.whl",
        "Installing built Python package"
    )

    # Step 3: Run tests
    run_command(
        "python -m pytest python/tests/ -v --tb=short",
        "Running Python tests"
    )

    # Step 4: Test file verification commands (Windows compatibility)
    if platform.system() == "Windows":
        print("\n[RUN] Testing Windows-specific commands...")
        powershell_cmd = '''
if (!(Test-Path "data\\chemical_names.txt")) {
    Write-Host "Error: data\\chemical_names.txt not found"
    exit 1
}
Write-Host "[OK] Found existing data\\chemical_names.txt"
Write-Host "File contents:"
Get-Content "data\\chemical_names.txt" -Head 5
$lineCount = (Get-Content "data\\chemical_names.txt" | Measure-Object -Line).Lines
Write-Host "... ($lineCount total lines)"
'''
        try:
            result = run_command(
                powershell_cmd,
                "Testing Windows PowerShell file verification",
                shell_type="powershell"
            )
            print("[OK] Windows PowerShell commands work correctly")
        except Exception as e:
            print(f"[WARN] PowerShell test failed: {e}")
            print("This may indicate issues with Windows workflow execution")
    else:
        print("[OK] Unix/Linux/macOS - using bash commands in workflow")

    # Step 5: Test examples
    run_command(
        "python python/examples/demo.py",
        "Testing Python examples",
    )

    # Step 6: Check import
    try:
        import chemfst
        print("[OK] ChemFST module imported successfully")
        print(f"   [INFO] Available attributes: {[attr for attr in dir(chemfst) if not attr.startswith('_')]}")
    except ImportError as e:
        print(f"[FAIL] Failed to import chemfst: {e}")
        sys.exit(1)

    # Step 7: Validate test data content
    project_test_file = project_root / "data" / "chemical_names.txt"
    chemical_names = read_chemical_names(project_test_file)
    print(f"\n[INFO] Test Data Summary:")
    print(f"   Total chemical names: {len(chemical_names)}")
    print(f"   First few entries: {', '.join(chemical_names[:5])}")
    print(f"   Data source: {project_test_file}")

    print(f"\n[INFO] Platform Compatibility:")
    print(f"   Current OS: {platform.system()}")
    if platform.system() == "Windows":
        print("   [OK] Windows PowerShell commands tested successfully")
        print("   [OK] Workflow should work on windows-latest")
    else:
        print("   [OK] Unix/bash commands will work on ubuntu-latest and macos-latest")
        print("   [OK] Windows compatibility handled by separate PowerShell steps")

    print("\n[OK] All validation checks passed!")
    print("\nThe GitHub workflow should work correctly with this configuration.")
    print("\nNext steps:")
    print("- Push changes to trigger the GitHub workflow")
    print("- Monitor the workflow results in GitHub Actions")
    print("- Address any platform-specific issues that arise")
    print(f"- The workflow will use the {len(chemical_names)} chemical names from data/chemical_names.txt")
    print("- Windows, macOS, and Linux platforms are all supported")


if __name__ == "__main__":
    main()
