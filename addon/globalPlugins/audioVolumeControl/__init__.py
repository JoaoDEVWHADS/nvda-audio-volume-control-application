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

from .updateChecker import UpdateChecker, CURRENT_VERSION, show_update_dialog

log = logging.getLogger(__name__)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _("Audio Volume Control")
    
    __gestures__ = {
        "kb:control+NVDA+y": "showVolumeControl"
    }
    
    def __init__(self):
        super().__init__()
        log.info("Audio Volume Control add-on initialized")
        self.updateChecker = None
        if NVDA_AVAILABLE:
            try:
                self.updateChecker = UpdateChecker(self._on_update_available)
                self.updateChecker.start()
                log.info("Update checker started")
            except Exception as e:
                log.error(f"Failed to start update checker: {e}")
        else:
            log.warning("NVDA environment not detected")
    
    def terminate(self):
        if self.updateChecker:
            try:
                self.updateChecker.stop()
            except Exception as e:
                log.error(f"Error stopping update checker: {e}")
        log.info("Audio Volume Control add-on terminated")
        super().terminate()
    
    def _on_update_available(self, version, download_url, release_info):
        log.info(f"Update available: {version}")
        try:
            show_update_dialog(CURRENT_VERSION, version, download_url, release_info)
        except Exception as e:
            log.error(f"Error showing update dialog: {e}")
    
    def script_showVolumeControl(self, gesture):
        try:
            if not NVDA_AVAILABLE:
                log.error("Cannot show dialog - NVDA not available")
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
            import sys
            import os
            lib_path = os.path.join(os.path.dirname(__file__), 'lib')
            if os.path.exists(lib_path) and lib_path not in sys.path:
                sys.path.insert(0, lib_path)
            from .volumeControlDialog import VolumeControlDialog
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
