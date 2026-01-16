from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries
from site_scons.site_tools.NVDATool.utils import _

addon_info = AddonInfo(
	addon_name="audioVolumeControl",
	addon_summary=_("Per-Application Volume Control"),
	addon_description=_("""Control the volume of individual applications using keyboard shortcuts.
Press Ctrl+NVDA+Y to open the volume control dialog and adjust volume per application.
Supports precise volume control with multiple increment levels and real-time announcements.

Tested on NVDA 2025.3.2. Users may modify manifest.ini for other versions.
Contact: https://t.me/tierryt2021"""),
	addon_version="2026.01.16",
	addon_changelog=_("""Version 2026.01.16
- Fixed update system with robust file handling
- Vendorized pycaw library to avoid conflicts
- Windows binary support for psutil
- Improved dependency management
- Uses NVDA built-in comtypes"""),
	addon_author="JoaoDEVWHADS",
	addon_url="https://github.com/JoaoDEVWHADS/nvda-audio-volume-control-application",
	addon_sourceURL="https://github.com/JoaoDEVWHADS/nvda-audio-volume-control-application",
	addon_docFileName="readme.html",
	addon_minimumNVDAVersion="2019.3",
	addon_lastTestedNVDAVersion="2025.3",
	addon_updateChannel=None,
	addon_license="GPL v2",
	addon_licenseURL="https://www.gnu.org/licenses/gpl-2.0.html",
)

pythonSources: list[str] = [
	"addon/globalPlugins/audioVolumeControl/*.py",
	"addon/globalPlugins/audioVolumeControl/**/*.py",
]

i18nSources: list[str] = pythonSources + ["buildVars.py"]

excludedFiles: list[str] = []

baseLanguage: str = "en"

markdownExtensions: list[str] = []

brailleTables: BrailleTables = {}

symbolDictionaries: SymbolDictionaries = {}
