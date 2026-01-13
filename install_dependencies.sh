#!/bin/bash
# Install dependencies script for NVDA Audio Volume Control Add-on
# This script bundles Python dependencies with the add-on

echo "Installing Python dependencies for NVDA Audio Volume Control Add-on..."
echo ""

# Create lib directory if it doesn't exist
mkdir -p addon/lib

# Install dependencies to addon/lib
echo "Installing pycaw, comtypes, and psutil to addon/lib..."
pip install -r requirements.txt --target addon/lib --upgrade

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Dependencies installed successfully!"
    echo ""
    echo "Dependencies are now bundled in: addon/lib/"
    echo ""
    echo "You can now build the add-on with: scons"
else
    echo ""
    echo "✗ Error installing dependencies!"
    echo ""
    echo "Please ensure pip is installed and try again."
    exit 1
fi
