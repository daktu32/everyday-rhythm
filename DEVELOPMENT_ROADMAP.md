# DEVELOPMENT_ROADMAP.md

Everyday Rhythmプロジェクトの開発ロードマップです。各フェーズのマイルストーン、成果物、技術的決定事項を記録します。

## プロジェクト概要

**ビジョン**: Amazon Q Developerを活用した、誰でも楽しめるシンプルなリズムゲームの構築

**目標**:
- スペースキー1つで操作できるシンプルさ
- 自然言語からのステージ自動生成
- 日常をテーマとした親しみやすいコンテンツ
- ローカル実行による安全性とプライバシー保護

## フェーズ別開発計画

### Phase 0: プロジェクト初期設定 (完了)
**期間**: 2025年6月15日 - 2025年6月20日

#### マイルストーン
- [x] プロジェクト構造の決定
- [x] 技術スタックの選定
- [x] 開発ガイドライン（CLAUDE.md）の作成
- [x] developer-kit準拠のドキュメント構造整備
- [x] Python開発環境のセットアップ
- [x] 基本的なプロジェクト構造の作成
- [x] 依存関係の管理設定

#### 成果物
- CLAUDE.md（開発ガイドライン）
- PROGRESS.md（進捗管理ファイル）
- DEVELOPMENT_ROADMAP.md（このファイル）
- プロジェクトのディレクトリ構造
- requirements.txt（Python依存関係）

#### 技術的決定事項
- 言語: Python 3.10+
- UIフレームワーク: Pygame
- 音声処理: pydub, librosa
- ステージ生成: Amazon Q Developer API
- データ形式: JSON

### Phase 1: 基盤構築 (完了)
**期間**: 2025年6月15日 - 2025年6月15日

#### マイルストーン
- [x] Python開発環境の完全セットアップ
- [x] Pygameの基本ウィンドウとゲームループ実装
- [x] 基本的なキー入力処理
- [x] 設定管理システム実装
- [x] テスト環境構築
- [x] コード品質管理設定

#### 成果物
- main.py（メインエントリーポイント）
- src/core/game_manager.py（ゲーム制御）
- src/utils/config.py（設定管理）
- 包括的なテストスイート（15テスト）
- 開発環境完全構築

#### 技術的成果
- 60FPS安定動作確認
- テストカバレッジ67%達成
- flake8コード品質基準準拠
- CLI引数サポート実装

#### リスク評価
- [x] Pygame環境構築の複雑性 → 解決済み
- [ ] 音楽ファイル形式の互換性 → Phase 2で対応
- [ ] Amazon Q Developer API制限の確認 → Phase 3で対応

### Phase 2: Audio System (完了)
**期間**: 2025年6月15日 - 2025年6月15日

#### マイルストーン
- [x] 音楽再生機能の実装（AudioManager）
- [x] 音声解析機能の実装（AudioAnalyzer）
- [x] 高精度タイミング同期の実装
- [x] CLI音声サポートの実装
- [x] 包括的エラーハンドリング

#### 成果物
- src/audio/audio_manager.py（音楽再生・タイミング同期）
- src/audio/audio_analyzer.py（音声解析・テンポ検出）
- CLI音声引数サポート（--audio, --volume）
- 19のAudioManagerテスト + 12のAudioAnalyzerテスト

#### 成功指標
- [x] タイミング精度 ±10ms達成
- [x] 安定した60FPS描画
- [x] スムーズな音楽再生
- [x] 音声レイテンシ15-30ms

### Phase 3: Rhythm Engine (完了)
**期間**: 2025年6月15日 - 2025年6月15日

#### マイルストーン
- [x] リズム判定エンジンの実装（RhythmEngine）
- [x] ノート管理システムの実装（Note）
- [x] スコア評価システムの実装（JudgmentResult）
- [x] コンボシステムの実装
- [x] TDD品質保証の実施

