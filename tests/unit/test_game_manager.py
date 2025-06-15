"""
Unit tests for GameManager class
"""

import pytest
import pygame
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from core.game_manager import GameManager


class TestGameManager:
    """Test cases for GameManager class"""

    def setup_method(self):
        """Setup test environment before each test"""
        # Mock pygame to avoid actual window creation during tests
        self.pygame_mock = Mock()

    def teardown_method(self):
        """Cleanup after each test"""
        # Ensure pygame is properly cleaned up
        if pygame.get_init():
            pygame.quit()

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("core.game_manager.AudioManager")
    def test_game_manager_initialization(
        self, mock_audio_manager, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test GameManager initializes correctly"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock.return_value = mock_clock_instance
        mock_audio_instance = Mock()
        mock_audio_manager.return_value = mock_audio_instance

        # Act
        manager = GameManager()

        # Assert
        assert (
            manager.running == False
        )  # Should start as False, set to True when run() is called
        assert manager.screen == mock_screen
        assert manager.clock == mock_clock_instance
        assert manager.audio_manager == mock_audio_instance
        mock_init.assert_called_once()
        mock_display.assert_called_once()
        mock_caption.assert_called_once_with("Everyday Rhythm")
        mock_audio_manager.assert_called_once()
        mock_caption.assert_called_once_with("Everyday Rhythm")

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_game_manager_screen_dimensions(
        self, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test GameManager creates screen with correct dimensions"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen

        # Act
        manager = GameManager()

        # Assert
        # Should call set_mode with default dimensions (800, 600)
        mock_display.assert_called_once_with((800, 600))

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.event.get")
    def test_handle_events_quit(
        self, mock_event_get, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test handling quit events"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_quit_event = Mock()
        mock_quit_event.type = pygame.QUIT
        mock_event_get.return_value = [mock_quit_event]

        manager = GameManager()
        manager.running = True

        # Act
        manager.handle_events()

        # Assert
        assert manager.running == False

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.event.get")
    def test_handle_events_space_key(
        self, mock_event_get, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test handling space key events"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_key_event = Mock()
        mock_key_event.type = pygame.KEYDOWN
        mock_key_event.key = pygame.K_SPACE
        mock_event_get.return_value = [mock_key_event]

        manager = GameManager()

        # Act
        result = manager.handle_events()

        # Assert
        # Should return True when space key is pressed
        assert result == True

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.display.flip")
    def test_render_basic(
        self, mock_flip, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test basic rendering functionality"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen

        manager = GameManager()

        # Act
        manager.render()

        # Assert
        # Should fill screen with black background
        mock_screen.fill.assert_called_once_with((0, 0, 0))
        # Should call display.flip()
        mock_flip.assert_called_once()

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_update_method_exists(
        self, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test update method exists and can be called"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen

        manager = GameManager()

        # Act & Assert
        # Should not raise any exceptions
        manager.update()
        assert True  # If we get here, update() method exists and works

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_fps_target(self, mock_clock, mock_caption, mock_display, mock_init):
        """Test FPS target is set correctly"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock.return_value = mock_clock_instance

        manager = GameManager()

        # Act
        manager.tick()

        # Assert
        # Should call clock.tick with 60 FPS
        mock_clock_instance.tick.assert_called_once_with(60)
    
    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("core.game_manager.AudioManager")
    def test_audio_integration(
        self, mock_audio_manager, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test GameManager audio integration"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock.return_value = mock_clock_instance
        mock_audio_instance = Mock()
        mock_audio_manager.return_value = mock_audio_instance
        
        manager = GameManager()
        
        # Act & Assert - Test audio methods
        manager.load_audio("test.wav")
        mock_audio_instance.load_music.assert_called_once_with("test.wav")
        
        manager.play_audio()
        mock_audio_instance.play_music.assert_called_once()
        
        manager.stop_audio()
        mock_audio_instance.stop_music.assert_called_once()
        
        manager.set_volume(0.5)
        mock_audio_instance.set_volume.assert_called_once_with(0.5)
    
    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("core.game_manager.AudioManager")
    def test_cleanup_with_audio(
        self, mock_audio_manager, mock_clock, mock_caption, mock_display, mock_init
    ):
        """Test cleanup includes audio cleanup"""
        # Arrange
        mock_screen = Mock()
        mock_display.return_value = mock_screen
        mock_audio_instance = Mock()
        mock_audio_manager.return_value = mock_audio_instance
        
        manager = GameManager()
        
        # Act
        manager.cleanup()
        
        # Assert
        mock_audio_instance.cleanup.assert_called_once()
