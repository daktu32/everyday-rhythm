# F-04: UI Renderer Specification

## 概要

UI Rendererは、Everyday Rhythmゲームの視覚的ユーザーインターフェースを管理するコンポーネントです。ノートの表示とアニメーション、スコア表示、判定フィードバック、ゲーム画面全体のレイアウトを担当します。

## 要求事項

### 機能要求

#### 1. ノート表示・アニメーション
- **ノート描画**: 円形のノートを画面上に描画
- **移動アニメーション**: 上から下への滑らかな移動（60FPS）
- **判定ライン**: 画面下部に判定ラインを表示
- **ノート到達**: 判定ラインとノートの位置同期

#### 2. スコア表示
- **現在スコア**: リアルタイムスコア表示
- **コンボ表示**: 現在のコンボ数表示
- **コンボ倍率**: 倍率インジケーター（1.0x, 1.1x, 1.2x）
- **最高スコア**: セッション最高スコア記録

#### 3. 判定フィードバック
- **判定結果表示**: Perfect/Good/Miss の視覚フィードバック
- **タイミング差表示**: 判定タイミングのずれ表示（±ms）
- **判定エフェクト**: 判定結果に応じたビジュアルエフェクト
- **フェードアウト**: 判定表示の自然な消失

#### 4. ゲーム状態表示
- **音楽情報**: 現在再生中の音楽名表示
- **進行度**: 音楽の再生進行度バー
- **一時停止状態**: ゲーム一時停止時の画面表示

### 非機能要求

#### パフォーマンス
- **フレームレート**: 安定した60FPS描画
- **レスポンス**: 判定フィードバック遅延 < 50ms
- **メモリ効率**: ノートオブジェクトの効率的管理

#### 視覚品質
- **解像度**: 800x600基本解像度対応
- **色彩**: 高コントラスト・視認性重視
- **アニメーション**: 滑らかな補間処理

## 技術仕様

### クラス設計

#### UIRenderer
```python
class UIRenderer:
    """UI描画とアニメーション管理"""
    
    def __init__(self, screen: pygame.Surface, config: Config):
        """初期化"""
        
    def render_notes(self, notes: List[Note], current_time: float) -> None:
        """ノート描画・アニメーション"""
        
    def render_score(self, score: int, combo: int, multiplier: float) -> None:
        """スコア・コンボ表示"""
        
    def render_judgment(self, judgment_result: JudgmentResult) -> None:
        """判定結果フィードバック"""
        
    def render_game_info(self, music_name: str, progress: float) -> None:
        """ゲーム情報表示"""
        
    def render_pause_overlay(self) -> None:
        """一時停止画面"""
        
    def update(self, dt: float) -> None:
        """アニメーション更新"""
        
    def clear_screen(self) -> None:
        """画面クリア"""
```

### 画面レイアウト

#### 座標系
```
800x600 画面
┌─────────────────────────────────────┐
│ 音楽名            スコア: 12345    │ ← ヘッダー (0, 0-60)
│                  コンボ: 25x      │
├─────────────────────────────────────┤
│                                   │
│          ノート落下エリア            │ ← メイン (0, 60-500)
│                                   │
│             ○ ○ ○                │
│               ↓                   │
├═════════════════════════════════════┤
│            判定ライン               │ ← 判定 (0, 500-520)
├─────────────────────────────────────┤
│ Perfect! +15ms    進行度: ████▒▒  │ ← フッター (0, 520-600)
└─────────────────────────────────────┘
```

#### 色彩設計
```python
COLORS = {
    'background': (20, 20, 30),       # ダークブルー背景
    'note': (255, 255, 255),          # 白ノート
    'judgment_line': (255, 215, 0),   # ゴールド判定ライン
    'perfect': (0, 255, 0),           # 緑Perfect
    'good': (255, 255, 0),            # 黄Good
    'miss': (255, 0, 0),              # 赤Miss
    'text': (255, 255, 255),          # 白テキスト
    'progress_bar': (100, 150, 255),  # 青プログレスバー
}
```

### アニメーション仕様

