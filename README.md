# CZUR Scanner Tool

Document scanning application with automatic edge detection.

## Application

### Document Scanner (`docscan`)
Real-time document detection and capture with automatic edge detection.

- **Features:**
  - Auto-detect documents with edge detection
  - Automatic cropping and rotation
  - Live preview with confidence tracking
  - Barcode detection on first capture (auto-naming)
  - Multi-tape session management

- **Controls:**
  - SPACE: Capture image
  - U: Toggle tracking
  - R: Rotate preview
  - B: Change basename
  - T: New tape (increment tape number)
  - Q/ESC: Quit

- **Documentation:** See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

```bash
./dist/docscan --help
./dist/docscan --filename my_scan --output_dir ./scans
```

## Quick Start

**💡 REQUIRED:** For barcode detection, install zbar: `brew install zbar`

### Using Pre-built Binary

```bash
# Option 1: Use launcher (recommended - sets up zbar paths automatically)
./docscan_launcher.sh

# Option 2: Run binary directly with environment variable
DYLD_LIBRARY_PATH=/opt/homebrew/lib ./dist/docscan
```

**Note:** Barcode detection requires the zbar library. Install it with `brew install zbar`.

### Building from Source

```bash
# Install dependencies
uv sync

# Build document scanner
.venv/bin/pyinstaller docscan.spec --clean

# Binary will be in: dist/
```

## Requirements

- **macOS:** Apple Silicon (M1, M2, M3, M4) - ARM64
- **Camera:** USB camera or built-in webcam
- **Permissions:** Camera access must be granted to Terminal

## Documentation

- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Building binaries for macOS
- [BUILD_LINUX_EL8.md](BUILD_LINUX_EL8.md) - Building for Linux EL8
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## Platform Support

| Platform | Architecture | Status |
|----------|-------------|--------|
| macOS (Apple Silicon) | ARM64 | ✅ Supported |
| macOS (Intel) | x86_64 | ⚠️ Build on Intel Mac |
| Linux EL8 | x86_64 | ⚠️ Build on EL8 system |
| Windows | x86_64 | ⚠️ Build on Windows |

## Project Structure

```
czur_scanner/
├── src/
│   └── document_scanner/      # Document scanner app
│       ├── main.py
│       ├── scanner.py
│       └── utils.py
├── dist/                      # Built binaries
│   └── docscan               # Document scanner (51MB)
├── docscan.spec              # PyInstaller config
└── pyproject.toml            # Python project config
```

## Dependencies

- Python 3.9 or 3.10
- OpenCV 4.8+
- NumPy 1.26+
- Fire (CLI framework)
- pyzbar (barcode detection)
- zbar library (system requirement - install with `brew install zbar`)

## Installation Notes

### Barcode Detection

The scanner uses **pyzbar/zbar** for barcode detection:

```bash
# Install zbar library (required for barcode detection)
brew install zbar
```

**To run with zbar support:**
```bash
# Use launcher script (automatically sets up zbar paths)
./docscan_launcher.sh

# Or set environment variable manually
DYLD_LIBRARY_PATH=/opt/homebrew/lib ./dist/docscan
```

## Usage Examples

### Basic Usage
```bash
# Start scanning with default settings
./docscan_launcher.sh

# Specify custom output directory
./docscan_launcher.sh --output_dir ./scans

# Alternative: Set library path manually
DYLD_LIBRARY_PATH=/opt/homebrew/lib ./dist/docscan --output_dir ./scans
```

### Workflow with Barcode Auto-naming
1. Start the scanner
2. Place a document with a barcode under the camera
3. Press SPACE to capture - the barcode will be detected and used as the basename
4. Continue scanning - files will be numbered sequentially (e.g., `OOA201L8_001.jpg`, `OOA201L8_002.jpg`)
5. Press T to start a new tape - increments tape number and resets file counter
6. Next files will be named like `OOA201L8_tape2_001.jpg`, `OOA201L8_tape2_002.jpg`

### Multi-Tape Workflow
- Each tape starts at file index 001
- Tape 1: `basename_001.jpg`, `basename_002.jpg`
- Press T for new tape
- Tape 2: `basename_tape2_001.jpg`, `basename_tape2_002.jpg`
- Press T again
- Tape 3: `basename_tape3_001.jpg`, `basename_tape3_002.jpg`

## TODO / Future Features
- Tracking Disabled atm
- Directory output change