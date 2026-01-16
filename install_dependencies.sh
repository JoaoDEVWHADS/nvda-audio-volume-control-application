#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ADDON_DIR=$(find . -type d -name "globalPlugins" -print -quit 2>/dev/null)
if [ -z "$ADDON_DIR" ]; then
    echo "Error: globalPlugins directory not found"
    exit 1
fi

PLUGIN_DIR=$(find "$ADDON_DIR" -mindepth 1 -maxdepth 1 -type d -print -quit)
if [ -z "$PLUGIN_DIR" ]; then
    echo "Error: Plugin directory not found"
    exit 1
fi

LIB_DIR="$PLUGIN_DIR/lib"
mkdir -p "$LIB_DIR"

echo "Target: $LIB_DIR"

TMP_DIR=$(mktemp -d)

echo "Downloading psutil for Windows..."
pip3 download psutil --platform win32 --python-version 311 --only-binary=:all: -d "$TMP_DIR" --quiet
PSUTIL_WHL=$(find "$TMP_DIR" -name "psutil*.whl" -print -quit)
if [ -n "$PSUTIL_WHL" ]; then
    rm -rf "$LIB_DIR/psutil"
    unzip -q "$PSUTIL_WHL" -d "$TMP_DIR/ext"
    mv "$TMP_DIR/ext/psutil" "$LIB_DIR/psutil"
    echo "psutil OK"
fi

echo "Installing pycaw..."
pip3 install pycaw -t "$TMP_DIR/pycaw_tmp" --quiet --no-compile
if [ -d "$TMP_DIR/pycaw_tmp/pycaw" ]; then
    rm -rf "$LIB_DIR/avc_pycaw"
    mv "$TMP_DIR/pycaw_tmp/pycaw" "$LIB_DIR/avc_pycaw"
    find "$LIB_DIR/avc_pycaw" -name "*.py" -exec sed -i 's/from pycaw\./from avc_pycaw./g; s/import pycaw/import avc_pycaw/g' {} \;
    echo "pycaw vendorized as avc_pycaw OK"
fi

rm -rf "$TMP_DIR"

find "$LIB_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$LIB_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$LIB_DIR" -type d -name "*dist-info" -exec rm -rf {} + 2>/dev/null || true

echo "Dependencies installed to $LIB_DIR"
ls -la "$LIB_DIR"
