#!/usr/bin/env python3
"""
お料理リズムデモ用の音声素材生成スクリプト

著作権フリーの音声を生成するため、数学的に音を合成します。
"""

import numpy as np
import wave
import os

def generate_tone(frequency, duration, sample_rate=44100, amplitude=0.3):
    """指定した周波数の音を生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def generate_chord(frequencies, duration, sample_rate=44100, amplitude=0.2):
    """和音を生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.zeros_like(t)
    for freq in frequencies:
        wave_data += amplitude * np.sin(2 * np.pi * freq * t)
    return wave_data / len(frequencies)

def add_envelope(wave_data, attack=0.1, decay=0.1, sustain=0.7, release=0.2):
    """ADSR エンベロープを適用"""
    length = len(wave_data)
    envelope = np.ones(length)
    
    # Attack
    attack_samples = int(length * attack)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    decay_samples = int(length * decay)
    decay_end = attack_samples + decay_samples
    envelope[attack_samples:decay_end] = np.linspace(1, sustain, decay_samples)
    
    # Release
    release_samples = int(length * release)
    release_start = length - release_samples
    envelope[release_start:] = np.linspace(sustain, 0, release_samples)
    
    return wave_data * envelope

def save_wav(wave_data, filename, sample_rate=44100):
    """WAVファイルとして保存"""
    # 16-bit PCMに変換
    wave_data_int = (wave_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # モノラル
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data_int.tobytes())

def create_cooking_sounds():
    """料理テーマの効果音を生成"""
    base_path = "assets/cooking-theme/audio/sfx"
    
    # Perfect判定音 - 明るい和音
    perfect_chord = generate_chord([523, 659, 784], 0.3)  # C-E-G
    perfect_sound = add_envelope(perfect_chord, attack=0.05, release=0.4)
    save_wav(perfect_sound, f"{base_path}/chop_perfect.wav")
    
    # Good判定音 - 単音
    good_tone = generate_tone(523, 0.2)  # C
    good_sound = add_envelope(good_tone, attack=0.05, release=0.3)
    save_wav(good_sound, f"{base_path}/chop_good.wav")
    
    # Miss判定音 - 低い音
    miss_tone = generate_tone(220, 0.4)  # A
    miss_sound = add_envelope(miss_tone, attack=0.1, decay=0.3, sustain=0.3, release=0.3)
    save_wav(miss_sound, f"{base_path}/miss_sound.wav")
    
    # コンボ音 - 上昇音階
    combo_freqs = [523, 587, 659, 698, 784]  # C-D-E-F-G
    combo_data = np.array([])
    for freq in combo_freqs:
        tone = generate_tone(freq, 0.1)
        tone = add_envelope(tone, attack=0.02, release=0.08)
        combo_data = np.concatenate([combo_data, tone])
    save_wav(combo_data, f"{base_path}/sizzle_combo.wav")
    
    # 背景音 - 低周波のアンビエント
    ambient_freqs = [110, 165, 220]  # 低い和音
    ambient_chord = generate_chord(ambient_freqs, 2.0, amplitude=0.1)
    ambient_sound = add_envelope(ambient_chord, attack=0.5, decay=0.5, sustain=0.8, release=0.5)
    save_wav(ambient_sound, f"{base_path}/kitchen_ambient.wav")

def create_simple_bgm():
    """シンプルなBGMを生成"""
    base_path = "assets/cooking-theme/audio/bgm"
    
    # 料理テーマのメロディー（C major scale）
    melody_notes = [
        (523, 0.5), (587, 0.5), (659, 0.5), (698, 0.5),  # C-D-E-F
        (784, 1.0), (698, 0.5), (659, 0.5),              # G-F-E
        (587, 0.5), (523, 1.0)                           # D-C
    ]
    
    bgm_data = np.array([])
    for freq, duration in melody_notes:
        tone = generate_tone(freq, duration, amplitude=0.2)
        tone = add_envelope(tone, attack=0.1, release=0.2)
        bgm_data = np.concatenate([bgm_data, tone])
    
    # ループ用に3回繰り返し
    full_bgm = np.tile(bgm_data, 3)
    save_wav(full_bgm, f"{base_path}/cooking_bgm.wav")

if __name__ == "__main__":
    print("お料理リズムデモ用音声素材を生成中...")
    
    # ディレクトリが存在することを確認
    os.makedirs("assets/cooking-theme/audio/sfx", exist_ok=True)
    os.makedirs("assets/cooking-theme/audio/bgm", exist_ok=True)
    
    try:
        create_cooking_sounds()
        create_simple_bgm()
        print("✅ 音声素材の生成が完了しました！")
        print("\n生成された素材:")
        print("- chop_perfect.wav (Perfect判定音)")
        print("- chop_good.wav (Good判定音)")
        print("- miss_sound.wav (Miss判定音)")
        print("- sizzle_combo.wav (コンボ音)")
        print("- kitchen_ambient.wav (背景音)")
        print("- cooking_bgm.wav (BGM)")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        print("numpy がインストールされていることを確認してください:")
        print("pip install numpy")
