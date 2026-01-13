# -*- coding: utf-8 -*-
"""
Audio Session Manager for NVDA Volume Control Add-on
Handles enumeration and management of Windows audio sessions using WASAPI.
"""

from typing import List, Optional
import logging
import sys
import os

# Add current directory to sys.path to find bundled dependencies (pycaw, comtypes, psutil)
_current_dir = os.path.dirname(__file__)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

try:
    # Try importing from local bundle (renamed to avoid conflict)
    # We use dep_pycaw instead of pycaw because NVDA has its own incompatible pycaw
    from dep_pycaw.pycaw import AudioUtilities
    import psutil
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    logging.getLogger(__name__).error(f"Failed to import dependencies: {e}")

log = logging.getLogger(__name__)


class AudioSession:
    """Represents an active audio session with volume control capabilities."""
    
    def __init__(self, session, pid: int, name: str):
        """
        Initialize an audio session.
        
        Args:
            session: The pycaw audio session object
            pid: Process ID of the application
            name: Human-readable name of the application
        """
        self.session = session
        self.pid = pid
        self.name = name
        self.volume_interface = None
        
        # Get volume interface
        try:
            self.volume_interface = session.SimpleAudioVolume
        except Exception as e:
            log.error(f"Failed to get volume interface for {name}: {e}")


class AudioSessionManager:
    """Manages Windows audio sessions using WASAPI."""
    
    @staticmethod
    def check_dependencies() -> bool:
        """
        Check if required dependencies are available.
        
        Returns:
            bool: True if dependencies are available, False otherwise
        """
        return DEPENDENCIES_AVAILABLE
    
    @staticmethod
    def get_active_sessions() -> List[AudioSession]:
        """
        Enumerate all active audio sessions.
        
        Returns:
            List[AudioSession]: List of active audio sessions, sorted alphabetically
        """
        if not DEPENDENCIES_AVAILABLE:
            log.error("Required dependencies (pycaw, psutil) are not available")
            return []
        
        sessions = []
        
        try:
            # Get all audio sessions
            all_sessions = AudioUtilities.GetAllSessions()
            
            for session in all_sessions:
                # Filter for active sessions with a process
                # Filter for active sessions (State 0=Inactive, 1=Active, 2=Expired)
                # User wants to see all apps, so we include Inactive (0) and Active (1)
                # We skip Expired (2) if it ever shows up
                if session.Process and session.State != 2:
                    try:
                        pid = session.ProcessId
                        name = AudioSessionManager.get_process_name(pid)
                        
                        audio_session = AudioSession(session, pid, name)
                        
                        # Only add if we successfully got the volume interface
                        if audio_session.volume_interface:
                            sessions.append(audio_session)
                        else:
                            log.warning(f"Skipping session for {name} - no volume interface")
                            
                    except Exception as e:
                        log.error(f"Error processing session: {e}")
                        continue
            
            # Sort alphabetically by name (case-insensitive)
            sessions.sort(key=lambda s: s.name.lower())
            
            log.info(f"Found {len(sessions)} active audio sessions")
            
        except Exception as e:
            log.error(f"Failed to enumerate audio sessions: {e}")
            return []
        
        return sessions
    
    @staticmethod
    def get_process_name(pid: int) -> str:
        """
        Convert PID to human-readable process name.
        
        Args:
            pid: Process ID
            
        Returns:
            str: Human-readable process name
        """
        if not DEPENDENCIES_AVAILABLE:
            return f"Process {pid}"
        
        try:
            process = psutil.Process(pid)
            name = process.name()
            
            # Remove .exe extension for cleaner display
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
        """
        Get the name of the foreground application.
        
        Returns:
            Optional[str]: Name of foreground app, or None if unavailable
        """
        try:
            import win32gui
            import win32process
            
            # Get foreground window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Get process ID from window handle
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            return AudioSessionManager.get_process_name(pid)
            
        except ImportError:
            log.debug("win32gui/win32process not available for foreground detection")
            return None
        except Exception as e:
            log.error(f"Error getting foreground app: {e}")
            return None
