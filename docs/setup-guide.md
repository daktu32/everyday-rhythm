# 開発環境セットアップガイド

バージョン: 1.0  
作成日: 2025-06-15  
プロジェクト: Everyday Rhythm

---

## 🚀 セットアップ手順

### Step 1: 必要なツールのインストール

#### 1.1 Python (3.10以上)
```bash
# Python バージョン確認
python3 --version
pip3 --version

# 3.10以上でない場合は以下からインストール
# https://www.python.org/downloads/
```

#### 1.2 Homebrew (macOS)
```bash
# Homebrew インストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# インストール確認
brew --version
```

#### 1.3 Git
```bash
# Git インストール確認
git --version

# 未インストールの場合
brew install git
```

#### 1.4 音声ライブラリの依存関係
```bash
# macOS で必要な音声処理ライブラリ
brew install portaudio
brew install ffmpeg
```

---

### Step 2: Python仮想環境の設定

#### 2.1 仮想環境作成
```bash
# プロジェクトディレクトリに移動
cd /path/to/everyday-rhythm

# 仮想環境作成
python3 -m venv venv

# 仮想環境有効化
source venv/bin/activate

# 仮想環境確認
which python
```

#### 2.2 依存関係インストール
```bash
# pip アップグレード
pip install --upgrade pip

# 必要なパッケージインストール
pip install pygame>=2.5.0
pip install pydub>=0.25.1
pip install librosa>=0.10.0
pip install requests>=2.31.0
pip install pytest>=7.4.0
pip install flake8>=6.0.0
pip install black>=23.0.0
```

---

### Step 3: プロジェクト初期化

#### 3.1 プロジェクトディレクトリ作成
```bash
# GitHubリポジトリをクローン
git clone [YOUR-REPO-URL] everyday-rhythm
cd everyday-rhythm

# プロジェクト構造作成
mkdir -p {src,assets,stages,tests,docs}
```

#### 3.2 requirements.txt作成
```bash
# requirements.txt作成
cat > requirements.txt << EOF
pygame>=2.5.0
pydub>=0.25.1
librosa>=0.10.0
requests>=2.31.0
pytest>=7.4.0
flake8>=6.0.0
black>=23.0.0
numpy>=1.24.0
scipy>=1.10.0
EOF
```

#### 3.3 基本ファイル構造作成
```bash
# ソースコードディレクトリ
mkdir -p src/{core,audio,ui,stages,utils}

# アセットディレクトリ
mkdir -p assets/{audio,images,fonts}

# ステージディレクトリ
mkdir -p stages/{generated,templates,samples}

# テストディレクトリ
mkdir -p tests/{unit,integration,fixtures}
```

---

### Step 4: Amazon Q Developer API設定

#### 4.1 API キー取得
- [ ] Amazon Q Developer アカウント作成
- [ ] API キーの生成
- [ ] 使用制限の確認

#### 4.2 環境変数設定
```bash
# .env ファイル作成
cat > .env << EOF
# Amazon Q Developer API
AMAZON_Q_API_KEY=your_api_key_here
AMAZON_Q_ENDPOINT=https://api.amazonq.developer

# Game Configuration
GAME_WINDOW_WIDTH=800
GAME_WINDOW_HEIGHT=600
AUDIO_BUFFER_SIZE=1024
TARGET_FPS=60

# Development
DEBUG_MODE=true
LOG_LEVEL=INFO
EOF
```

#### 4.3 環境変数読み込み設定
```python
# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AMAZON_Q_API_KEY = os.getenv('AMAZON_Q_API_KEY')
    AMAZON_Q_ENDPOINT = os.getenv('AMAZON_Q_ENDPOINT')
    GAME_WINDOW_WIDTH = int(os.getenv('GAME_WINDOW_WIDTH', 800))
    GAME_WINDOW_HEIGHT = int(os.getenv('GAME_WINDOW_HEIGHT', 600))
    AUDIO_BUFFER_SIZE = int(os.getenv('AUDIO_BUFFER_SIZE', 1024))
    TARGET_FPS = int(os.getenv('TARGET_FPS', 60))
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
```

