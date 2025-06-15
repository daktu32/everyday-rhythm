"""
Unit tests for AudioAnalyzer class
"""
import pytest
import os
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from audio.audio_analyzer import AudioAnalyzer


class TestAudioAnalyzer:
    """Test cases for AudioAnalyzer class"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        # Path to test audio files
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
        self.test_audio_short = os.path.join(self.fixtures_dir, 'test_short.wav')
        self.test_audio_medium = os.path.join(self.fixtures_dir, 'test_medium.wav')
        self.invalid_audio = os.path.join(self.fixtures_dir, 'nonexistent.wav')
    
    def test_audio_analyzer_initialization(self):
        """Test AudioAnalyzer initializes correctly"""
        # Act
        analyzer = AudioAnalyzer()
        
        # Assert
        assert analyzer is not None
    
    @patch('librosa.load')
    def test_analyze_audio_valid_file(self, mock_load):
        """Test analyzing valid audio file"""
        # Arrange
        mock_y = np.array([0.1, 0.2, 0.3, 0.4])
        mock_sr = 22050
        mock_load.return_value = (mock_y, mock_sr)
        
        analyzer = AudioAnalyzer()
        
        # Act
        result = analyzer.analyze_audio(self.test_audio_short)
        
        # Assert
        assert isinstance(result, dict)
        assert 'tempo' in result
        assert 'beats' in result
        assert 'duration' in result
        assert 'sample_rate' in result
        mock_load.assert_called_once_with(self.test_audio_short)
    
    def test_analyze_audio_invalid_file(self):
        """Test analyzing invalid audio file"""
        # Arrange
        analyzer = AudioAnalyzer()
        
        # Act
        result = analyzer.analyze_audio(self.invalid_audio)
        
        # Assert
        assert result == {}
    
    def test_analyze_audio_empty_path(self):
        """Test analyzing with empty file path"""
        # Arrange
        analyzer = AudioAnalyzer()
        
        # Act
        result = analyzer.analyze_audio("")
        
        # Assert
        assert result == {}
    
    @patch('librosa.load')
    @patch('librosa.beat.beat_track')
    def test_get_tempo(self, mock_beat_track, mock_load):
        """Test tempo detection"""
        # Arrange
        mock_y = np.array([0.1, 0.2, 0.3, 0.4])
        mock_sr = 22050
        mock_load.return_value = (mock_y, mock_sr)
        mock_beat_track.return_value = (120.0, np.array([0, 1, 2]))
        
        analyzer = AudioAnalyzer()
        
        # Act
        tempo = analyzer.get_tempo(self.test_audio_short)
        
        # Assert
        assert tempo == 120.0
        mock_load.assert_called_once_with(self.test_audio_short)
        mock_beat_track.assert_called_once()
    
    @patch('librosa.load')
    @patch('librosa.beat.beat_track')
    @patch('librosa.frames_to_time')
    def test_get_beats(self, mock_frames_to_time, mock_beat_track, mock_load):
        """Test beat detection"""
        # Arrange
        mock_y = np.array([0.1, 0.2, 0.3, 0.4])
        mock_sr = 22050
        mock_load.return_value = (mock_y, mock_sr)
        mock_beats = np.array([0, 1, 2, 3])
        mock_beat_track.return_value = (120.0, mock_beats)
        mock_beat_times = np.array([0.5, 1.0, 1.5, 2.0])
        mock_frames_to_time.return_value = mock_beat_times
        
        analyzer = AudioAnalyzer()
        
        # Act
        beats = analyzer.get_beats(self.test_audio_short)
        
        # Assert
        assert isinstance(beats, list)
        assert len(beats) == 4
        assert beats == [0.5, 1.0, 1.5, 2.0]
        mock_load.assert_called_once_with(self.test_audio_short)
        mock_beat_track.assert_called_once()
        mock_frames_to_time.assert_called_once_with(mock_beats, sr=mock_sr)
    
    @patch('librosa.load')
    def test_get_audio_features(self, mock_load):
        """Test audio feature extraction"""
        # Arrange
        mock_y = np.array([0.1, 0.2, 0.3, 0.4])
        mock_sr = 22050
        mock_load.return_value = (mock_y, mock_sr)
        
        analyzer = AudioAnalyzer()
        
        # Act
        features = analyzer.get_audio_features(self.test_audio_short)
        
        # Assert
        assert isinstance(features, dict)
        assert 'duration' in features
        assert 'sample_rate' in features
        assert 'rms_energy' in features
        assert 'zero_crossing_rate' in features
        mock_load.assert_called_once_with(self.test_audio_short)
    
    @patch('librosa.load')
    def test_librosa_error_handling(self, mock_load):
        """Test handling of librosa errors"""
        # Arrange
        mock_load.side_effect = Exception("Test librosa error")
        analyzer = AudioAnalyzer()
        
        # Act
        result = analyzer.analyze_audio(self.test_audio_short)
        
        # Assert
        assert result == {}
    
    @patch('librosa.load')
    def test_get_tempo_error_handling(self, mock_load):
        """Test tempo detection error handling"""
        # Arrange
        mock_load.side_effect = Exception("Test error")
        analyzer = AudioAnalyzer()
        
        # Act
        tempo = analyzer.get_tempo(self.test_audio_short)
        
        # Assert
        assert tempo == 0.0
    
    @patch('librosa.load')
    def test_get_beats_error_handling(self, mock_load):
        """Test beat detection error handling"""
        # Arrange
        mock_load.side_effect = Exception("Test error")
        analyzer = AudioAnalyzer()
        
        # Act
        beats = analyzer.get_beats(self.test_audio_short)
        
        # Assert
        assert beats == []
    
    @patch('librosa.load')
    def test_get_audio_features_error_handling(self, mock_load):
        """Test audio features error handling"""
        # Arrange
        mock_load.side_effect = Exception("Test error")
        analyzer = AudioAnalyzer()
        
        # Act
        features = analyzer.get_audio_features(self.test_audio_short)
        
        # Assert
        assert features == {}
    
    @patch('librosa.load')
    @patch('librosa.beat.beat_track')
    @patch('librosa.feature.rms')
    @patch('librosa.feature.zero_crossing_rate')
    def test_comprehensive_analysis(self, mock_zcr, mock_rms, mock_beat_track, mock_load):
        """Test comprehensive audio analysis"""
        # Arrange
        mock_y = np.array([0.1, 0.2, 0.3, 0.4])
        mock_sr = 22050
        mock_load.return_value = (mock_y, mock_sr)
        mock_beat_track.return_value = (120.0, np.array([0.5, 1.0, 1.5]))
        mock_rms.return_value = np.array([[0.2]])
        mock_zcr.return_value = np.array([[0.1]])
        
        analyzer = AudioAnalyzer()
        
        # Act
        result = analyzer.analyze_audio(self.test_audio_short)
        
        # Assert
        assert 'tempo' in result
        assert 'beats' in result
        assert 'duration' in result
        assert 'sample_rate' in result
        assert result['tempo'] == 120.0
        assert len(result['beats']) == 3
        assert result['sample_rate'] == 22050
        
        # Verify all librosa functions were called
        mock_load.assert_called_once()
        mock_beat_track.assert_called_once()
        mock_rms.assert_called_once()
        mock_zcr.assert_called_once()
