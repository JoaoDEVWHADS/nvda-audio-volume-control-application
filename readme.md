# Audio Volume Control for NVDA

An NVDA add-on that allows you to control the audio volume of individual applications directly using keyboard shortcuts.

[GitHub Repository](https://github.com/JoaoDEVWHADS/nvda-audio-volume-control-application)

## 🚀 Features

- **List Active Applications:** Shows a list of all applications capable of producing audio.
- **Separate Volume Control:** Adjust volume per application without affecting the global system volume.
- **Mute Toggle:** Quickly mute or unmute specific applications.
- **Reset Defaults:** One-click button to reset all applications to 100% volume and unmute them.
- **Automatic Focus:** Automatically selects the application you were using when opening the dialog.
- **Accessible UI:** 
  - Standard List view for navigation.
  - Tab navigation between List, Volume Slider, and Mute Checkbox.
  - Screen reader friendly announcements.

## 📦 Installation

1. Download the latest `.nvda-addon` release.
2. Open NVDA.
3. Press `Enter` on the downloaded file or use the "Manage add-ons" dialog to install.
4. Restart NVDA when prompted.

## 🎮 Usage

1. Press `Ctrl + NVDA + Y` to open the Volume Control dialog.
2. **Navigate the list** with Up/Down arrows to select an application.
3. Press **TAB** to move to the **Volume Slider**.
   - Use Left/Right arrows to adjust volume.
4. Press **TAB** again to move to the **Mute Checkbox**.
   - Press Space to toggle mute.
5. Press **TAB** to access the **Reset Defaults** button.
   - Press Enter/Space to reset all application volumes to 100% and unmute them.
6. Press **Esc** or click Close to exit.

## 🛠️ Building from Source

### Prerequisites
- Python 3.10+
- SCons
- Gettext (for translations)

### Build on Linux (Recommended)
This project includes a unified build script that handles dependencies (pycaw, psutil, comtypes) and cross-platform compatibility.

```bash
chmod +x build_linux.sh
./build_linux.sh
```

This will generate the `.nvda-addon` package in the root directory.

## 🤝 internal details

This add-on uses `pycaw` (Python Core Audio Windows Library) to interface with WASAPI. It creates a "shaded" version of dependencies during the build process to avoid conflicts with NVDA's internal libraries.

## 📄 License

GPL v2

## 📢 Bugs and Suggestions

For reports on bugs, errors, or feature suggestions, please contact us.
We value your feedback to make this tool better for everyone.

Contact: https://t.me/tierryt2021
