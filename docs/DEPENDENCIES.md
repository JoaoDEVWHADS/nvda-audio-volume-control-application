# Dependencies

This add-on uses external Python libraries to interact with Windows Audio APIs.

## Bundled Libraries

### avc_pycaw (vendorized)
- Original: [pycaw](https://github.com/AndreMiras/pycaw)
- Purpose: Windows Core Audio API (WASAPI) interface
- Renamed to `avc_pycaw` to avoid conflicts with NVDA's internal libraries
- Location: `addon/globalPlugins/audioVolumeControl/lib/avc_pycaw/`

### psutil
- Original: [psutil](https://github.com/giampaolo/psutil)
- Purpose: Process information (get application names from PIDs)
- Includes Windows binary `_psutil_windows.pyd`
- Location: `addon/globalPlugins/audioVolumeControl/lib/psutil/`

### comtypes
- Uses NVDA's built-in comtypes (not bundled)
- Purpose: COM interface for Windows APIs

## Why Vendorize?

NVDA includes its own versions of some libraries. Loading duplicate libraries causes conflicts like:
- `TypeError: expected LP_GUID instance instead of pointer to GUID`
- Import errors when module names clash

By renaming `pycaw` to `avc_pycaw`, we ensure our code uses our bundled version without conflicts.

## Building Dependencies

Run `build_linux.sh` to automatically:
1. Download psutil with Windows 32-bit binary
2. Install pycaw and rename to avc_pycaw
3. Update internal imports
4. Build the .nvda-addon package

```bash
chmod +x build_linux.sh
./build_linux.sh
```

## Cross-Platform Build

To download Windows binaries from Linux:
```bash
pip3 download psutil --platform win32 --python-version 311 --only-binary=:all: -d /tmp
```

This downloads the `.whl` file containing `_psutil_windows.pyd` for Windows 32-bit.
