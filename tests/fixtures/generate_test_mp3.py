#!/usr/bin/env python3
"""
Generate test MP3 files for testing
"""
import numpy as np
import wave
import os

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("pydub not available, cannot generate MP3 files")


def generate_test_mp3(filename: str, duration: float = 3.0, frequency: float = 440.0, sample_rate: int = 44100):
    """Generate a simple sine wave test MP3 file"""
    
    if not PYDUB_AVAILABLE:
        print("pydub is required to generate MP3 files")
        return False
    
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Create temporary WAV file
    temp_wav = filename.replace('.mp3', '_temp.wav')
    
    try:
        # Write WAV file first
        with wave.open(temp_wav, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wave_data.tobytes())
        
        # Convert WAV to MP3 using pydub
        audio = AudioSegment.from_wav(temp_wav)
        audio.export(filename, format="mp3", bitrate="128k")
        
        # Remove temporary WAV file
        os.remove(temp_wav)
        
        print(f"Generated test MP3: {filename}")
        return True
        
    except Exception as e:
        print(f"Error generating MP3 {filename}: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
        return False


def main():
    """Generate test MP3 files"""
    fixtures_dir = os.path.dirname(__file__)
    
    if not PYDUB_AVAILABLE:
        print("Installing pydub is required for MP3 support:")
        print("pip install pydub")
        return
    
    # Generate different test files
    success = True
    success &= generate_test_mp3(os.path.join(fixtures_dir, "test_short.mp3"), duration=1.0, frequency=440.0)
    success &= generate_test_mp3(os.path.join(fixtures_dir, "test_medium.mp3"), duration=3.0, frequency=880.0)
    success &= generate_test_mp3(os.path.join(fixtures_dir, "test_long.mp3"), duration=5.0, frequency=220.0)
    
    if success:
        print("Test MP3 files generated successfully!")
    else:
        print("Some MP3 files failed to generate")


if __name__ == "__main__":
    main()
