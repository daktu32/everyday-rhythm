"""
Integration tests for audio system
"""
import pytest
import pygame
import os
import sys
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from audio.audio_manager import AudioManager
from audio.audio_analyzer import AudioAnalyzer


class TestAudioIntegration:
    """Integration tests for audio system components"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        # Initialize pygame for testing
        pygame.mixer.pre_init(buffer=512)
        pygame.mixer.init()
        
        # Path to test audio files
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
        self.test_audio_short = os.path.join(self.fixtures_dir, 'test_short.wav')
        self.test_audio_medium = os.path.join(self.fixtures_dir, 'test_medium.wav')
    
    def teardown_method(self):
        """Cleanup after each test"""
        pygame.mixer.stop()
        pygame.mixer.quit()
    
    def test_audio_manager_and_analyzer_integration(self):
        """Test AudioManager and AudioAnalyzer working together"""
        # Arrange
        manager = AudioManager()
        analyzer = AudioAnalyzer()
        
        # Act - Load and analyze audio
        load_result = manager.load_music(self.test_audio_short)
        analysis_result = analyzer.analyze_audio(self.test_audio_short)
        
        # Assert
        assert load_result == True
        assert isinstance(analysis_result, dict)
        
        # Check that both components can work with the same file
        if analysis_result:  # Only if librosa is available
            assert 'duration' in analysis_result
            assert analysis_result['duration'] > 0
        
        # Test playback
        manager.play_music()
        assert manager.is_playing() == True
        
        # Cleanup
        manager.cleanup()
    
    def test_audio_file_compatibility(self):
        """Test audio file format compatibility"""
        # Arrange
        manager = AudioManager()
        analyzer = AudioAnalyzer()
        
        test_files = [self.test_audio_short, self.test_audio_medium]
        
        for audio_file in test_files:
            if os.path.exists(audio_file):
                # Act
                load_result = manager.load_music(audio_file)
                analysis_result = analyzer.analyze_audio(audio_file)
                
                # Assert
                assert load_result == True
                
                # Test basic playback
                manager.play_music()
                time.sleep(0.1)  # Brief playback
                manager.stop_music()
                
                # Verify analysis (if librosa available)
                if analyzer.is_available() and analysis_result:
                    assert 'duration' in analysis_result
                    assert analysis_result['duration'] > 0
    
    def test_audio_timing_accuracy(self):
        """Test audio timing accuracy between manager and analyzer"""
        # Arrange
        manager = AudioManager()
        analyzer = AudioAnalyzer()
        
        # Load audio file
        manager.load_music(self.test_audio_short)
        
        # Get duration from both sources
        manager_duration = manager.get_duration()
        
        if analyzer.is_available():
            analysis_result = analyzer.analyze_audio(self.test_audio_short)
            if analysis_result and 'duration' in analysis_result:
                analyzer_duration = analysis_result['duration'] * 1000  # Convert to ms
                
                # Assert durations are close (within 100ms tolerance)
                duration_diff = abs(manager_duration - analyzer_duration)
                assert duration_diff < 100, f"Duration mismatch: {duration_diff}ms"
    
    def test_audio_playback_with_analysis_data(self):
        """Test using analysis data to control playback"""
        # Arrange
        manager = AudioManager()
        analyzer = AudioAnalyzer()
        
        # Load and analyze
        manager.load_music(self.test_audio_short)
        
        if analyzer.is_available():
            tempo = analyzer.get_tempo(self.test_audio_short)
            beats = analyzer.get_beats(self.test_audio_short)
            
            # Start playback
            manager.play_music()
            
            # Verify we can get timing information
            current_time = manager.get_current_time()
            assert current_time >= 0
            
            # If we have beat data, verify it's reasonable
            if beats:
                assert len(beats) > 0
                assert all(beat >= 0 for beat in beats)
                assert tempo > 0
            
            manager.stop_music()
    
    def test_audio_volume_control_integration(self):
        """Test volume control across audio components"""
        # Arrange
        manager = AudioManager()
        
        # Test volume levels
        test_volumes = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        manager.load_music(self.test_audio_short)
        
        for volume in test_volumes:
            # Act
            manager.set_volume(volume)
            
            # Assert
            assert manager.volume == volume
            
            # Test playback at this volume
            manager.play_music()
            time.sleep(0.05)  # Brief playback
            manager.stop_music()
    
    def test_audio_error_recovery(self):
        """Test error recovery in audio system"""
        # Arrange
        manager = AudioManager()
        analyzer = AudioAnalyzer()
        
        # Test with invalid file
        invalid_file = os.path.join(self.fixtures_dir, 'nonexistent.wav')
        
        # Act
        load_result = manager.load_music(invalid_file)
        analysis_result = analyzer.analyze_audio(invalid_file)
        
        # Assert - Should handle errors gracefully
        assert load_result == False
        assert analysis_result == {}
        
        # Verify system can still work with valid files after error
        valid_load = manager.load_music(self.test_audio_short)
        assert valid_load == True
    
    def test_audio_cleanup_integration(self):
        """Test proper cleanup of audio resources"""
        # Arrange
        manager = AudioManager()
        
        # Use audio system
        manager.load_music(self.test_audio_short)
        manager.play_music()
        time.sleep(0.1)
        
        # Act - Cleanup
        manager.cleanup()
        
        # Assert - System should be in clean state
        assert manager.current_music is None
        assert manager.start_time == 0
        assert manager.is_paused == False
        assert not manager.is_playing()
    
    def test_multiple_audio_files_sequence(self):
        """Test loading and playing multiple audio files in sequence"""
        # Arrange
        manager = AudioManager()
        test_files = [self.test_audio_short, self.test_audio_medium]
        
        for audio_file in test_files:
            if os.path.exists(audio_file):
                # Act
                load_result = manager.load_music(audio_file)
                
                # Assert
                assert load_result == True
                assert manager.current_file_path == audio_file
                
                # Test playback
                manager.play_music()
                time.sleep(0.05)  # Brief playback
                manager.stop_music()
        
        # Final cleanup
        manager.cleanup()
