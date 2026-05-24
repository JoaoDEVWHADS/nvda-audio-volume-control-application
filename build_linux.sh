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
    echo "Error: Plugin directory not found inside globalPlugins"
    exit 1
fi

LIB_DIR="$PLUGIN_DIR/lib"
mkdir -p "$LIB_DIR"

echo "Installing dependencies to $LIB_DIR..."

rm -rf "$LIB_DIR/psutil" "$LIB_DIR/avc_pycaw" "$LIB_DIR/pycaw"

TMP_DIR=$(mktemp -d)
mkdir -p "$LIB_DIR/psutil"

echo "Downloading psutil wheels..."
for pyver in 37 38 39 310 311 312 313; do
    if [ "$pyver" = "37" ]; then
        abi="cp37m"
    else
        abi="cp$pyver"
    fi
    pip3 download psutil --platform win32 --python-version "$pyver" --abi "$abi" --only-binary=:all: --implementation cp -d "$TMP_DIR" --quiet || true
done
for pyver in 311 312 313; do
    pip3 download psutil --platform win_amd64 --python-version "$pyver" --abi "cp$pyver" --only-binary=:all: --implementation cp -d "$TMP_DIR" --quiet || true
done

ANY_WHL=$(find "$TMP_DIR" -name "psutil*.whl" -print -quit)
if [ -n "$ANY_WHL" ]; then
    unzip -q "$ANY_WHL" -d "$TMP_DIR/psutil_extracted"
    cp -r "$TMP_DIR/psutil_extracted/psutil/"* "$LIB_DIR/psutil/"
    rm -f "$LIB_DIR/psutil/"*.pyd
    echo "psutil pure Python files copied"
fi

for whl in "$TMP_DIR"/psutil*.whl; do
    if [ -f "$whl" ]; then
        WHL_NAME=$(basename "$whl" .whl)
        IFS='-' read -ra PARTS <<< "$WHL_NAME"
        LEN=${#PARTS[@]}
        PY_TAG="${PARTS[$((LEN-3))]}"
        PLAT_TAG="${PARTS[$((LEN-1))]}"
        
        EXT_DIR="$TMP_DIR/extract_${WHL_NAME}"
        mkdir -p "$EXT_DIR"
        unzip -q "$whl" -d "$EXT_DIR"
        
        for pyd in "$EXT_DIR/psutil/"*.pyd; do
            if [ -f "$pyd" ]; then
                TARGET_NAME="_psutil_windows.${PY_TAG}-${PLAT_TAG}.pyd"
                cp "$pyd" "$LIB_DIR/psutil/$TARGET_NAME"
                echo "  ✓ Extracted and renamed to $TARGET_NAME"
            fi
        done
    fi
done

pip3 install pycaw -t "$TMP_DIR/pycaw_tmp" --quiet --no-compile
if [ -d "$TMP_DIR/pycaw_tmp/pycaw" ]; then
    mv "$TMP_DIR/pycaw_tmp/pycaw" "$LIB_DIR/avc_pycaw"
    find "$LIB_DIR/avc_pycaw" -name "*.py" -exec sed -i 's/from pycaw\./from avc_pycaw./g; s/import pycaw/import avc_pycaw/g' {} \;
    find "$LIB_DIR/avc_pycaw" -name "*.py" -exec sed -i 's/import comtypes/import comtypes/g' {} \;
    echo "pycaw vendorized as avc_pycaw"
fi

rm -rf "$TMP_DIR"

find "$LIB_DIR" -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find "$LIB_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$LIB_DIR" -name "*.pyc" -delete 2>/dev/null || true

rm -f ./*.nvda-addon
scons -c
scons

echo "Build complete!"
ls -la ./*.nvda-addon 2>/dev/null || echo "No addon file found"