---

### Step 5: 開発ツール設定

#### 5.1 VS Code拡張機能（推奨）
```json
// .vscode/extensions.json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-python.pylint",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml"
  ]
}
```

#### 5.2 VS Code設定
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true
  }
}
```

#### 5.3 Git設定
```bash
# .gitignore作成
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Game specific
*.wav
*.mp3
!assets/audio/samples/*.wav
!assets/audio/samples/*.mp3

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Temporary files
*.tmp
*.temp
EOF
```

---

### Step 6: 基本コード実装

#### 6.1 メインエントリーポイント
```python
# main.py
#!/usr/bin/env python3
"""
Everyday Rhythm - Main Entry Point
"""

import sys
import pygame
from src.core.game_manager import GameManager
from src.utils.config import Config

def main():
    """Main game loop"""
    try:
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init(buffer=Config.AUDIO_BUFFER_SIZE)
        
        # Create game manager
        game_manager = GameManager()
        
        # Start game
        game_manager.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        return 1
    
    finally:
        pygame.quit()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

#### 6.2 基本的なゲームマネージャー
```python
# src/core/game_manager.py
import pygame
from src.utils.config import Config

class GameManager:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (Config.GAME_WINDOW_WIDTH, Config.GAME_WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Everyday Rhythm")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(Config.TARGET_FPS)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space key pressed!")
    
    def update(self):
        """Update game state"""
        pass
    
    def render(self):
        """Render game"""
        self.screen.fill((0, 0, 0))  # Black background
        pygame.display.flip()
```

---

### Step 7: 動作確認

#### 7.1 基本動作テスト
```bash
# 仮想環境有効化
source venv/bin/activate

# 基本動作確認
python main.py
```

#### 7.2 依存関係テスト
```bash
# Pygame テスト
python -c "import pygame; print('Pygame version:', pygame.version.ver)"

# 音声ライブラリテスト
python -c "import pydub; print('pydub imported successfully')"
python -c "import librosa; print('librosa imported successfully')"
```

#### 7.3 コード品質チェック
```bash
# コードスタイルチェック
flake8 src/ --max-line-length=88

# コードフォーマット
black src/ tests/

# テスト実行
pytest tests/ -v
```

---

## ✅ セットアップ完了チェック

- [ ] Python 3.10+ インストール済み
- [ ] 仮想環境作成・有効化済み
- [ ] 必要なPythonパッケージインストール済み
- [ ] プロジェクト構造作成済み
- [ ] Amazon Q Developer API設定済み
- [ ] 環境変数ファイル作成済み
- [ ] VS Code設定完了
- [ ] Git設定完了
- [ ] 基本コード実装済み
- [ ] 動作確認成功

---

## 🚀 次のステップ

セットアップ完了後、以下を開始できます：

1. **音声システム実装**: AudioManager クラスの実装
2. **リズムエンジン実装**: RhythmEngine クラスの実装
3. **ステージローダー実装**: StageLoader クラスの実装
4. **Amazon Q統合**: ステージ生成機能の実装

---

## ❓ トラブルシューティング

### よくある問題

#### Python バージョンエラー
```bash
# pyenv使用の場合
pyenv install 3.10.12
pyenv local 3.10.12
```

#### Pygame インストールエラー
```bash
# macOS での解決方法
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

#### 音声ライブラリエラー
```bash
# portaudio エラーの場合
brew install portaudio
pip uninstall pydub
pip install pydub
```

#### librosa インストールエラー
```bash
# 依存関係の問題
brew install llvm
pip install librosa
```

#### 仮想環境の問題
```bash
# 仮想環境再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**完了お疲れさまでした！** 🎉  
何か問題があれば、エラーメッセージと一緒にお知らせください。
