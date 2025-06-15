"""
AudioAnalyzer - Audio analysis and feature extraction using librosa
"""
import os
import sys
import numpy as np
from typing import Dict, List, Any

# Add src to path for imports (must be before local imports)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Local imports after path setup
from utils.config import Config  # noqa: E402

try:
    import librosa
    import librosa.feature
    import librosa.beat
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    if Config.is_debug():
        print("Warning: librosa not available. Audio analysis features disabled.")


class AudioAnalyzer:
    """Analyzes audio files for tempo, beats, and other musical features"""
    
    def __init__(self):
        """Initialize the audio analyzer"""
        if not LIBROSA_AVAILABLE:
            if Config.is_debug():
                print("AudioAnalyzer initialized without librosa support")
        else:
            if Config.is_debug():
                print("AudioAnalyzer initialized with librosa support")
    
    def analyze_audio(self, file_path: str) -> Dict[str, Any]:
        """
        Comprehensive audio analysis
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Dictionary containing analysis results
        """
        if not LIBROSA_AVAILABLE:
            if Config.is_debug():
                print("Audio analysis not available - librosa not installed")
            return {}
        
        if not file_path or not os.path.exists(file_path):
            if Config.is_debug():
                print(f"Audio file not found: {file_path}")
            return {}
        
        try:
            # Load audio file
            y, sr = librosa.load(file_path)
            
            # Basic audio properties
            duration = len(y) / sr
            
            # Tempo and beat analysis
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Convert beat frames to time
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Audio features
            rms = librosa.feature.rms(y=y)
            zcr = librosa.feature.zero_crossing_rate(y)
            
            # Compile results
            analysis_result = {
                'tempo': float(tempo),
                'beats': beat_times.tolist(),
                'duration': float(duration),
                'sample_rate': int(sr),
                'rms_energy': float(np.mean(rms)),
                'zero_crossing_rate': float(np.mean(zcr)),
                'num_beats': len(beat_times)
            }
            
            if Config.is_debug():
                print(f"Audio analysis completed for {file_path}")
                print(f"  Tempo: {tempo:.1f} BPM")
                print(f"  Duration: {duration:.2f} seconds")
                print(f"  Beats detected: {len(beat_times)}")
            
            return analysis_result
            
        except Exception as e:
            if Config.is_debug():
                print(f"Error analyzing audio file {file_path}: {e}")
            return {}
    
    def get_tempo(self, file_path: str) -> float:
        """
        Extract tempo (BPM) from audio file
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tempo in beats per minute
        """
        if not LIBROSA_AVAILABLE:
            return 0.0
        
        if not file_path or not os.path.exists(file_path):
            return 0.0
        
        try:
            # Load audio file
            y, sr = librosa.load(file_path)
            
            # Extract tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            if Config.is_debug():
                print(f"Tempo detected: {tempo:.1f} BPM")
            
            return float(tempo)
            
        except Exception as e:
            if Config.is_debug():
                print(f"Error extracting tempo from {file_path}: {e}")
            return 0.0
    
    def get_beats(self, file_path: str) -> List[float]:
        """
        Extract beat times from audio file
        
        Args:
            file_path: Path to audio file
            
        Returns:
            List of beat times in seconds
        """
        if not LIBROSA_AVAILABLE:
            return []
        
        if not file_path or not os.path.exists(file_path):
            return []
        
        try:
            # Load audio file
            y, sr = librosa.load(file_path)
            
            # Extract beats
            _, beats = librosa.beat.beat_track(y=y, sr=sr)
            
            # Convert to time
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            if Config.is_debug():
                print(f"Beats detected: {len(beat_times)}")
            
            return beat_times.tolist()
            
        except Exception as e:
            if Config.is_debug():
                print(f"Error extracting beats from {file_path}: {e}")
            return []
    
    def get_audio_features(self, file_path: str) -> Dict[str, Any]:
        """
        Extract various audio features
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Dictionary of audio features
        """
        if not LIBROSA_AVAILABLE:
            return {}
        
        if not file_path or not os.path.exists(file_path):
            return {}
        
        try:
            # Load audio file
            y, sr = librosa.load(file_path)
            
            # Basic properties
            duration = len(y) / sr
            
            # Audio features
            rms = librosa.feature.rms(y=y)
            zcr = librosa.feature.zero_crossing_rate(y)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            
            features = {
                'duration': float(duration),
                'sample_rate': int(sr),
                'rms_energy': float(np.mean(rms)),
                'zero_crossing_rate': float(np.mean(zcr)),
                'spectral_centroid': float(np.mean(spectral_centroids))
            }
            
            if Config.is_debug():
                print(f"Audio features extracted for {file_path}")
            
            return features
            
        except Exception as e:
            if Config.is_debug():
                print(f"Error extracting features from {file_path}: {e}")
            return {}
    
    def is_available(self) -> bool:
        """Check if audio analysis is available"""
        return LIBROSA_AVAILABLE
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats"""
        if LIBROSA_AVAILABLE:
            return ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
        else:
            return []
