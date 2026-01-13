# Changelog - NVDA Per-Application Volume Control

## Version 1.0.0 (2026-01-12)

### Initial Release

**Features:**
- List all applications with active audio sessions
- Control volume per application with keyboard shortcuts
- Multiple volume increment levels:
  - Fine control: ±1% (Left/Right arrows)
  - Medium control: ±5% (Up/Down arrows)
  - Large control: ±10% (Page Up/Down)
- Quick volume presets:
  - Home: Set to 0%
  - End: Set to 100%
- Real-time volume announcements via NVDA
- Mute/unmute individual applications (M key)
- Auto-select foreground application on dialog open
- Refresh functionality to update session list
- Fully accessible keyboard navigation
- Alphabetically sorted application list

**Technical Details:**
- Uses Windows Audio Session API (WASAPI) via pycaw
- Compatible with Windows 10 and Windows 11
- Minimum NVDA version: 2019.3
- Last tested NVDA version: 2024.4
- Dependencies: pycaw, comtypes, psutil

**Known Limitations:**
- Windows-only (WASAPI requirement)
- Only shows applications actively playing audio
- Some system processes may require administrator privileges

---

## Future Versions

### Planned for 1.1.0
- Volume profiles (save and load presets)
- Custom hotkeys for specific applications
- Configuration dialog for preferences
- Persistent favorites list

### Planned for 1.2.0
- Audio device selection per application
- Volume change history
- Keyboard shortcuts for common applications
- Enhanced error messages

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.
