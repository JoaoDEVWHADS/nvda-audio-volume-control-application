from typing import List, Optional
import logging
import sys
import os

_current_dir = os.path.dirname(__file__)
_lib_dir = os.path.join(_current_dir, 'lib')

if os.path.exists(_lib_dir):
    if _lib_dir not in sys.path:
        sys.path.insert(0, _lib_dir)
    modules_to_remove = [key for key in list(sys.modules.keys()) if key.startswith('psutil')]
    for mod in modules_to_remove:
        del sys.modules[mod]

try:
    from avc_pycaw.utils import AudioUtilities
    import psutil
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    logging.getLogger(__name__).error(f"Failed to import dependencies: {e}")

log = logging.getLogger(__name__)


class AudioSession:
    def __init__(self, session, pid: int, name: str):
        self.session = session
        self.pid = pid
        self.name = name
        self.volume_interface = None
        try:
            self.volume_interface = session.SimpleAudioVolume
        except Exception as e:
            log.error(f"Failed to get volume interface for {name}: {e}")


class AudioSessionManager:
    @staticmethod
    def check_dependencies() -> bool:
        return DEPENDENCIES_AVAILABLE
    
    @staticmethod
    def get_active_sessions() -> List[AudioSession]:
        if not DEPENDENCIES_AVAILABLE:
            log.error("Required dependencies (pycaw, psutil) are not available")
            return []
        
        sessions = []
        
        try:
            all_sessions = AudioUtilities.GetAllSessions()
            
            for session in all_sessions:
                if session.Process and session.State != 2:
                    try:
                        pid = session.ProcessId
                        name = AudioSessionManager.get_process_name(pid)
                        audio_session = AudioSession(session, pid, name)
                        if audio_session.volume_interface:
                            sessions.append(audio_session)
                        else:
                            log.warning(f"Skipping session for {name} - no volume interface")
                    except Exception as e:
                        log.error(f"Error processing session: {e}")
                        continue
            
            sessions.sort(key=lambda s: s.name.lower())
            log.info(f"Found {len(sessions)} active audio sessions")
            
        except Exception as e:
            log.error(f"Failed to enumerate audio sessions: {e}")
            return []
        
        return sessions
    
    @staticmethod
    def get_process_name(pid: int) -> str:
        if not DEPENDENCIES_AVAILABLE:
            return f"Process {pid}"
        
        try:
            process = psutil.Process(pid)
            name = process.name()
            if name.lower().endswith('.exe'):
                name = name[:-4]
            return name
        except psutil.NoSuchProcess:
            log.warning(f"Process {pid} no longer exists")
            return f"Unknown Process ({pid})"
        except psutil.AccessDenied:
            log.warning(f"Access denied to process {pid}")
            return f"System Process ({pid})"
        except Exception as e:
            log.error(f"Error getting process name for PID {pid}: {e}")
            return f"Process {pid}"
    
    @staticmethod
    def get_foreground_app_name() -> Optional[str]:
        try:
            import win32gui
            import win32process
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return AudioSessionManager.get_process_name(pid)
        except ImportError:
            log.debug("win32gui/win32process not available for foreground detection")
            return None
        except Exception as e:
            log.error(f"Error getting foreground app: {e}")
            return None
