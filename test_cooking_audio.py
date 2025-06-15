#!/usr/bin/env python3
"""
お料理リズムデモ用音声素材のテストスクリプト
"""

import pygame
import os
import time

def test_cooking_audio():
    """料理テーマの音声素材をテスト"""
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    audio_path = "assets/cooking-theme/audio"
    
    # テスト対象の音声ファイル
    test_sounds = [
        ("BGM", f"{audio_path}/bgm/cooking_bgm.wav"),
        ("Perfect判定音", f"{audio_path}/sfx/chop_perfect.wav"),
        ("Good判定音", f"{audio_path}/sfx/chop_good.wav"),
        ("Miss判定音", f"{audio_path}/sfx/miss_sound.wav"),
        ("コンボ音", f"{audio_path}/sfx/sizzle_combo.wav"),
        ("背景音", f"{audio_path}/sfx/kitchen_ambient.wav")
    ]
    
    print("🎵 お料理リズム - 音声素材テスト")
    print("=" * 40)
    
    for name, filepath in test_sounds:
        if os.path.exists(filepath):
            print(f"\n▶️  {name} をテスト中...")
            print(f"   ファイル: {os.path.basename(filepath)}")
            
            try:
                # 音声ファイルを読み込み
                sound = pygame.mixer.Sound(filepath)
                
                # ファイル情報を表示
                file_size = os.path.getsize(filepath)
                print(f"   サイズ: {file_size:,} bytes ({file_size/1024:.1f} KB)")
                
                # 音声を再生
                sound.play()
                
                # BGMの場合は長めに再生
                if "bgm" in filepath:
                    print("   🎼 BGMを10秒間再生します...")
                    time.sleep(10)
                    sound.stop()
                else:
                    print("   🔊 効果音を再生中...")
                    # 音声の長さを待つ
                    while pygame.mixer.get_busy():
                        time.sleep(0.1)
                
                print("   ✅ 再生完了")
                
            except Exception as e:
                print(f"   ❌ エラー: {e}")
        else:
            print(f"\n❌ {name}: ファイルが見つかりません")
            print(f"   パス: {filepath}")
    
    print("\n" + "=" * 40)
    print("🎵 音声テスト完了")
    
    # 対話的テスト
    print("\n🎮 対話的テスト（Enterキーで各音を再生）")
    print("終了するには 'q' を入力してください")
    
    # 効果音のみを対話的にテスト
    interactive_sounds = {
        '1': ("Perfect判定音", f"{audio_path}/sfx/chop_perfect.wav"),
        '2': ("Good判定音", f"{audio_path}/sfx/chop_good.wav"),
        '3': ("Miss判定音", f"{audio_path}/sfx/miss_sound.wav"),
        '4': ("コンボ音", f"{audio_path}/sfx/sizzle_combo.wav"),
        '5': ("背景音", f"{audio_path}/sfx/kitchen_ambient.wav")
    }
    
    while True:
        print("\n選択してください:")
        for key, (name, _) in interactive_sounds.items():
            print(f"  {key}: {name}")
        print("  q: 終了")
        
        choice = input("\n> ").strip().lower()
        
        if choice == 'q':
            break
        elif choice in interactive_sounds:
            name, filepath = interactive_sounds[choice]
            if os.path.exists(filepath):
                print(f"🔊 {name} を再生中...")
                sound = pygame.mixer.Sound(filepath)
                sound.play()
                while pygame.mixer.get_busy():
                    time.sleep(0.1)
            else:
                print(f"❌ ファイルが見つかりません: {filepath}")
        else:
            print("❌ 無効な選択です")
    
    pygame.mixer.quit()
    print("\n👋 テスト終了")

if __name__ == "__main__":
    try:
        test_cooking_audio()
    except KeyboardInterrupt:
        print("\n\n⏹️  テストを中断しました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("Pygameがインストールされていることを確認してください:")
