# Building the Standalone Binary

This project uses PyInstaller to create a standalone executable for the CZUR document scanner application.

## Prerequisites

- Python 3.9 or 3.10
- uv package manager (or pip)

## Building the Binary

1. Install PyInstaller (if not already installed):
   ```bash
   uv pip install pyinstaller
   ```

2. Build the standalone binary:
   ```bash
   .venv/bin/pyinstaller docscan.spec --clean
   ```

3. The binary will be created in the `dist/` directory:
   ```
   dist/docscan
   ```

## Using the Binary

The standalone binary can be run without any Python installation:

```bash
./dist/docscan --help
```

### Basic Usage

```bash
# Run with default settings (auto-detect CZUR camera)
./dist/docscan

# Specify output directory and filename
./dist/docscan --filename my_scan --output_dir ./scans

# Specify camera index manually
./dist/docscan --camera_index 0 --auto_detect false
```

### Controls

- **SPACE**: Capture image
- **U**: Toggle detection tracking
- **R**: Rotate preview and capture
- **B**: Change basename
- **Q/ESC**: Quit

## Distribution

The `docscan` binary is self-contained and can be distributed to other macOS systems without requiring Python or any dependencies to be installed. The binary is approximately 42MB in size.

## Notes

- The binary is built for the current platform (macOS ARM64 in this case)
- For other platforms, you'll need to rebuild on that platform
- The spec file ([docscan.spec](docscan.spec)) contains all build configuration