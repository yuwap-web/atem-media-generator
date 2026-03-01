#!/bin/bash
# Build macOS executable for ATEM Media File Generator
# Uses PyInstaller with selective hidden imports (avoids Qt symlink issues)

set -e  # Exit on error

echo "========================================="
echo "ATEM Media File Generator - macOS Build"
echo "========================================="

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check PyInstaller is installed
if ! python -m pip show pyinstaller > /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Clean previous build
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build executable
echo "Building executable..."
python -m PyInstaller \
    --onedir \
    --name "cpt_editor" \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PIL \
    --collect-data=PIL \
    --windowed \
    --icon=icon.icns 2>/dev/null || true \
    main.py

echo ""
echo "========================================="
echo "Build complete!"
echo "========================================="
echo ""
echo "Executable location: dist/cpt_editor"
echo ""
echo "To run:"
echo "  ./dist/cpt_editor"
echo ""
echo "To create a distributable package:"
echo "  zip -r cpt_editor-mac.zip dist/cpt_editor"
echo "========================================="
