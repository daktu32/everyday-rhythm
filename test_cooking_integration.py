#!/usr/bin/env python3
"""
お料理リズムデモ - 統合テスト

既存のゲームシステムと料理テーマの統合をテスト
"""

import pygame
import sys
import os

# プロジェクトのsrcディレクトリをパスに追加
sys.path.append('src')

from core.game_manager import GameManager
from cooking_theme import CookingTheme
from gameplay.note import Note

class CookingRhythmDemo:
    """料理リズムデモの統合テスト"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("お料理リズム - 統合テスト")
        self.clock = pygame.time.Clock()
        
        # 料理テーマの初期化
        self.cooking_theme = CookingTheme()
        
        # 音声システムの初期化
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # テスト用の音声読み込み
        self.load_cooking_sounds()
        
        # テスト用のノート
        self.test_notes = []
        self.create_test_notes()
        
        # ゲーム状態
        self.running = True
        self.judgment_line_y = 0
        self.last_judgment = None
        self.judgment_timer = 0
        
    def load_cooking_sounds(self):
        """料理テーマの音声を読み込み"""
        audio_path = "assets/cooking-theme/audio"
        
        try:
            self.sounds = {
                'perfect': pygame.mixer.Sound(f"{audio_path}/sfx/chop_perfect.wav"),
                'good': pygame.mixer.Sound(f"{audio_path}/sfx/chop_good.wav"),
                'miss': pygame.mixer.Sound(f"{audio_path}/sfx/miss_sound.wav"),
                'combo': pygame.mixer.Sound(f"{audio_path}/sfx/sizzle_combo.wav"),
                'ambient': pygame.mixer.Sound(f"{audio_path}/sfx/kitchen_ambient.wav")
            }
            
            # BGMの読み込み
            pygame.mixer.music.load(f"{audio_path}/bgm/cooking_bgm.wav")
            
            print("✅ 料理テーマ音声の読み込み完了")
            
        except Exception as e:
            print(f"❌ 音声読み込みエラー: {e}")
            self.sounds = {}
    
    def create_test_notes(self):
        """テスト用のノートを作成"""
        import time
        current_time = time.time()
        
        # 野菜の種類を循環させながらノートを作成
        vegetables = self.cooking_theme.vegetable_types
        
        for i in range(10):
            # 2秒間隔でノートを配置
            note_time = current_time + (i + 3) * 2.0
            
            # 野菜の種類を循環
            veg_name, veg_draw_func = vegetables[i % len(vegetables)]
            
            # テスト用のノートオブジェクト（簡易版）
            note = {
                'time': note_time,
                'vegetable': (veg_name, veg_draw_func),
                'x': 640,  # 画面中央
                'y': -50,  # 画面上部から開始
                'active': True
            }
            
            self.test_notes.append(note)
    
    def update_notes(self):
        """ノートの位置を更新"""
        import time
        current_time = time.time()
        
        for note in self.test_notes:
            if note['active']:
                # ノートが判定ラインに到達するまでの時間を計算
                time_to_judgment = note['time'] - current_time
                
                # 2秒前から表示開始
                if time_to_judgment <= 2.0:
                    # Y座標を時間に基づいて計算
                    progress = (2.0 - time_to_judgment) / 2.0
                    note['y'] = -50 + (self.judgment_line_y + 50) * progress
                
                # 判定ラインを通り過ぎたら非アクティブに
                if time_to_judgment < -1.0:
                    note['active'] = False
    
    def check_input(self):
        """入力チェックと判定"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            # スペースキーが押された時の判定
            import time
            current_time = time.time()
            
            # 最も近いアクティブなノートを探す
            closest_note = None
            min_distance = float('inf')
            
            for note in self.test_notes:
                if note['active']:
                    time_diff = abs(note['time'] - current_time)
                    if time_diff < min_distance and time_diff < 1.0:  # 1秒以内
                        min_distance = time_diff
                        closest_note = note
            
            if closest_note:
                # 判定を実行
                if min_distance <= 0.025:  # 25ms以内
                    self.last_judgment = "Perfect"
                    if 'perfect' in self.sounds:
                        self.sounds['perfect'].play()
                elif min_distance <= 0.05:  # 50ms以内
                    self.last_judgment = "Good"
                    if 'good' in self.sounds:
                        self.sounds['good'].play()
                else:
                    self.last_judgment = "Miss"
                    if 'miss' in self.sounds:
                        self.sounds['miss'].play()
                
                # ノートを非アクティブに
                closest_note['active'] = False
                self.judgment_timer = 60  # 1秒間表示
    
    def draw(self):
        """描画処理"""
        # キッチン背景を描画
        self.judgment_line_y = self.cooking_theme.background.draw_simple_kitchen(
            self.screen, 1280, 720
        )
        
        # アクティブなノートを描画
        for note in self.test_notes:
            if note['active'] and note['y'] > -50:
                veg_name, veg_draw_func = note['vegetable']
                veg_draw_func(self.screen, int(note['x']), int(note['y']), 30)
        
        # 判定結果を表示
        if self.judgment_timer > 0:
            self.cooking_theme.draw_judgment_text(
                self.screen, self.last_judgment, 640, 200
            )
            self.judgment_timer -= 1
        
        # UI情報を表示
        font = pygame.font.Font(None, 36)
        
        # 操作説明
        instructions = [
            "🎮 お料理リズム - 統合テスト",
            "スペースキー: 野菜を切る",
            "ESC: 終了",
            "",
            "🎵 BGM: M キー",
            "🔊 背景音: A キー"
        ]
        
        for i, text in enumerate(instructions):
            color = self.cooking_theme.colors.BLACK
            if text.startswith("🎮"):
                color = self.cooking_theme.colors.WARM_ORANGE
            
            text_surface = font.render(text, True, color)
            self.screen.blit(text_surface, (50, 50 + i * 40))
        
        # アクティブなノート数を表示
        active_notes = sum(1 for note in self.test_notes if note['active'])
        note_info = f"アクティブなノート: {active_notes}"
        note_surface = font.render(note_info, True, self.cooking_theme.colors.BLACK)
        self.screen.blit(note_surface, (50, 400))
    
    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_m:
                    # BGMの再生/停止
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        print("🎵 BGM停止")
                    else:
                        pygame.mixer.music.play(-1)  # ループ再生
                        print("🎵 BGM開始")
                elif event.key == pygame.K_a:
                    # 背景音の再生
                    if 'ambient' in self.sounds:
                        self.sounds['ambient'].play()
                        print("🔊 背景音再生")
                elif event.key == pygame.K_r:
                    # ノートをリセット
                    self.create_test_notes()
                    print("🔄 ノートリセット")
    
    def run(self):
        """メインループ"""
        print("🎮 お料理リズム統合テスト開始")
        print("操作方法:")
        print("  スペースキー: 野菜を切る")
        print("  M: BGM再生/停止")
        print("  A: 背景音再生")
        print("  R: ノートリセット")
        print("  ESC: 終了")
        
        while self.running:
            self.handle_events()
            self.check_input()
            self.update_notes()
            
            self.draw()
            self.cooking_theme.update()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        print("👋 テスト終了")

def main():
    """メイン関数"""
    try:
        demo = CookingRhythmDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\n⏹️  テストを中断しました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