#### ノート移動
```python
# ノート移動計算
def calculate_note_position(note: Note, current_time: float) -> Tuple[int, int]:
    # 落下時間: 2秒で判定ラインに到達
    fall_duration = 2000.0  # ms
    start_y = 60
    target_y = 500
    
    time_to_hit = note.hit_time - current_time
    progress = 1.0 - (time_to_hit / fall_duration)
    
    y = start_y + (target_y - start_y) * progress
    x = 400  # 画面中央
    
    return (int(x), int(y))
```

#### 判定フィードバック
```python
# 判定表示時間とフェード
JUDGMENT_DISPLAY_TIME = 1000  # ms
JUDGMENT_FADE_TIME = 500      # ms

def render_judgment_with_fade(judgment: str, display_time: float):
    alpha = min(255, max(0, 255 - (display_time / JUDGMENT_FADE_TIME) * 255))
    # アルファブレンディング適用
```

## API設計

### 主要メソッド

#### render_frame()
```python
def render_frame(self, game_state: dict) -> None:
    """1フレーム全体の描画"""
    self.clear_screen()
    
    # 各要素を順序描画
    self.render_background()
    self.render_notes(game_state['notes'], game_state['current_time'])
    self.render_judgment_line()
    self.render_score(game_state['score'], game_state['combo'], game_state['multiplier'])
    self.render_judgment(game_state['last_judgment'])
    self.render_game_info(game_state['music_name'], game_state['progress'])
    
    if game_state['paused']:
        self.render_pause_overlay()
    
    pygame.display.flip()
```

#### add_judgment_feedback()
```python
def add_judgment_feedback(self, judgment_result: JudgmentResult) -> None:
    """判定フィードバックを追加"""
    self.active_judgments.append({
        'result': judgment_result,
        'start_time': pygame.time.get_ticks(),
        'position': (400, 400)  # 画面中央
    })
```

## 統合仕様

### GameManagerとの連携
```python
# GameManager内での使用例
def update(self, dt: float):
    # RhythmEngineから状態取得
    current_time = self.audio_manager.get_current_time()
    active_notes = self.rhythm_engine.get_active_notes(current_time)
    
    # UI描画用状態作成
    ui_state = {
        'notes': active_notes,
        'current_time': current_time,
        'score': self.rhythm_engine.get_score(),
        'combo': self.rhythm_engine.get_combo(),
        'multiplier': self.rhythm_engine.get_combo_multiplier(),
        'last_judgment': self.last_judgment_result,
        'music_name': self.current_music_name,
        'progress': current_time / self.music_duration,
        'paused': self.paused
    }
    
    # UI描画実行
    self.ui_renderer.render_frame(ui_state)
```

### RhythmEngineとの連携
```python
# 判定結果の受信
def on_judgment_made(self, judgment_result: JudgmentResult):
    self.ui_renderer.add_judgment_feedback(judgment_result)
```

## テスト戦略

### ユニットテスト
1. **描画テスト**: 各描画メソッドの動作確認
2. **アニメーションテスト**: 位置計算とタイミング検証
3. **状態管理テスト**: UI状態の正確な反映確認
4. **パフォーマンステスト**: フレームレート維持確認

### 統合テスト
1. **GameManager統合**: 完全なゲームフロー確認
2. **RhythmEngine統合**: 判定結果表示確認
3. **AudioManager統合**: 音楽同期確認

## 実装優先度

### Phase 1 (必須機能)
1. 基本的なノート描画・移動
2. スコア・コンボ表示
3. 判定結果フィードバック
4. 判定ライン表示

### Phase 2 (改善機能)
1. アニメーション効果改善
2. ビジュアルエフェクト追加
3. カスタマイズ可能な色彩
4. 解像度対応改善

## 成功基準

### 機能基準
- [ ] ノートが滑らかに移動し、判定ラインで正確に停止
- [ ] スコア・コンボがリアルタイムで正確に表示
- [ ] 判定結果が即座に視覚フィードバック
- [ ] 60FPS安定描画の達成

### 品質基準
- [ ] ユニットテストカバレッジ > 80%
- [ ] flake8コード品質準拠
- [ ] メモリ使用量の安定性
- [ ] レスポンシブな操作感

## 将来の拡張

### Phase 2での追加機能
- マルチレーン対応（複数キー）
- カスタムテーマ・スキン機能
- パーティクルエフェクト
- 解像度自動調整

### Phase 3での追加機能
- 3Dエフェクト
- アニメーション設定カスタマイズ
- リプレイ機能のUI
- オンライン機能のUI