#### 成果物
- src/core/rhythm_engine.py（リズム判定・スコア評価）
- src/gameplay/note.py（ノート管理・タイミング判定）
- JudgmentResultクラス（判定結果管理）
- 12のRhythmEngineテスト + 16のNoteテスト

#### 成功指標
- [x] タイミング判定精度 ±25ms/±50ms達成
- [x] コンボシステム実装（1.1x-1.2x倍率）
- [x] TDD品質保証完了
- [x] 包括的API設計完了

### Phase 4: UI/UX Development (完了)
**期間**: 2025年6月15日 - 2025年6月15日

#### マイルストーン
- [x] UI描画機能の実装（UIRenderer）
- [x] ノート表示・移動アニメーション
- [x] スコア表示・判定フィードバック
- [x] GameManager統合（RhythmEngineとの連携）
- [x] 基本的なゲームプレイの完成

#### 成果物
- src/ui/ui_renderer.py（UI描画・アニメーション）
- GameManager-RhythmEngine-UIRenderer統合
- 完全なゲームプレイ体験
- UIRendererテストスイート（18テスト）

#### 成功指標
- [x] スムーズなノートアニメーション（60FPS）
- [x] 直感的なスコア表示
- [x] レスポンシブな判定フィードバック

### Phase 5: ステージ生成機能 (次期)
**期間**: 2025年6月15日 - 2025年6月20日

#### マイルストーン
- [ ] StageLoader実装（JSONステージ読み込み）
- [ ] 音楽解析による自動ノート配置改善
- [ ] Amazon Q Developer API統合
- [ ] 自然言語からステージ生成機能
- [ ] ステージテンプレート最適化

#### 成果物
- src/stage/stage_loader.py（ステージ管理）
- 改良された音楽解析機能（librosa活用）
- Amazon Q Developer API連携モジュール
- 自動ステージ生成システム
- ステージテンプレート・ライブラリ

### Phase 6: 品質保証とUI改善
**期間**: 2025年6月21日 - 2025年6月30日

#### マイルストーン
- [ ] 包括的なテスト実装
- [ ] UI/UX改善
- [ ] パフォーマンス最適化
- [ ] ドキュメント整備
- [ ] 配布準備

#### 成果物
- 完全なテストスイート
- 改善されたUI/UX
- パフォーマンス最適化
- ユーザードキュメント
- 配布パッケージ

### Phase 7: リリースと拡張
**期間**: 2025年7月1日以降

#### マイルストーン
- [ ] オープンソースリリース
- [ ] コミュニティフィードバック収集
- [ ] 機能改善とバグ修正
- [ ] 将来機能の検討
- [ ] 継続的なメンテナンス

#### 成功基準
- 安定したゲームプレイ体験
- ユーザーフレンドリーなUI
- 効果的なステージ生成機能
- 良好なコミュニティ反応

## 技術アーキテクチャの進化

### 現在の構成
```
main.py → GameManager → [AudioManager, StageLoader, RhythmEngine, ScoreEvaluator, UIRenderer]
                                ↓
                        Amazon Q Developer API
```

### 将来の拡張
```
main.py → GameManager → [AudioManager, StageLoader, RhythmEngine, ScoreEvaluator, UIRenderer]
                                ↓                    ↓
                        Amazon Q Developer API    GUI Framework (Tkinter/PyQt)
                                ↓
                        Online Features (Future)
```

## リスク管理

### 技術的リスク
- **API制限**: Amazon Q Developer APIの使用制限とコスト管理
- **音楽処理**: 異なる音楽形式への対応とパフォーマンス
- **タイミング精度**: Pygameでの正確なタイミング判定実装
- **依存関係**: Python環境とライブラリの互換性

### ビジネスリスク
- **著作権**: 音楽ファイルの著作権問題
- **API コスト**: Amazon Q Developer使用料の予算管理
- **ユーザビリティ**: シンプルさと機能性のバランス

## 更新履歴

### 2025-06-15
- 初版作成
- Phase 0-5の定義
- 技術スタックの決定
- マイルストーンの設定
- developer-kit準拠のドキュメント構造整備完了