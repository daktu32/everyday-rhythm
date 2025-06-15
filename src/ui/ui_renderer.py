"""
UI Renderer Module

このモジュールは、Everyday Rhythmゲームの視覚的ユーザーインターフェースを
管理するUIRendererクラスを提供します。
"""

import pygame
import math
from typing import List, Dict, Tuple, Optional
from utils.config import Config
from gameplay.note import Note
from core.rhythm_engine import JudgmentResult


class UIRenderer:
    """UI描画とアニメーション管理クラス"""

    # 色彩定義
    COLORS = {
        'background': (20, 20, 30),       # ダークブルー背景
        'note': (255, 255, 255),          # 白ノート
        'judgment_line': (255, 215, 0),   # ゴールド判定ライン
        'perfect': (0, 255, 0),           # 緑Perfect
        'good': (255, 255, 0),            # 黄Good
        'miss': (255, 0, 0),              # 赤Miss
        'text': (255, 255, 255),          # 白テキスト
        'progress_bar': (100, 150, 255),  # 青プログレスバー
        'pause_overlay': (0, 0, 0, 128),  # 半透明黒
    }

    # レイアウト定数
    HEADER_HEIGHT = 60
    FOOTER_HEIGHT = 80
    JUDGMENT_LINE_Y = 500
    NOTE_RADIUS = 20
    JUDGMENT_LINE_WIDTH = 3
    
    # アニメーション定数
    FALL_DURATION = 2000.0  # ms - ノートが判定ラインに到達するまでの時間
    JUDGMENT_DISPLAY_TIME = 1000  # ms - 判定表示時間
    JUDGMENT_FADE_TIME = 500      # ms - 判定フェード時間

    def __init__(self, screen: pygame.Surface, config: Config):
        """UIRendererの初期化
        
        Args:
            screen: Pygameの描画サーフェス
            config: ゲーム設定オブジェクト
        """
        self.screen = screen
        self.config = config
        self.screen_width, self.screen_height = screen.get_size()
        
        # フォント初期化
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # アクティブな判定フィードバック
        self.active_judgments = []
        
        # フレーム管理
        self.last_frame_time = 0

    def clear_screen(self) -> None:
        """画面をクリア"""
        self.screen.fill(self.COLORS['background'])

    def calculate_note_position(self, note: Note, current_time: float) -> Tuple[int, int]:
        """ノートの現在位置を計算
        
        Args:
            note: ノートオブジェクト
            current_time: 現在時刻（ミリ秒）
            
        Returns:
            (x, y): ノートの画面座標
        """
        # ノート落下の進行度計算
        time_to_hit = note.hit_time - current_time
        progress = 1.0 - (time_to_hit / self.FALL_DURATION)
        
        # Y座標計算（上から下へ）
        start_y = self.HEADER_HEIGHT
        target_y = self.JUDGMENT_LINE_Y
        y = start_y + (target_y - start_y) * progress
        
        # X座標（画面中央固定）
        x = self.screen_width // 2
        
        return (int(x), int(y))

    def render_notes(self, notes: List[Note], current_time: float) -> None:
        """ノートの描画とアニメーション
        
        Args:
            notes: 描画するノートリスト
            current_time: 現在時刻（ミリ秒）
        """
        for note in notes:
            # ノート位置を計算
            x, y = self.calculate_note_position(note, current_time)
            
            # 画面内にあるノートのみ描画
            if -self.NOTE_RADIUS <= y <= self.screen_height + self.NOTE_RADIUS:
                # ノート本体（白い円）
                pygame.draw.circle(
                    self.screen,
                    self.COLORS['note'],
                    (x, y),
                    self.NOTE_RADIUS
                )
                
                # ノート輪郭（黒い縁）
                pygame.draw.circle(
                    self.screen,
                    (0, 0, 0),
                    (x, y),
                    self.NOTE_RADIUS,
                    2
                )

    def render_score(self, score: int, combo: int, multiplier: float) -> None:
        """スコア・コンボ表示
        
        Args:
            score: 現在のスコア
            combo: 現在のコンボ数
            multiplier: コンボ倍率
        """
        # スコア表示
        score_text = f"Score: {score:,}"
        score_surface = self.font.render(score_text, True, self.COLORS['text'])
        score_rect = score_surface.get_rect()
        score_rect.topright = (self.screen_width - 20, 10)
        self.screen.blit(score_surface, score_rect)
        
        # コンボ表示
        combo_text = f"Combo: {combo}x"
        combo_surface = self.font.render(combo_text, True, self.COLORS['text'])
        combo_rect = combo_surface.get_rect()
        combo_rect.topright = (self.screen_width - 20, 40)
        self.screen.blit(combo_surface, combo_rect)
        
        # 倍率表示（コンボが10以上の時）
        if combo >= 10:
            multiplier_text = f"Multiplier: {multiplier:.1f}x"
            multiplier_color = self.COLORS['good'] if multiplier > 1.0 else self.COLORS['text']
            multiplier_surface = self.font_small.render(multiplier_text, True, multiplier_color)
            multiplier_rect = multiplier_surface.get_rect()
            multiplier_rect.topright = (self.screen_width - 20, 70)
            self.screen.blit(multiplier_surface, multiplier_rect)

    def render_judgment(self, judgment_result: Optional[JudgmentResult]) -> None:
        """判定結果フィードバック
        
        Args:
            judgment_result: 判定結果オブジェクト
        """
        if judgment_result is None:
            return
            
        # 判定テキストと色を決定
        judgment_text = ""
        judgment_color = self.COLORS['text']
        
        if judgment_result.judgment == 'perfect':
            judgment_text = "Perfect!"
            judgment_color = self.COLORS['perfect']
        elif judgment_result.judgment == 'good':
            judgment_text = "Good!"
            judgment_color = self.COLORS['good']
        elif judgment_result.judgment == 'miss':
            judgment_text = "Miss!"
            judgment_color = self.COLORS['miss']
        
        # 判定テキスト描画
        judgment_surface = self.font_large.render(judgment_text, True, judgment_color)
        judgment_rect = judgment_surface.get_rect()
        judgment_rect.center = (self.screen_width // 2, self.JUDGMENT_LINE_Y - 60)
        self.screen.blit(judgment_surface, judgment_rect)
        
        # タイミング差表示
        timing_text = f"{judgment_result.timing_diff:+.0f}ms"
        timing_surface = self.font_small.render(timing_text, True, judgment_color)
        timing_rect = timing_surface.get_rect()
        timing_rect.center = (self.screen_width // 2, self.JUDGMENT_LINE_Y - 30)
        self.screen.blit(timing_surface, timing_rect)

    def render_game_info(self, music_name: str, progress: float) -> None:
        """ゲーム情報表示
        
        Args:
            music_name: 音楽名
            progress: 再生進行度（0.0-1.0）
        """
        # 音楽名表示
        music_surface = self.font.render(music_name, True, self.COLORS['text'])
        music_rect = music_surface.get_rect()
        music_rect.topleft = (20, 10)
        self.screen.blit(music_surface, music_rect)
        
        # プログレスバー描画
        progress_bar_width = 200
        progress_bar_height = 20
        progress_bar_x = 20
        progress_bar_y = self.screen_height - 60
        
        # プログレスバー背景
        progress_bg_rect = pygame.Rect(
            progress_bar_x, progress_bar_y,
            progress_bar_width, progress_bar_height
        )
        pygame.draw.rect(self.screen, (50, 50, 50), progress_bg_rect)
        pygame.draw.rect(self.screen, self.COLORS['text'], progress_bg_rect, 2)
        
        # プログレスバー進行度
        if progress > 0:
            progress_fill_width = int(progress_bar_width * min(progress, 1.0))
            progress_fill_rect = pygame.Rect(
                progress_bar_x, progress_bar_y,
                progress_fill_width, progress_bar_height
            )
            pygame.draw.rect(self.screen, self.COLORS['progress_bar'], progress_fill_rect)
        
        # 進行度テキスト
        progress_text = f"{progress * 100:.1f}%"
        progress_surface = self.font_small.render(progress_text, True, self.COLORS['text'])
        progress_rect = progress_surface.get_rect()
        progress_rect.topleft = (progress_bar_x + progress_bar_width + 10, progress_bar_y + 2)
        self.screen.blit(progress_surface, progress_rect)

    def render_judgment_line(self) -> None:
        """判定ライン描画"""
        pygame.draw.line(
            self.screen,
            self.COLORS['judgment_line'],
            (0, self.JUDGMENT_LINE_Y),
            (self.screen_width, self.JUDGMENT_LINE_Y),
            self.JUDGMENT_LINE_WIDTH
        )

    def render_pause_overlay(self) -> None:
        """一時停止画面描画"""
        # 半透明オーバーレイ
        overlay_surface = pygame.Surface((self.screen_width, self.screen_height))
        overlay_surface.set_alpha(128)
        overlay_surface.fill((0, 0, 0))
        self.screen.blit(overlay_surface, (0, 0))
        
        # "PAUSED"テキスト
        pause_text = "PAUSED"
        pause_surface = self.font_large.render(pause_text, True, self.COLORS['text'])
        pause_rect = pause_surface.get_rect()
        pause_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(pause_surface, pause_rect)
        
        # 操作説明
        instruction_text = "Press SPACE to resume"
        instruction_surface = self.font.render(instruction_text, True, self.COLORS['text'])
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.center = (self.screen_width // 2, self.screen_height // 2 + 50)
        self.screen.blit(instruction_surface, instruction_rect)

    def add_judgment_feedback(self, judgment_result: JudgmentResult) -> None:
        """判定フィードバックを追加
        
        Args:
            judgment_result: 判定結果オブジェクト
        """
        feedback = {
            'result': judgment_result,
            'start_time': pygame.time.get_ticks(),
            'position': (self.screen_width // 2, self.screen_height // 2)
        }
        self.active_judgments.append(feedback)

    def update(self, dt: float) -> None:
        """アニメーション更新
        
        Args:
            dt: デルタタイム（ミリ秒）
        """
        current_time = pygame.time.get_ticks()
        
        # 期限切れの判定フィードバックを削除
        self.active_judgments = [
            feedback for feedback in self.active_judgments
            if current_time - feedback['start_time'] < self.JUDGMENT_DISPLAY_TIME
        ]
        
        self.last_frame_time = current_time

    def render_active_judgments(self) -> None:
        """アクティブな判定フィードバックを描画"""
        current_time = pygame.time.get_ticks()
        
        for feedback in self.active_judgments:
            elapsed_time = current_time - feedback['start_time']
            
            # フェードアウト計算
            if elapsed_time > self.JUDGMENT_FADE_TIME:
                alpha = max(0, 255 - ((elapsed_time - self.JUDGMENT_FADE_TIME) / 
                                    (self.JUDGMENT_DISPLAY_TIME - self.JUDGMENT_FADE_TIME)) * 255)
            else:
                alpha = 255
            
            if alpha > 0:
                # 判定結果描画
                result = feedback['result']
                position = feedback['position']
                
                # 判定テキスト
                judgment_text = result.judgment.capitalize() + "!"
                judgment_color = self.COLORS.get(result.judgment, self.COLORS['text'])
                
                # アルファブレンディング用サーフェス作成
                text_surface = self.font_large.render(judgment_text, True, judgment_color)
                text_surface.set_alpha(int(alpha))
                
                text_rect = text_surface.get_rect()
                text_rect.center = position
                self.screen.blit(text_surface, text_rect)

    def render_frame(self, game_state: Dict) -> None:
        """1フレーム全体の描画
        
        Args:
            game_state: ゲーム状態辞書
        """
        # 背景クリア
        self.clear_screen()
        
        # 各要素を順序描画
        self.render_judgment_line()
        self.render_notes(game_state['notes'], game_state['current_time'])
        self.render_score(
            game_state['score'],
            game_state['combo'],
            game_state['multiplier']
        )
        
        # 最新の判定結果表示
        if game_state.get('last_judgment'):
            self.render_judgment(game_state['last_judgment'])
        
        # アクティブな判定フィードバック
        self.render_active_judgments()
        
        # ゲーム情報表示
        self.render_game_info(
            game_state['music_name'],
            game_state['progress']
        )
        
        # 一時停止状態の場合はオーバーレイ表示
        if game_state.get('paused', False):
            self.render_pause_overlay()
        
        # 画面更新
        pygame.display.flip()

    def render_background(self) -> None:
        """背景描画（将来の拡張用）"""
        # 現在は単色背景のみ
        # 将来的にはグラデーションやパターンを追加可能
        pass

    def get_note_visibility_range(self, current_time: float) -> Tuple[float, float]:
        """ノートの可視範囲を計算
        
        Args:
            current_time: 現在時刻
            
        Returns:
            (min_time, max_time): 可視範囲の時刻
        """
        # 画面上部から判定ライン下まで
        min_time = current_time
        max_time = current_time + self.FALL_DURATION
        return (min_time, max_time)

    def get_screen_info(self) -> Dict:
        """画面情報を取得
        
        Returns:
            画面情報辞書
        """
        return {
            'width': self.screen_width,
            'height': self.screen_height,
            'header_height': self.HEADER_HEIGHT,
            'footer_height': self.FOOTER_HEIGHT,
            'judgment_line_y': self.JUDGMENT_LINE_Y,
            'note_radius': self.NOTE_RADIUS,
            'colors': self.COLORS.copy()
        }