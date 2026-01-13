import sys
import os

_current_dir = os.path.dirname(__file__)
_addon_lib = os.path.abspath(os.path.join(_current_dir, '..', '..', 'lib'))
if os.path.exists(_addon_lib) and _addon_lib not in sys.path:
    sys.path.insert(0, _addon_lib)

import globalPluginHandler
import logging
import addonHandler

addonHandler.initTranslation()

try:
    import gui
    import wx
    import ui
    NVDA_AVAILABLE = True
except ImportError:
    NVDA_AVAILABLE = False

from .volumeControlDialog import VolumeControlDialog

log = logging.getLogger(__name__)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Audio Volume Control")
    
    __gestures__ = {
        "kb:control+NVDA+y": "showVolumeControl"
    }
    
    def __init__(self):
        super().__init__()
        log.info("Audio Volume Control add-on initialized")
        
        if not NVDA_AVAILABLE:
            log.warning("NVDA environment not detected - limited functionality")
    
    def terminate(self):
        log.info("Audio Volume Control add-on terminated")
        super().terminate()
    
    def script_showVolumeControl(self, gesture):
        try:
            if not NVDA_AVAILABLE:
                log.error("Cannot show dialog - NVDA environment not available")
                return
            
            log.debug("Opening volume control dialog")
            wx.CallAfter(self._showDialog)
            
        except Exception as e:
            log.error(f"Failed to show volume control dialog: {e}", exc_info=True)
            try:
                ui.message("Error: Could not open volume control")
            except:
                pass
    
    def _showDialog(self):
        try:
            dialog = VolumeControlDialog(gui.mainFrame)
            dialog.ShowModal()
            dialog.Destroy()
        except Exception as e:
            log.error(f"Error in dialog: {e}", exc_info=True)
            try:
                ui.message(f"Error opening volume control: {str(e)}")
            except:
                pass
    
    script_showVolumeControl.__doc__ = _("Show the per-application volume control dialog")
