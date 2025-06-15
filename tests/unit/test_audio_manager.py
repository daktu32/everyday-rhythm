"""
Unit tests for AudioManager class
"""
import pytest
import pygame
import os
import sys
import time
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from audio.audio_manager import AudioManager


class TestAudioManager:
    """Test cases for AudioManager class"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        # Initialize pygame mixer for testing
        pygame.mixer.pre_init(buffer=512)  # Small buffer for testing
        pygame.mixer.init()
        
        # Path to test audio files
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
        self.test_audio_short = os.path.join(self.fixtures_dir, 'test_short.wav')
        self.test_audio_medium = os.path.join(self.fixtures_dir, 'test_medium.wav')
        self.invalid_audio = os.path.join(self.fixtures_dir, 'nonexistent.wav')
        
    def teardown_method(self):
        """Cleanup after each test"""
        # Stop any playing audio and cleanup
        pygame.mixer.stop()
        pygame.mixer.quit()
    
    def test_audio_manager_initialization(self):
        """Test AudioManager initializes correctly"""
        # Act
        manager = AudioManager()
        
        # Assert
        assert manager.current_music is None
        assert manager.start_time == 0
        assert manager.is_paused == False
        assert manager.volume == 1.0
    
    def test_audio_manager_custom_buffer_size(self):
        """Test AudioManager with custom buffer size"""
        # Act
        manager = AudioManager(buffer_size=2048)
        
        # Assert
        assert manager.buffer_size == 2048
    
    def test_load_valid_audio_file(self):
        """Test loading valid audio file"""
        # Arrange
        manager = AudioManager()
        
        # Act
        result = manager.load_music(self.test_audio_short)
        
        # Assert
        assert result == True
        assert manager.current_music is not None
        assert manager.current_file_path == self.test_audio_short
    
    def test_load_invalid_audio_file(self):
        """Test loading invalid audio file"""
        # Arrange
        manager = AudioManager()
        
        # Act
        result = manager.load_music(self.invalid_audio)
        
        # Assert
        assert result == False
        assert manager.current_music is None
    
    def test_load_empty_file_path(self):
        """Test loading with empty file path"""
        # Arrange
        manager = AudioManager()
        
        # Act
        result = manager.load_music("")
        
        # Assert
        assert result == False
        assert manager.current_music is None
    
    def test_play_music_without_loading(self):
        """Test playing music without loading a file first"""
        # Arrange
        manager = AudioManager()
        
        # Act & Assert
        # Should not raise exception, but should handle gracefully
        manager.play_music()
        assert manager.start_time == 0
    
    def test_play_music_with_loaded_file(self):
        """Test playing music with loaded file"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        
        # Act
        manager.play_music()
        
        # Assert
        assert manager.start_time > 0  # Should have a valid start time now
        assert manager.is_paused == False
    
    def test_stop_music(self):
        """Test stopping music playback"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        manager.play_music()
        
        # Act
        manager.stop_music()
        
        # Assert
        assert manager.start_time == 0
        assert manager.is_paused == False
    
    def test_pause_and_resume_music(self):
        """Test pausing and resuming music"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        manager.play_music()
        
        # Act - Pause
        manager.pause_music()
        
        # Assert - Paused
        assert manager.is_paused == True
        
        # Act - Resume
        manager.resume_music()
        
        # Assert - Resumed
        assert manager.is_paused == False
    
    def test_volume_control(self):
        """Test volume control functionality"""
        # Arrange
        manager = AudioManager()
        
        # Test valid volume levels
        test_volumes = [0.0, 0.5, 1.0]
        
        for volume in test_volumes:
            # Act
            manager.set_volume(volume)
            
            # Assert
            assert manager.volume == volume
    
    def test_volume_control_invalid_values(self):
        """Test volume control with invalid values"""
        # Arrange
        manager = AudioManager()
        
        # Test invalid volume levels (should be clamped)
        test_cases = [
            (-0.5, 0.0),  # Below minimum
            (1.5, 1.0),   # Above maximum
            (2.0, 1.0),   # Way above maximum
        ]
        
        for input_volume, expected_volume in test_cases:
            # Act
            manager.set_volume(input_volume)
            
            # Assert
            assert manager.volume == expected_volume
    
    def test_get_current_time_not_playing(self):
        """Test getting current time when not playing"""
        # Arrange
        manager = AudioManager()
        
        # Act
        current_time = manager.get_current_time()
        
        # Assert
        assert current_time == 0.0
    
    def test_get_current_time_while_playing(self):
        """Test getting current time while playing"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        manager.play_music()
        
        # Wait a small amount of time
        time.sleep(0.1)
        
        # Act
        current_time = manager.get_current_time()
        
        # Assert
        assert current_time > 0  # Should be positive after waiting
        assert current_time < 1000  # Should be less than 1 second
        
        # Cleanup
        manager.stop_music()
    
    def test_is_playing_status(self):
        """Test is_playing status tracking"""
        # Arrange
        manager = AudioManager()
        
        # Initially not playing
        assert manager.is_playing() == False
        
        # Load and play
        manager.load_music(self.test_audio_short)
        manager.play_music()
        
        # Should be playing
        assert manager.is_playing() == True
        
        # Stop
        manager.stop_music()
        
        # Should not be playing
        assert manager.is_playing() == False
    
    def test_get_duration_without_file(self):
        """Test getting duration without loaded file"""
        # Arrange
        manager = AudioManager()
        
        # Act
        duration = manager.get_duration()
        
        # Assert
        assert duration == 0.0
    
    def test_get_duration_with_file(self):
        """Test getting duration with loaded file"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        
        # Act
        duration = manager.get_duration()
        
        # Assert
        # test_short.wav is 1 second long
        assert 900 <= duration <= 1100  # Allow some tolerance (900-1100ms)
    
    def test_cleanup(self):
        """Test cleanup functionality"""
        # Arrange
        manager = AudioManager()
        manager.load_music(self.test_audio_short)
        manager.play_music()
        
        # Act
        manager.cleanup()
        
        # Assert
        assert manager.current_music is None
        assert manager.start_time == 0
        assert manager.is_paused == False
    
    def test_multiple_file_loading(self):
        """Test loading multiple files sequentially"""
        # Arrange
        manager = AudioManager()
        
        # Load first file
        result1 = manager.load_music(self.test_audio_short)
        first_file = manager.current_file_path
        
        # Load second file
        result2 = manager.load_music(self.test_audio_medium)
        second_file = manager.current_file_path
        
        # Assert
        assert result1 == True
        assert result2 == True
        assert first_file != second_file
        assert manager.current_file_path == self.test_audio_medium
    
    @patch('pygame.mixer.Sound')
    def test_pygame_error_handling(self, mock_sound):
        """Test handling of pygame errors"""
        # Arrange
        mock_sound.side_effect = pygame.error("Test pygame error")
        manager = AudioManager()
        
        # Act
        result = manager.load_music(self.test_audio_short)
        
        # Assert
        assert result == False
        assert manager.current_music is None
