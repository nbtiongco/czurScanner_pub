# CZUR Document Scanner - Installation Instructions

## Requirements

**System Requirements:**
- macOS (Apple Silicon or Intel)
- USB camera or built-in webcam
- Homebrew package manager

**Required Software:**
- zbar library for barcode detection

## Installation Steps

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install zbar library

```bash
brew install zbar
```

### 3. Make the binary executable

```bash
chmod +x docscan
chmod +x docscan_launcher.sh
```

### 4. Run the application

**Option 1: Use the launcher script (Recommended)**
```bash
./docscan_launcher.sh
```

**Option 2: Run directly with environment variable**
```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib ./docscan
```

**Option 3: Specify output directory**
```bash
./docscan_launcher.sh --output_dir ~/Documents/scans
```

## Controls

- **SPACE**: Capture image
- **R**: Rotate preview & capture
- **B**: Change basename (manual entry)
- **D**: Change output directory (Finder dialog)
- **T**: New Tape (resets file numbering)
- **Q / ESC**: Quit

## Workflow

1. **First Capture**: Place barcode under camera and press SPACE
   - Scanner will automatically detect barcode and use it as filename
   - If detection fails, you'll be prompted to enter manually
   - Press ESC to cancel and retry detection

2. **Confirmation**: Before saving, confirm filename
   - SPACE = Save
   - B = Rename
   - ESC = Cancel and retry barcode detection

3. **Subsequent Captures**: Files are numbered automatically
   - Example: `OOA201L8_001.jpg`, `OOA201L8_002.jpg`, etc.

4. **New Tape**: Press T to start a new tape session
   - Resets file numbering to 001
   - Next capture will detect new barcode

5. **Change Directory**: Press D to change output folder
   - Opens Finder dialog to select directory

## Troubleshooting

### Barcode Detection Not Working

**Problem**: "pyzbar not available" error or no barcode detected

**Solution**: Make sure you installed zbar:
```bash
brew install zbar
```

Then run using the launcher script:
```bash
./docscan_launcher.sh
```

### Camera Not Found

**Problem**: Camera access error or black screen

**Solution**:
1. Grant camera permissions to Terminal in System Preferences > Privacy & Security > Camera
2. Make sure no other application is using the camera

### Binary Won't Run

**Problem**: "cannot be opened because the developer cannot be verified"

**Solution**:
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine docscan

# Or allow in System Preferences > Privacy & Security
```

## Support

For issues or questions, see the full README.md or create an issue at:
https://github.com/anthropics/claude-code/issues
