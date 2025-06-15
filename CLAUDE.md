# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリのコードを扱う際のガイダンスを提供します。

## プロジェクト概要

Everyday Rhythm - Amazon Q Developerを活用したPygameベースのリズムゲーム開発プロジェクト

## 技術スタック

### フロントエンド
- **フレームワーク**: Pygame
- **言語**: Python 3.10+
- **音声処理**: pydub, librosa
- **ファイル形式**: .mp3, .wav対応

### バックエンド
- **ランタイム**: Python 3.10+
- **ステージ生成**: Amazon Q Developer API
- **データ形式**: JSON（ステージテンプレート）

### Infrastructure as Code
- **実行環境**: macOS Sonoma (14.x) 以降
- **起動方法**: ターミナルから `python main.py`

## アーキテクチャ

### 概要
```
[main.py] → [GameManager] → [AudioManager, StageLoader, RhythmEngine, ScoreEvaluator, UIRenderer]
```

### 主要コンポーネント
- **main.py**: 起動・ループ管理
- **GameManager**: ゲーム全体の状態制御
- **AudioManager**: 音楽の再生・時刻取得
- **StageLoader**: ステージJSONの読み込み
- **RhythmEngine**: ノートとキー入力の照合
- **ScoreEvaluator**: 判定結果からスコア算出
- **UIRenderer**: 判定結果と画面描画処理

## 開発哲学

### コア原則
- **テスト駆動開発（TDD）**: テストを先に書き、その後実装
- **クリーンコード**: 保守性、可読性、ドキュメント化を重視
- **セキュリティファースト**: 最初からセキュリティのベストプラクティスに従う
- **パフォーマンス**: 速度と効率を最適化
- **スケーラビリティ**: 初日から成長を想定した設計

## 主要機能

### MVP機能
1. **音楽再生**: 指定音楽を再生しながらゲーム進行
2. **ステージ生成**: Amazon Q Developerで自然言語からステージ自動生成
3. **リズム判定**: スペースキーによるタップタイミング評価
4. **スコア表示**: 判定結果に基づくスコア算出・表示
5. **ステージ管理**: JSONテンプレートの読み込み・管理

### 将来の機能
- GUI化（Tkinter/PyQt）
- ステージ投稿・共有機能
- 複数キー対応
- オンライン機能

## セキュリティ＆コンプライアンス

### セキュリティ対策
- **API制限**: Amazon Q Developer APIの使用制限遵守
- **データ保護**: ローカル実行でプライバシー保護
- **著作権**: 音源は非商用利用に限定

### コンプライアンス考慮事項
- **API利用規約**: Amazon Q Developer利用規約準拠
- **音楽著作権**: JASRACなど著作権団体のガイドライン遵守
- **プライバシー**: ユーザーデータのローカル保存

## コスト構造

### 見積もりコスト
- **開発フェーズ**: 無料（ローカル開発）
- **API使用**: Amazon Q Developer API使用料
- **配布**: 無料（オープンソース）

### コスト内訳
- **開発環境**: Python環境（無料）
- **API使用**: Amazon Q Developer従量課金
- **音楽ファイル**: ユーザー提供（著作権フリー推奨）

## 開発ワークフロー

### 現在のステータス
- **フェーズ**: 初期設定・設計
- **スプリント**: Sprint 0
- **マイルストーン**: プロジェクト構造の確立

### アクティブな開発
1. プロジェクト初期設定
2. 開発環境構築（Python + Pygame）
3. 基本的なゲームループ実装
4. Amazon Q Developer API統合

## 進捗管理ルール

### 必須ファイル更新
AIエージェントは以下のファイルを最新の状態に保つ必要があります：

1. **PROGRESS.md** - 開発進捗の追跡
   - 各タスク完了後に更新
   - 完了したタスク、現在の作業、次のタスクを文書化
   - 日付とタイムスタンプを含める

