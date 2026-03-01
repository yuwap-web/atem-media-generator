#!/bin/bash
# Build macOS .app bundle for ATEM Media File Generator
# Creates a proper macOS application bundle with all dependencies

set -e  # Exit on error

echo "========================================="
echo "ATEM Media File Generator - macOS Build"
echo "========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found."
    echo "Run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check PyInstaller is installed
echo "Checking PyInstaller..."
if ! python -m pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
else
    PYINSTALLER_VERSION=$(python -m pip show pyinstaller | grep Version | awk '{print $2}')
    echo "✓ PyInstaller version: $PYINSTALLER_VERSION"
fi

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build/ dist/ *.spec
echo "✓ Clean complete"

# Build .app bundle
echo ""
echo "Building macOS .app bundle..."
python -m PyInstaller \
    --name "ATEM Media Generator" \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtPrintSupport \
    --hidden-import=PyQt5.QtSvg \
    --hidden-import=PIL \
    --hidden-import=PIL.ImageTk \
    --collect-data=PIL \
    --collect-all=dotenv \
    --add-data "templates:templates" \
    --windowed \
    --osx-bundle-identifier="com.atem.media-generator" \
    main.py

# Remove redundant --onedir output (keep only .app bundle)
if [ -d "dist/ATEM Media Generator" ] && [ -d "dist/ATEM Media Generator.app" ]; then
    echo ""
    echo "Cleaning redundant build output..."
    rm -rf "dist/ATEM Media Generator"
    echo "✓ Removed redundant directory"
fi

echo ""
echo "========================================="
echo "✅ macOS .app Bundle Build Complete!"
echo "========================================="
echo ""
echo "Application location:"
echo "  dist/ATEM Media Generator.app"
echo ""
echo "To run the application:"
echo "  open dist/ATEM\\ Media\\ Generator.app"
echo ""
echo "To create a distributable .dmg:"
echo "  bash create-dmg-bundle.sh"
echo ""
echo "To create a .zip archive for GitHub Release:"
echo "  ditto -c -k --sequesterRsrc dist/ATEM\\ Media\\ Generator.app atem-mac.zip"
echo ""
echo "Application size:"
ls -lh dist/ATEM\ Media\ Generator.app/Contents/MacOS/ATEM\ Media\ Generator 2>/dev/null | awk '{print "  Binary: " $5}' || echo "  Building..."
echo "========================================="
