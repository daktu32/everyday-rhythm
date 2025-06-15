# Product Requirements Document (PRD)

## 1. Product Name
**Everyday Rhythm**

## 2. Executive Summary

### 🎯 Vision
「リズムは誰の中にもある」──日常の何気ない行動をポップで楽しいリズムゲームに変える、新感覚ミニゲーム集。

### 🔍 Problem Statement
- リズムゲームは複雑な操作やルールで初心者が入りづらい  
- カジュアル層向けに1キーで楽しめるゲームが不足  
- ステージ作成の負荷が高く、クリエイターも参入しにくい  

### 💡 Solution Overview
Amazon Q Developer を使って、音楽と自然言語の雰囲気からステージを自動生成。スペースキーだけで操作でき、日常の行動をテーマとしたミニゲーム集として展開。

## 3. Target Audience

### Primary Users
- カジュアルゲーマー（簡単操作）
- 非ゲーマー層（親しみやすさ重視）
- クリエイター層（生成ツール活用）

### User Demographics
- 年齢: 10〜40代
- 技術: 初〜中級
- 地域: 日本中心にアジア圏
- 業界: エンタメ、一般消費者

## 4. Value Proposition
> 誰でも、いつでも、どこでも、スペースキー1つでリズムを楽しめる。

### Key Benefits
1. 操作がシンプル  
2. 身近なテーマで共感しやすい  
3. ステージが自動生成される  

## 5. Product Requirements

### Must-Have Features

| Feature | Description | User Story | Priority |
|--------|-------------|------------|----------|
| 音楽再生 | 指定音楽を再生しながらゲーム進行 | As a player, I want to play rhythm with my own music | P0 |
| 自然言語からステージ生成 | Amazon Qで雰囲気→ステージ生成 | As a creator, I want to generate stages from text and music | P0 |
| スペースキー判定 | タップタイミングを評価 | As a player, I want to tap space in rhythm and get evaluated | P0 |

### Nice-to-Have Features

| Feature | Description | User Story | Priority |
|--------|-------------|------------|----------|
| ステージ編集GUI | 自動生成の微調整用 | As a creator, I want to tweak stages | P1 |
| スコア共有 | SNSに投稿可能 | As a player, I want to share my results | P2 |

### Future Considerations
- ステージ共有機能
- マルチキー操作
- 内蔵音楽ライブラリ

## 6. User Journey

```mermaid
graph LR
    A[起動] --> B[音楽とテーマ選択]
    B --> C[自動生成]
    C --> D[プレイ開始]
    D --> E[スコアと判定表示]
```

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| 月間アクティブユーザー | 10,000 |
| ステージ生成回数 | 1,000/日 |
| SNSシェア率 | 20% |

## 8. Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| 設計 | 2週間 | PRD、要件定義 |
| 開発 | 4週間 | Pygameプロトタイプ |
| βテスト | 2週間 | ユーザーフィードバック |
| リリース | 2週間 | 公開と初期広報 |

---
**Author**: 塚原大輔  
**Version**: 0.1  
**Last Updated**: 2025-06-15
