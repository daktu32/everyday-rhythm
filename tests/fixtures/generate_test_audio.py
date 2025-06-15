#!/usr/bin/env python3
"""
Generate test audio files for testing
"""
import numpy as np
import wave
import os


def generate_test_wav(filename: str, duration: float = 2.0, frequency: float = 440.0, sample_rate: int = 44100):
    """Generate a simple sine wave test audio file"""
    
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    print(f"Generated test audio: {filename}")


def main():
    """Generate test audio files"""
    fixtures_dir = os.path.dirname(__file__)
    
    # Generate different test files
    generate_test_wav(os.path.join(fixtures_dir, "test_short.wav"), duration=1.0, frequency=440.0)
    generate_test_wav(os.path.join(fixtures_dir, "test_medium.wav"), duration=3.0, frequency=880.0)
    generate_test_wav(os.path.join(fixtures_dir, "test_long.wav"), duration=5.0, frequency=220.0)
    
    print("Test audio files generated successfully!")


if __name__ == "__main__":
    main()
