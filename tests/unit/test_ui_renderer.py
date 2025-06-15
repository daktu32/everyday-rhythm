"""
UIRenderer クラスのユニットテスト

このテストスイートは、UIRenderer クラスの動作を検証します。
TDD (Test-Driven Development) アプローチに従って作成されています。
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
import sys
import os

# テスト対象のモジュールをインポートパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.ui_renderer import UIRenderer
from utils.config import Config
from gameplay.note import Note
from core.rhythm_engine import JudgmentResult


class TestUIRenderer(unittest.TestCase):
    """UIRenderer クラスのテストケース"""

    def setUp(self):
        """各テストの前に実行される初期化処理"""
        # Pygame の初期化をモック
        with patch('pygame.init'), \
             patch('pygame.font.init'), \
             patch('pygame.font.Font'):
            
            # モックサーフェスを作成
            self.mock_screen = Mock(spec=pygame.Surface)
            self.mock_screen.get_size.return_value = (800, 600)
            self.mock_screen.fill = Mock()
            self.mock_screen.blit = Mock()
            
            # モック設定を作成
            self.mock_config = Mock(spec=Config)
            self.mock_config.SCREEN_WIDTH = 800
            self.mock_config.SCREEN_HEIGHT = 600
            self.mock_config.FPS = 60
            
            # UIRenderer を初期化
            self.ui_renderer = UIRenderer(self.mock_screen, self.mock_config)

    def test_init(self):
        """UIRenderer の初期化テスト"""
        # 初期化が正常に完了することを確認
        self.assertIsNotNone(self.ui_renderer)
        self.assertEqual(self.ui_renderer.screen, self.mock_screen)
        self.assertEqual(self.ui_renderer.config, self.mock_config)
        
        # 初期状態の確認
        self.assertEqual(len(self.ui_renderer.active_judgments), 0)
        self.assertEqual(self.ui_renderer.last_frame_time, 0)

    def test_clear_screen(self):
        """画面クリア機能のテスト"""
        # 画面をクリア
        self.ui_renderer.clear_screen()
        
        # 背景色で画面がクリアされることを確認
        expected_color = (20, 20, 30)  # ダークブルー背景
        self.mock_screen.fill.assert_called_once_with(expected_color)

    def test_calculate_note_position(self):
        """ノート位置計算のテスト"""
        # テスト用ノートを作成
        note = Note(hit_time=2000.0)  # 2秒後にヒット
        current_time = 0.0
        
        # ノート位置を計算
        x, y = self.ui_renderer.calculate_note_position(note, current_time)
        
        # 初期位置（画面上部）にあることを確認
        self.assertEqual(x, 400)  # 画面中央
        self.assertEqual(y, 60)   # 画面上部
        
        # 1秒後の位置を計算
        current_time = 1000.0
        x, y = self.ui_renderer.calculate_note_position(note, current_time)
        
        # 中間位置にあることを確認
        self.assertEqual(x, 400)
        self.assertGreater(y, 60)   # 初期位置より下
        self.assertLess(y, 500)     # 判定ラインより上
        
        # ヒット時刻の位置を計算
        current_time = 2000.0
        x, y = self.ui_renderer.calculate_note_position(note, current_time)
        
        # 判定ライン位置にあることを確認
        self.assertEqual(x, 400)
        self.assertEqual(y, 500)  # 判定ライン

    def test_render_notes_empty_list(self):
        """空のノートリストの描画テスト"""
        # 空のノートリストで描画
        self.ui_renderer.render_notes([], 0.0)
        
        # エラーが発生しないことを確認（例外なし）
        # 具体的な描画呼び出しは行われない

    def test_render_notes_single_note(self):
        """単一ノートの描画テスト"""
        # テスト用ノートを作成
        note = Note(hit_time=1000.0)
        notes = [note]
        current_time = 0.0
        
        with patch('pygame.draw.circle') as mock_draw_circle:
            # ノートを描画
            self.ui_renderer.render_notes(notes, current_time)
            
            # 円が描画されることを確認
            mock_draw_circle.assert_called_once()
            
            # 描画位置と色を確認
            args = mock_draw_circle.call_args
            surface, color, center, radius = args[0]
            
            self.assertEqual(surface, self.mock_screen)
            self.assertEqual(color, (255, 255, 255))  # 白色
            self.assertEqual(center, (400, 60))       # 初期位置
            self.assertEqual(radius, 20)              # ノートサイズ

    def test_render_notes_multiple_notes(self):
        """複数ノートの描画テスト"""
        # テスト用ノートを作成
        notes = [
            Note(hit_time=1000.0),
            Note(hit_time=2000.0),
            Note(hit_time=3000.0)
        ]
        current_time = 0.0
        
        with patch('pygame.draw.circle') as mock_draw_circle:
            # ノートを描画
            self.ui_renderer.render_notes(notes, current_time)
            
            # 3つの円が描画されることを確認
            self.assertEqual(mock_draw_circle.call_count, 3)

    def test_render_score_display(self):
        """スコア表示のテスト"""
        score = 12345
        combo = 25
        multiplier = 1.2
        
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # スコアを描画
            self.ui_renderer.render_score(score, combo, multiplier)
            
            # フォントレンダリングが呼び出されることを確認
            self.assertGreater(mock_font.render.call_count, 0)
            
            # 画面への描画が呼び出されることを確認
            self.assertGreater(self.mock_screen.blit.call_count, 0)

    def test_render_judgment_perfect(self):
        """Perfect判定の描画テスト"""
        # Perfect判定結果を作成
        judgment_result = JudgmentResult(
            judgment='perfect',
            timing_diff=15.0,
            score_gained=100,
            combo_multiplier=1.1
        )
        
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # 判定結果を描画
            self.ui_renderer.render_judgment(judgment_result)
            
            # フォントレンダリングが呼び出されることを確認
            mock_font.render.assert_called()
            
            # 緑色でPerfectが表示されることを確認
            call_args = mock_font.render.call_args_list
            text_calls = [call[0][0] for call in call_args]
            
            self.assertIn('Perfect!', text_calls)

    def test_render_judgment_good(self):
        """Good判定の描画テスト"""
        # Good判定結果を作成
        judgment_result = JudgmentResult(
            judgment='good',
            timing_diff=35.0,
            score_gained=50,
            combo_multiplier=1.0
        )
        
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # 判定結果を描画
            self.ui_renderer.render_judgment(judgment_result)
            
            # フォントレンダリングが呼び出されることを確認
            mock_font.render.assert_called()
            
            # 黄色でGoodが表示されることを確認
            call_args = mock_font.render.call_args_list
            text_calls = [call[0][0] for call in call_args]
            
            self.assertIn('Good!', text_calls)

    def test_render_judgment_miss(self):
        """Miss判定の描画テスト"""
        # Miss判定結果を作成
        judgment_result = JudgmentResult(
            judgment='miss',
            timing_diff=100.0,
            score_gained=0,
            combo_multiplier=1.0
        )
        
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # 判定結果を描画
            self.ui_renderer.render_judgment(judgment_result)
            
            # フォントレンダリングが呼び出されることを確認
            mock_font.render.assert_called()
            
            # 赤色でMissが表示されることを確認
            call_args = mock_font.render.call_args_list
            text_calls = [call[0][0] for call in call_args]
            
            self.assertIn('Miss!', text_calls)

    def test_render_game_info(self):
        """ゲーム情報表示のテスト"""
        music_name = "Test Song"
        progress = 0.5  # 50%進行
        
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # ゲーム情報を描画
            self.ui_renderer.render_game_info(music_name, progress)
            
            # 音楽名とプログレスバーが描画されることを確認
            self.assertGreater(mock_font.render.call_count, 0)
            self.assertGreater(self.mock_screen.blit.call_count, 0)

    def test_render_judgment_line(self):
        """判定ライン描画のテスト"""
        with patch('pygame.draw.line') as mock_draw_line:
            # 判定ラインを描画
            self.ui_renderer.render_judgment_line()
            
            # 線が描画されることを確認
            mock_draw_line.assert_called_once()
            
            # 描画パラメータを確認
            args = mock_draw_line.call_args[0]
            surface, color, start_pos, end_pos, width = args
            
            self.assertEqual(surface, self.mock_screen)
            self.assertEqual(color, (255, 215, 0))  # ゴールド色
            self.assertEqual(start_pos, (0, 500))   # 左端
            self.assertEqual(end_pos, (800, 500))   # 右端
            self.assertEqual(width, 3)              # 線の太さ

    def test_render_pause_overlay(self):
        """一時停止画面の描画テスト"""
        with patch.object(self.ui_renderer, 'font') as mock_font:
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # 一時停止画面を描画
            self.ui_renderer.render_pause_overlay()
            
            # 半透明オーバーレイと"PAUSED"テキストが描画されることを確認
            self.assertGreater(self.mock_screen.blit.call_count, 0)
            mock_font.render.assert_called()

    def test_add_judgment_feedback(self):
        """判定フィードバック追加のテスト"""
        # 判定結果を作成
        judgment_result = JudgmentResult(
            judgment='perfect',
            timing_diff=10.0,
            score_gained=100,
            combo_multiplier=1.1
        )
        
        # 初期状態では active_judgments が空
        self.assertEqual(len(self.ui_renderer.active_judgments), 0)
        
        with patch('pygame.time.get_ticks', return_value=1000):
            # 判定フィードバックを追加
            self.ui_renderer.add_judgment_feedback(judgment_result)
        
        # active_judgments に追加されることを確認
        self.assertEqual(len(self.ui_renderer.active_judgments), 1)
        
        # 追加されたフィードバックの内容を確認
        feedback = self.ui_renderer.active_judgments[0]
        self.assertEqual(feedback['result'], judgment_result)
        self.assertEqual(feedback['start_time'], 1000)
        self.assertEqual(feedback['position'], (400, 400))

    def test_update_judgment_fade(self):
        """判定フィードバックのフェードアウトテスト"""
        # 判定結果を追加
        judgment_result = JudgmentResult(
            judgment='perfect',
            timing_diff=10.0,
            score_gained=100,
            combo_multiplier=1.1
        )
        
        with patch('pygame.time.get_ticks', return_value=1000):
            self.ui_renderer.add_judgment_feedback(judgment_result)
        
        # 時間経過後のアップデート
        with patch('pygame.time.get_ticks', return_value=2500):  # 1.5秒後
            self.ui_renderer.update(16.67)  # 60FPS相当
        
        # フィードバックが自動的に削除されることを確認
        self.assertEqual(len(self.ui_renderer.active_judgments), 0)

    def test_render_frame_integration(self):
        """フレーム描画統合テスト"""
        # テスト用ゲーム状態を作成
        game_state = {
            'notes': [Note(hit_time=1000.0)],
            'current_time': 0.0,
            'score': 12345,
            'combo': 25,
            'multiplier': 1.2,
            'last_judgment': JudgmentResult('perfect', 10.0, 100, 1.1),
            'music_name': 'Test Song',
            'progress': 0.5,
            'paused': False
        }
        
        with patch.object(self.ui_renderer, 'font') as mock_font, \
             patch('pygame.draw.circle') as mock_draw_circle, \
             patch('pygame.draw.line') as mock_draw_line, \
             patch('pygame.display.flip') as mock_flip:
            
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # フレームを描画
            self.ui_renderer.render_frame(game_state)
            
            # 各要素が描画されることを確認
            self.mock_screen.fill.assert_called()           # 背景クリア
            mock_draw_circle.assert_called()                # ノート描画
            mock_draw_line.assert_called()                  # 判定ライン描画
            self.assertGreater(mock_font.render.call_count, 0)  # テキスト描画
            mock_flip.assert_called_once()                  # 画面更新

    def test_render_frame_with_pause(self):
        """一時停止状態でのフレーム描画テスト"""
        # 一時停止状態のゲーム状態を作成
        game_state = {
            'notes': [],
            'current_time': 0.0,
            'score': 0,
            'combo': 0,
            'multiplier': 1.0,
            'last_judgment': None,
            'music_name': 'Test Song',
            'progress': 0.0,
            'paused': True
        }
        
        with patch.object(self.ui_renderer, 'font') as mock_font, \
             patch('pygame.display.flip') as mock_flip:
            
            mock_surface = Mock()
            mock_font.render = Mock(return_value=mock_surface)
            
            # フレームを描画
            self.ui_renderer.render_frame(game_state)
            
            # 一時停止オーバーレイが描画されることを確認
            self.assertGreater(self.mock_screen.blit.call_count, 0)
            mock_flip.assert_called_once()


if __name__ == '__main__':
    unittest.main()
