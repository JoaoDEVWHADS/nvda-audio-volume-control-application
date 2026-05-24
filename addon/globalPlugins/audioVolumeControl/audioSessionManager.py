from typing import List, Optional
import logging
import sys
import os

_current_dir = os.path.dirname(__file__)
_lib_dir = os.path.join(_current_dir, 'lib')

if os.path.exists(_lib_dir):
    if _lib_dir not in sys.path:
        sys.path.insert(0, _lib_dir)
    
    # Dynamic psutil C extension resolver bootstrap
    try:
        import struct
        import shutil
        _psutil_dir = os.path.join(_lib_dir, 'psutil')
        if os.path.exists(_psutil_dir):
            is_64bit = struct.calcsize("P") * 8 == 64
            plat_tag = "win_amd64" if is_64bit else "win32"
            py_ver_num = sys.version_info.major * 100 + sys.version_info.minor
            # CPython 3.7+ use the cp37 stable ABI wheel
            if py_ver_num >= 307:
                src_name = f"_psutil_windows.cp37-{plat_tag}.pyd"
            else:
                py_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"
                src_name = f"_psutil_windows.{py_tag}-{plat_tag}.pyd"
            src_path = os.path.join(_psutil_dir, src_name)
            dest_path = os.path.join(_psutil_dir, "_psutil_windows.pyd")
            
            if os.path.exists(src_path):
                copy_needed = True
                if os.path.exists(dest_path):
                    try:
                        if os.path.getsize(src_path) == os.path.getsize(dest_path):
                            copy_needed = False
                    except:
                        pass
                
                if copy_needed:
                    try:
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                        shutil.copy2(src_path, dest_path)
                        logging.getLogger(__name__).info(f"VolumeControl: Copied C extension {src_name}")
                    except Exception as copy_err:
                        logging.getLogger(__name__).error(f"VolumeControl: Failed to copy C extension: {copy_err}")
            else:
                logging.getLogger(__name__).error(f"VolumeControl: Tagged C extension not found: {src_path}")
    except Exception as e:
        logging.getLogger(__name__).error(f"VolumeControl: Error during psutil bootstrap: {e}")

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
