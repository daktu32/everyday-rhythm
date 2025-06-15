"""
AudioManager - Audio playback and timing management
"""
import pygame
import os
import sys
import time
from typing import Optional

# Add src to path for imports (must be before local imports)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Local imports after path setup
from utils.config import Config  # noqa: E402


class AudioManager:
    """Manages audio playback, timing synchronization, and audio analysis"""
    
    # Supported audio formats
    SUPPORTED_FORMATS = {
        '.wav': 'WAV Audio',
        '.mp3': 'MP3 Audio', 
        '.ogg': 'OGG Vorbis',
        '.flac': 'FLAC Audio'
    }
    
    def __init__(self, buffer_size: Optional[int] = None):
        """Initialize the audio manager"""
        self.buffer_size = buffer_size or Config.AUDIO_BUFFER_SIZE
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(buffer=self.buffer_size)
            pygame.mixer.init()
        
        # Audio state
        self.current_music: Optional[pygame.mixer.Sound] = None
        self.current_file_path: str = ""
        self.start_time: float = 0
        self.pause_time: float = 0
        self.is_paused: bool = False
        self.volume: float = 1.0
        
        # Use system time as fallback for testing
        self._use_system_time = False
        
        # Debug info
        if Config.is_debug():
            print(f"AudioManager initialized - Buffer: {self.buffer_size}")
    
    def _get_time(self) -> float:
        """Get current time in milliseconds"""
        if self._use_system_time:
            return time.time() * 1000
        else:
            pygame_time = pygame.time.get_ticks()
            if pygame_time == 0:
                # Fallback to system time if pygame time is not working
                self._use_system_time = True
                return time.time() * 1000
            return float(pygame_time)
    
    def load_music(self, file_path: str) -> bool:
        """Load music file for playback"""
        if not file_path or not os.path.exists(file_path):
            if Config.is_debug():
                print(f"Audio file not found: {file_path}")
            return False
        
        # Check if format is supported
        if not self.is_supported_format(file_path):
            if Config.is_debug():
                print(f"Unsupported audio format: {self.get_format_info(file_path)}")
            return False
        
        try:
            # Stop current music if playing
            self.stop_music()
            
            # Load new music file
            self.current_music = pygame.mixer.Sound(file_path)
            self.current_file_path = file_path
            
            # Set volume
            if self.current_music:
                self.current_music.set_volume(self.volume)
            
            if Config.is_debug():
                print(f"Loaded audio file: {file_path} ({self.get_format_info(file_path)})")
            
            return True
            
        except pygame.error as e:
            if Config.is_debug():
                print(f"Failed to load audio file {file_path}: {e}")
            self.current_music = None
            self.current_file_path = ""
            return False
    
    def play_music(self) -> None:
        """Start music playback"""
        if not self.current_music:
            if Config.is_debug():
                print("No music loaded to play")
            return
        
        try:
            # Stop any currently playing music
            pygame.mixer.stop()
            
            # Start playback
            self.current_music.play()
            self.start_time = self._get_time()
            self.is_paused = False
            
            if Config.is_debug():
                print(f"Music playback started at time: {self.start_time}")
                
        except pygame.error as e:
            if Config.is_debug():
                print(f"Failed to play music: {e}")
    
    def stop_music(self) -> None:
        """Stop music playback"""
        try:
            pygame.mixer.stop()
            self.start_time = 0
            self.pause_time = 0
            self.is_paused = False
            
            if Config.is_debug():
                print("Music playback stopped")
                
        except pygame.error as e:
            if Config.is_debug():
                print(f"Failed to stop music: {e}")
    
    def pause_music(self) -> None:
        """Pause music playback"""
        if not self.is_playing():
            return
        
        try:
            pygame.mixer.pause()
            self.pause_time = self._get_time()
            self.is_paused = True
            
            if Config.is_debug():
                print("Music playback paused")
                
        except pygame.error as e:
            if Config.is_debug():
                print(f"Failed to pause music: {e}")
    
    def resume_music(self) -> None:
        """Resume music playback"""
        if not self.is_paused:
            return
        
        try:
            pygame.mixer.unpause()
            
            # Adjust start time to account for pause duration
            if self.pause_time > 0:
                pause_duration = self._get_time() - self.pause_time
                self.start_time += pause_duration
                self.pause_time = 0
            
            self.is_paused = False
            
            if Config.is_debug():
                print("Music playback resumed")
                
        except pygame.error as e:
            if Config.is_debug():
                print(f"Failed to resume music: {e}")
    
    def set_volume(self, volume: float) -> None:
        """Set playback volume (0.0 - 1.0)"""
        # Clamp volume to valid range
        self.volume = max(0.0, min(1.0, volume))
        
        # Apply to current music if loaded
        if self.current_music:
            self.current_music.set_volume(self.volume)
        
        if Config.is_debug():
            print(f"Volume set to: {self.volume}")
    
    def get_current_time(self) -> float:
        """Get current playback time in milliseconds"""
        if not self.is_playing() and not self.is_paused:
            return 0.0
        
        if self.is_paused:
            return float(self.pause_time - self.start_time)
        
        return float(self._get_time() - self.start_time)
    
    def get_duration(self) -> float:
        """Get total duration of loaded music in milliseconds"""
        if not self.current_music:
            return 0.0
        
        try:
            # pygame.mixer.Sound.get_length() returns seconds
            duration_seconds = self.current_music.get_length()
            return duration_seconds * 1000.0  # Convert to milliseconds
        except:
            return 0.0
    
    def is_playing(self) -> bool:
        """Check if music is currently playing"""
        try:
            return pygame.mixer.get_busy() and not self.is_paused
        except:
            return False
    
    def cleanup(self) -> None:
        """Clean up audio resources"""
        try:
            self.stop_music()
            self.current_music = None
            self.current_file_path = ""
            self.start_time = 0
            self.pause_time = 0
            self.is_paused = False
            
            if Config.is_debug():
                print("AudioManager cleanup completed")
                
        except Exception as e:
            if Config.is_debug():
                print(f"Error during AudioManager cleanup: {e}")
    
    def get_audio_info(self) -> dict:
        """Get information about currently loaded audio"""
        if not self.current_music or not self.current_file_path:
            return {}
        
        return {
            "file_path": self.current_file_path,
            "duration_ms": self.get_duration(),
            "current_time_ms": self.get_current_time(),
            "is_playing": self.is_playing(),
            "is_paused": self.is_paused,
            "volume": self.volume,
            "format": self.get_format_info(self.current_file_path)
        }

    def is_supported_format(self, file_path: str) -> bool:
        """Check if the audio file format is supported"""
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_FORMATS

    def get_format_info(self, file_path: str) -> str:
        """Get format information for the file"""
        _, ext = os.path.splitext(file_path.lower())
        return self.SUPPORTED_FORMATS.get(ext, f"Unknown format ({ext})")
