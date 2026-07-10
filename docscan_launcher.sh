#!/bin/bash
# Launcher script for docscan that sets up the environment for zbar library
#
# Usage: ./docscan_launcher.sh [options]
#   or just: ./docscan_launcher.sh
#
# This script sets DYLD_LIBRARY_PATH so that pyzbar can find the zbar library
# installed via Homebrew.

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set library path for zbar (Homebrew locations)
if [ -d "/opt/homebrew/lib" ]; then
    # Apple Silicon Mac (M1, M2, M3, M4)
    export DYLD_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_LIBRARY_PATH:-}"
    echo "✓ Using zbar from: /opt/homebrew/lib"
elif [ -d "/usr/local/lib" ]; then
    # Intel Mac
    export DYLD_LIBRARY_PATH="/usr/local/lib:${DYLD_LIBRARY_PATH:-}"
    echo "✓ Using zbar from: /usr/local/lib"
else
    echo "⚠ Warning: zbar library not found in Homebrew paths"
    echo "  Install with: brew install zbar"
    echo "  Barcode detection will not work without it."
    echo ""
fi

# Run the actual binary
exec "$SCRIPT_DIR/dist/docscan" "$@"
