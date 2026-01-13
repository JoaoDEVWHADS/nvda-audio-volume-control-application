import wx
import logging

try:
    import ui
    NVDA_UI_AVAILABLE = True
except ImportError:
    NVDA_UI_AVAILABLE = False
    class ui:
        @staticmethod
        def message(msg):
            print(f"NVDA: {msg}")

from .audioSessionManager import AudioSessionManager
from .volumeController import VolumeController

log = logging.getLogger(__name__)

class VolumeControlDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Application Volume Control",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        
        self.sessions = []
        self.current_selection = -1
        
        self.InitUI()
        self.LoadSessions()
        self.AutoSelectForeground()
        
        self.appList.SetFocus()
    
    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        instructionsText = (
            "Select an application from the list, then press TAB to access volume controls."
        )
        instructionsLabel = wx.StaticText(self, label=instructionsText)
        instructionsLabel.Wrap(500)
        mainSizer.Add(instructionsLabel, flag=wx.ALL, border=10)
        
        listLabel = wx.StaticText(self, label="&Applications:")
        mainSizer.Add(listLabel, flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        
        self.appList = wx.ListBox(
            self,
            size=(500, 200),
            style=wx.LB_SINGLE
        )
        self.appList.Bind(wx.EVT_LISTBOX, self.OnSelectionChange)
        mainSizer.Add(
            self.appList,
            proportion=1,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            border=10
        )
        
        controlsSizer = wx.StaticBoxSizer(wx.VERTICAL, self, "Audio Control")
        
        sliderSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.volLabel = wx.StaticText(self, label="&Volume:")
        sliderSizer.Add(self.volLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        
        self.volSlider = wx.Slider(
            self,
            value=0,
            minValue=0,
            maxValue=100,
            size=(300, -1),
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.volSlider.Bind(wx.EVT_SLIDER, self.OnSliderChange)
        sliderSizer.Add(self.volSlider, proportion=1, flag=wx.EXPAND)
        
        controlsSizer.Add(sliderSizer, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.muteChk = wx.CheckBox(self, label="&Mute")
        self.muteChk.Bind(wx.EVT_CHECKBOX, self.OnMuteChange)
        controlsSizer.Add(self.muteChk, flag=wx.ALL, border=5)
        
        mainSizer.Add(controlsSizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        refreshBtn = wx.Button(self, label="&Refresh List")
        refreshBtn.Bind(wx.EVT_BUTTON, self.OnRefresh)
        buttonSizer.Add(refreshBtn, flag=wx.RIGHT, border=5)
        
        resetBtn = wx.Button(self, label="R&eset Defaults")
        resetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
        buttonSizer.Add(resetBtn, flag=wx.RIGHT, border=5)
        
        closeBtn = wx.Button(self, wx.ID_CLOSE, "&Close")
        closeBtn.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        buttonSizer.Add(closeBtn)
        
        mainSizer.Add(
            buttonSizer,
            flag=wx.ALIGN_CENTER | wx.ALL,
            border=10
        )
        
        self.SetSizer(mainSizer)
        self.Fit()
        self.Center()
        
        self.SetMinSize((450, 450))
    
    def LoadSessions(self):
        try:
            if not AudioSessionManager.check_dependencies():
                ui.message("Error: Required dependencies (pycaw, psutil) are not installed")
                self.appList.Clear()
                self.appList.Append("Dependencies not available")
                self.DisableControls()
                return
            
            self.sessions = AudioSessionManager.get_active_sessions()
            self.appList.Clear()
            
            if not self.sessions:
                self.appList.Append("No applications found")
                self.DisableControls()
                return
            
            for session in self.sessions:
                self.appList.Append(session.name)
            
            self.EnableControls()
            
            if self.appList.GetCount() > 0:
                 self.appList.SetSelection(0)
                 self.OnSelectionChange(None)

        except Exception as e:
            log.error(f"Failed to load sessions: {e}")
            self.appList.Clear()
            self.appList.Append(f"Error: {str(e)}")
            self.DisableControls()

    def DisableControls(self):
        self.volSlider.Disable()
        self.muteChk.Disable()
    
    def EnableControls(self):
        self.volSlider.Enable()
        self.muteChk.Enable()

    def AutoSelectForeground(self):
        if not self.sessions:
            return
        
        fg_name = AudioSessionManager.get_foreground_app_name()
        
        if fg_name:
            for i, session in enumerate(self.sessions):
                if session.name.lower() == fg_name.lower():
                    self.appList.SetSelection(i)
                    self.OnSelectionChange(None)
                    return
        
        if self.appList.GetSelection() == wx.NOT_FOUND and self.sessions:
            self.appList.SetSelection(0)
            self.OnSelectionChange(None)

    def OnSelectionChange(self, event):
        selection = self.appList.GetSelection()
        
        if selection == wx.NOT_FOUND or selection >= len(self.sessions):
            self.DisableControls()
            return
        
        self.EnableControls()
        session = self.sessions[selection]
        
        try:
            vol = int(VolumeController.get_volume(session))
            self.volSlider.SetValue(vol)
        except:
             pass

        try:
            is_muted = VolumeController.get_mute_state(session)
            self.muteChk.SetValue(is_muted)
        except:
             pass
    
    def OnSliderChange(self, event):
        selection = self.appList.GetSelection()
        if selection == wx.NOT_FOUND or selection >= len(self.sessions):
            return
            
        session = self.sessions[selection]
        vol = self.volSlider.GetValue()
        
        try:
            VolumeController.set_volume_absolute(session, vol)
        except Exception as e:
            log.error(f"Slider change failed: {e}")

    def OnMuteChange(self, event):
        selection = self.appList.GetSelection()
        if selection == wx.NOT_FOUND or selection >= len(self.sessions):
            return
            
        session = self.sessions[selection]
        is_muted = self.muteChk.GetValue()
        
        try:
            current_state = VolumeController.get_mute_state(session)
            if current_state != is_muted:
                VolumeController.toggle_mute(session)
                
        except Exception as e:
            log.error(f"Mute change failed: {e}")

    def OnRefresh(self, event):
        old_selection_name = None
        
        if self.current_selection >= 0 and self.current_selection < len(self.sessions):
            old_selection_name = self.sessions[self.current_selection].name
        
        self.LoadSessions()
        
        if old_selection_name and self.sessions:
            for i, session in enumerate(self.sessions):
                if session.name == old_selection_name:
                    self.appList.SetSelection(i)
                    self.OnSelectionChange(None)
                    return
        
        self.AutoSelectForeground()

    def OnReset(self, event):
        if not self.sessions:
            return
        
        count = 0
        for session in self.sessions:
            VolumeController.set_volume(session, 100.0)
            VolumeController.set_mute(session, False)
            count += 1
        
        self.OnSelectionChange(None)
        
        try:
            ui.message(f"Reset {count} applications to default")
        except:
            pass