2. **DEVELOPMENT_ROADMAP.md** - 開発ロードマップ
   - フェーズが進むにつれて更新
   - 完了したマイルストーンにチェックマークを付ける
   - 新しい課題や変更を反映

### 更新タイミング
- 機能実装完了時
- 重要な設定変更後
- フェーズ移行時
- バグ修正や改善後
- 新しい技術的決定を行った時

### 更新方法
1. 作業完了直後に関連ファイルを更新
2. 具体的な成果物と変更を文書化
3. 次のステップを明確にする
4. コミットメッセージに進捗更新を含める

## プロジェクト固有の開発ルール

### Gitワークフロー

#### ブランチ戦略
- **メインブランチ**: `main`
- **機能ブランチ**: `feature/task-description`
- **バグ修正ブランチ**: `fix/bug-description`

#### 必須作業手順
すべての開発作業で以下の手順に従う：

1. 機能要件を定義し、`docs/specs/`に文書化
2. **作業ブランチを作成し、git worktreeで分離**
3. 期待される入出力に基づいてテストを作成
4. テストを実行し、失敗を確認
5. テストがパスするコードを実装
6. すべてのテストがパスしたらリファクタリング
7. 進捗ファイル（PROGRESS.md、DEVELOPMENT_ROADMAP.md）を更新

#### Worktreeの使用
```bash
# 必須手順
git checkout main && git pull origin main
git checkout -b feature/task-name
git worktree add ../amazon-q-game-challenge-feature ./feature/task-name
```

### モジュール構造

- `src/`: ソースコード
  - `main.py`: メインエントリーポイント
  - `game_manager.py`: ゲーム全体制御
  - `audio_manager.py`: 音楽再生管理
  - `stage_loader.py`: ステージ読み込み
  - `rhythm_engine.py`: リズム判定エンジン
  - `score_evaluator.py`: スコア評価
  - `ui_renderer.py`: UI描画
- `stages/`: ステージJSONファイル
- `assets/`: 音楽ファイル・画像
- `docs/`: ドキュメント
- `tests/`: テストファイル

### コーディング標準

#### ファイル命名規則
- **Pythonモジュール**: `snake_case.py`
- **クラス**: `PascalCase`
- **関数・変数**: `snake_case`
- **定数**: `UPPER_SNAKE_CASE`
- **ステージファイル**: `stage_name.json`

#### 品質チェックリスト
実装完了前に以下を確認：
- `python -m py_compile src/*.py` (構文チェック)
- `python -m pytest tests/` (テスト実行)
- `python -m flake8 src/` (コードスタイル)
- `python main.py` (動作確認)

### クラウド統合ガイドライン

#### サービスアーキテクチャ
- **ステージ生成**: Amazon Q Developer API
- **音楽処理**: pydub, librosa（ローカル）
- **データ保存**: JSON形式（ローカル）
- **実行環境**: Python 3.10+ (macOS)

#### セキュリティ原則
- API キーの適切な管理
- ローカル実行によるプライバシー保護
- 著作権を考慮した音源利用
- 定期的なセキュリティ確認

### 禁止事項

以下の実践は厳格に禁止されています：
- テストなしでの機能実装
- mainブランチでの直接作業
- APIキーのハードコーディング
- 既存のゲームループインターフェースの破壊
- 承認なしでの外部依存関係の追加
- ドキュメント更新のスキップ
- PROGRESS.mdとDEVELOPMENT_ROADMAP.mdの更新を無視すること
- 著作権のある音源の無断使用

### 実装後チェックリスト
- [ ] すべてのテストがパス
- [ ] 構文チェックがパス
- [ ] コードスタイルチェックがパス
- [ ] ドキュメントが更新されている
- [ ] PROGRESS.mdが完了タスクと次のタスクで更新されている
- [ ] DEVELOPMENT_ROADMAP.mdが進捗で更新されている
- [ ] 説明的なメッセージでコミットされている
- [ ] 明確な説明でプルリクエストが作成されている