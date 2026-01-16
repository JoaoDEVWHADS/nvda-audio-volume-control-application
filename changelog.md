# Changelog - NVDA Per-Application Volume Control

## Version 2026.01.16

### New Features
- Automatic update checker on NVDA startup
- Downloads and installs updates from GitHub releases
- Improved dialog focus handling

### Bug Fixes
- Fixed dependency loading issues
- Vendorized pycaw library as avc_pycaw to avoid conflicts
- Added Windows binary support for psutil

### Technical
- Minimum NVDA: 2019.3
- Tested on: NVDA 2025.3.2
- Dependencies: avc_pycaw (vendorized), psutil (Windows binary)

---

## Version 1.0.0 (2026-01-12)

### Initial Release
- List all applications with active audio sessions
- Control volume per application with keyboard shortcuts
- Volume increments: 1% (arrows), 5% (Up/Down), 10% (Page Up/Down)
- Quick presets: Home (0%), End (100%)
- Real-time volume announcements via NVDA
- Mute/unmute individual applications (M key)
- Auto-select foreground application on dialog open
- Refresh functionality to update session list
- Fully accessible keyboard navigation
- Alphabetically sorted application list
