# Audio Volume Control for NVDA

An NVDA add-on that allows you to control the audio volume of individual applications directly using keyboard shortcuts.

[GitHub Repository](https://github.com/JoaoDEVWHADS/nvda-audio-volume-control-application)

## Compatibility

| NVDA Version | Status |
|--------------|--------|
| 2025.3.2 | First tested version |
| 2019.3 - 2025.3 | Supported (manifest range) |

Users may modify `manifest.ini` to adjust compatibility range for other NVDA versions.

## Features

- List Active Applications: Shows all applications capable of producing audio.
- Separate Volume Control: Adjust volume per application without affecting system volume.
- Mute Toggle: Quickly mute or unmute specific applications.
- Reset Defaults: One-click button to reset all applications to 100% volume.
- Automatic Focus: Automatically selects the application you were using when opening the dialog.
- Automatic Updates: Checks for updates on NVDA startup and offers one-click installation.

## Installation

1. Download the latest `.nvda-addon` release.
2. Open NVDA.
3. Press `Enter` on the downloaded file or use "Manage add-ons" dialog.
4. Restart NVDA when prompted.

## Usage

1. Press `Ctrl + NVDA + Y` to open the Volume Control dialog.
2. Navigate the list with Up/Down arrows to select an application.
3. Press TAB to move to the Volume Slider. Use Left/Right arrows to adjust.
4. Press TAB to move to the Mute Checkbox. Press Space to toggle.
5. Press TAB to access the Reset Defaults button.
6. Press Esc or click Close to exit.

## Building from Source

### Prerequisites
- Python 3.10+
- SCons
- pip

### Build on Linux

```bash
chmod +x build_linux.sh
./build_linux.sh
```

This downloads Windows binaries for psutil and generates the `.nvda-addon` package.

## Technical Details

This add-on uses:
- `pycaw` (vendorized as `avc_pycaw`) for Windows Core Audio API
- `psutil` with Windows `.pyd` binary for process information
- NVDA's built-in `comtypes` for COM interface

## Bugs and Suggestions

For reports on bugs, errors, or feature suggestions, please contact us.

Contact: https://t.me/tierryt2021
