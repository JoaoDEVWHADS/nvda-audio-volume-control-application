import logging

log = logging.getLogger(__name__)

class VolumeController:
    @staticmethod
    def get_volume(session) -> float:
        if not session or not session.volume_interface:
            log.error("Invalid session or volume interface")
            return 0.0
        
        try:
            volume = session.volume_interface.GetMasterVolume()
            volume_percent = volume * 100.0
            return round(volume_percent, 1)
        except Exception as e:
            log.error(f"Failed to get volume for {session.name}: {e}")
            return 0.0
    
    @staticmethod
    def set_volume(session, volume_percent: float) -> float:
        if not session or not session.volume_interface:
            log.error("Invalid session or volume interface")
            return 0.0
        
        volume_percent = max(0.0, min(100.0, volume_percent))
        
        try:
            volume_scalar = volume_percent / 100.0
            session.volume_interface.SetMasterVolume(volume_scalar, None)
            log.debug(f"Set volume for {session.name} to {volume_percent}%")
            return volume_percent
        except Exception as e:
            log.error(f"Failed to set volume for {session.name}: {e}")
            return VolumeController.get_volume(session)
    
    @staticmethod
    def adjust_volume(session, delta_percent: int) -> float:
        if not session or not session.volume_interface:
            log.error("Invalid session or volume interface")
            return 0.0
        
        current_volume = VolumeController.get_volume(session)
        new_volume = current_volume + delta_percent
        return VolumeController.set_volume(session, new_volume)
    
    @staticmethod
    def set_volume_absolute(session, target_percent: int) -> float:
        return VolumeController.set_volume(session, float(target_percent))
    
    @staticmethod
    def get_mute_state(session) -> bool:
        if not session or not session.volume_interface:
            return False
        
        try:
            return session.volume_interface.GetMute()
        except Exception as e:
            log.error(f"Failed to get mute state for {session.name}: {e}")
            return False
    
    @staticmethod
    def set_mute(session, mute: bool) -> bool:
        if not session or not session.volume_interface:
            return False
        
        try:
            session.volume_interface.SetMute(mute, None)
            log.debug(f"Set mute for {session.name} to {mute}")
            return mute
        except Exception as e:
            log.error(f"Failed to set mute for {session.name}: {e}")
            return VolumeController.get_mute_state(session)
    
    @staticmethod
    def toggle_mute(session) -> bool:
        current_mute = VolumeController.get_mute_state(session)
        return VolumeController.set_mute(session, not current_mute)
