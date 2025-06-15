#!/usr/bin/env python3
"""
お料理リズムデモ用のビジュアル素材とテーマ設定

自作のカラーパレットと描画関数で著作権フリーのビジュアルを提供
"""

import pygame
import math
import random

# お料理テーマカラーパレット
class CookingColors:
    # メインカラー
    WARM_ORANGE = (255, 140, 66)
    CREAM = (255, 248, 220)
    BROWN = (139, 69, 19)
    
    # 野菜カラー
    CARROT_ORANGE = (255, 165, 0)
    ONION_PURPLE = (221, 160, 221)
    TOMATO_RED = (255, 99, 71)
    LETTUCE_GREEN = (50, 205, 50)
    POTATO_BEIGE = (245, 222, 179)
    
    # UI カラー
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (211, 211, 211)
    
    # エフェクトカラー
    PERFECT_GOLD = (255, 215, 0)
    GOOD_SILVER = (192, 192, 192)
    MISS_RED = (220, 20, 60)

class VegetableIcons:
    """野菜アイコンの描画関数集"""
    
    @staticmethod
    def draw_carrot(surface, x, y, size):
        """人参アイコンを描画"""
        # 人参本体（三角形）
        points = [
            (x, y - size),
            (x - size//3, y + size),
            (x + size//3, y + size)
        ]
        pygame.draw.polygon(surface, CookingColors.CARROT_ORANGE, points)
        pygame.draw.polygon(surface, CookingColors.BROWN, points, 2)
        
        # 葉っぱ部分
        leaf_rect = pygame.Rect(x - size//4, y - size - size//3, size//2, size//3)
        pygame.draw.rect(surface, CookingColors.LETTUCE_GREEN, leaf_rect)
    
    @staticmethod
    def draw_onion(surface, x, y, size):
        """玉ねぎアイコンを描画"""
        # 玉ねぎ本体（円）
        pygame.draw.circle(surface, CookingColors.ONION_PURPLE, (x, y), size)
        pygame.draw.circle(surface, CookingColors.BROWN, (x, y), size, 2)
        
        # 層を表現する線
        for i in range(1, 4):
            radius = size - i * (size // 5)
            if radius > 0:
                pygame.draw.circle(surface, CookingColors.WHITE, (x, y), radius, 1)
    
    @staticmethod
    def draw_tomato(surface, x, y, size):
        """トマトアイコンを描画"""
        # トマト本体（円）
        pygame.draw.circle(surface, CookingColors.TOMATO_RED, (x, y), size)
        pygame.draw.circle(surface, CookingColors.BROWN, (x, y), size, 2)
        
        # ヘタ部分
        heta_points = [
            (x - size//3, y - size),
            (x, y - size - size//4),
            (x + size//3, y - size)
        ]
        pygame.draw.polygon(surface, CookingColors.LETTUCE_GREEN, heta_points)
    
    @staticmethod
    def draw_lettuce(surface, x, y, size):
        """レタスアイコンを描画"""
        # レタス本体（楕円）
        rect = pygame.Rect(x - size, y - size//2, size*2, size)
        pygame.draw.ellipse(surface, CookingColors.LETTUCE_GREEN, rect)
        pygame.draw.ellipse(surface, CookingColors.BROWN, rect, 2)
        
        # 葉脈
        pygame.draw.line(surface, CookingColors.WHITE, 
                        (x - size//2, y), (x + size//2, y), 1)
    
    @staticmethod
    def draw_potato(surface, x, y, size):
        """じゃがいもアイコンを描画"""
        # じゃがいも本体（楕円）
        rect = pygame.Rect(x - size, y - size//2, size*2, size)
        pygame.draw.ellipse(surface, CookingColors.POTATO_BEIGE, rect)
        pygame.draw.ellipse(surface, CookingColors.BROWN, rect, 2)
        
        # 芽の部分（小さな円）
        for i in range(3):
            spot_x = x + random.randint(-size//2, size//2)
            spot_y = y + random.randint(-size//4, size//4)
            pygame.draw.circle(surface, CookingColors.BROWN, (spot_x, spot_y), 2)

class KitchenBackground:
    """キッチン背景の描画"""
    
    @staticmethod
    def draw_simple_kitchen(surface, width, height):
        """シンプルなキッチン背景を描画"""
        # 背景色
        surface.fill(CookingColors.CREAM)
        
        # カウンター
        counter_height = height // 4
        counter_rect = pygame.Rect(0, height - counter_height, width, counter_height)
        pygame.draw.rect(surface, CookingColors.BROWN, counter_rect)
        
        # まな板（判定ライン）
        board_width = width // 3
        board_height = 20
        board_x = (width - board_width) // 2
        board_y = height - counter_height - 100
        board_rect = pygame.Rect(board_x, board_y, board_width, board_height)
        pygame.draw.rect(surface, CookingColors.POTATO_BEIGE, board_rect)
        pygame.draw.rect(surface, CookingColors.BROWN, board_rect, 3)
        
        return board_y  # 判定ラインのY座標を返す

class CookingEffects:
    """料理テーマのエフェクト"""
    
    @staticmethod
    def draw_sparkle(surface, x, y, size, color):
        """キラキラエフェクト"""
        # 十字の光
        pygame.draw.line(surface, color, (x - size, y), (x + size, y), 3)
        pygame.draw.line(surface, color, (x, y - size), (x, y + size), 3)
        
        # 斜めの光
        offset = size // 2
        pygame.draw.line(surface, color, 
                        (x - offset, y - offset), (x + offset, y + offset), 2)
        pygame.draw.line(surface, color, 
                        (x - offset, y + offset), (x + offset, y - offset), 2)
    
    @staticmethod
    def draw_steam(surface, x, y, frame_count):
        """湯気エフェクト"""
        # 湯気の粒子を描画
        for i in range(5):
            offset_x = math.sin((frame_count + i * 20) * 0.1) * 10
            offset_y = i * 15
            steam_x = x + offset_x
            steam_y = y - offset_y - (frame_count % 100)
            
            alpha = max(0, 255 - i * 50)
            if alpha > 0:
                steam_surface = pygame.Surface((6, 6))
                steam_surface.set_alpha(alpha)
                steam_surface.fill(CookingColors.WHITE)
                surface.blit(steam_surface, (steam_x - 3, steam_y - 3))

class CookingTheme:
    """料理テーマの統合クラス"""
    
    def __init__(self):
        self.colors = CookingColors()
        self.vegetables = VegetableIcons()
        self.background = KitchenBackground()
        self.effects = CookingEffects()
        self.frame_count = 0
        
        # 野菜の種類リスト
        self.vegetable_types = [
            ('carrot', self.vegetables.draw_carrot),
            ('onion', self.vegetables.draw_onion),
            ('tomato', self.vegetables.draw_tomato),
            ('lettuce', self.vegetables.draw_lettuce),
            ('potato', self.vegetables.draw_potato)
        ]
    
    def get_random_vegetable(self):
        """ランダムな野菜タイプを取得"""
        return random.choice(self.vegetable_types)
    
    def update(self):
        """フレーム更新"""
        self.frame_count += 1
    
    def draw_judgment_text(self, surface, judgment, x, y):
        """判定テキストを描画"""
        font = pygame.font.Font(None, 48)
        
        if judgment == "Perfect":
            text = font.render("美味しそう！", True, CookingColors.PERFECT_GOLD)
            self.effects.draw_sparkle(surface, x, y - 30, 15, CookingColors.PERFECT_GOLD)
        elif judgment == "Good":
            text = font.render("いい感じ♪", True, CookingColors.GOOD_SILVER)
        elif judgment == "Miss":
            text = font.render("あちゃー", True, CookingColors.MISS_RED)
        else:
            return
        
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

# 使用例とテスト用の関数
def test_cooking_theme():
    """料理テーマのテスト表示"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("お料理リズム - テーマテスト")
    clock = pygame.time.Clock()
    
    theme = CookingTheme()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 背景描画
        judgment_line_y = theme.background.draw_simple_kitchen(screen, 800, 600)
        
        # 野菜アイコンのテスト表示
        vegetables = [
            (theme.vegetables.draw_carrot, 150, 200),
            (theme.vegetables.draw_onion, 250, 200),
            (theme.vegetables.draw_tomato, 350, 200),
            (theme.vegetables.draw_lettuce, 450, 200),
            (theme.vegetables.draw_potato, 550, 200)
        ]
        
        for draw_func, x, y in vegetables:
            draw_func(screen, x, y, 30)
        
        # エフェクトテスト
        theme.effects.draw_steam(screen, 400, 500, theme.frame_count)
        theme.draw_judgment_text(screen, "Perfect", 400, 100)
        
        theme.update()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_cooking_theme()
