# News Archive & Analysis System

ニュースを定期収集してGoogle Driveに蓄積し、週次で大局的分析を行うシステム。

## システム概要

```
ニュース収集（毎日）         週次分析（毎週月曜）
     │                           │
  WebSearch                   Drive読み取り
  WebFetch                       │
     │                      Claude AI分析
  HTMLファイル生成           ─────────────
     │                      要約・カテゴリ分析
  Google Drive保存           トレンド分析
     │                      大局的洞察
news-archive/daily/              │
  YYYY-MM-DD/             weekly-report.html
    news-001.html              保存
    news-002.html
    index.html
```

## Google Drive フォルダ構成

| フォルダ | ID |
|---------|-----|
| `news-archive` (root) | `1SK3FX_cxmTUubW0HeVHj9MrXgvXUzlRK` |
| `news-archive/daily` | `1oLDOHTuLt7J8DhWlo9r5ux8HC56WAEIp` |
| `news-archive/weekly` | `1HaHP36UX5LpFhMtMLW4fUBRJN6wMQzTR` |

## Claude Code スラッシュコマンド

### `/fetch-news` — 日次ニュース収集
- WebSearch で設定トピックのニュースを検索
- 各記事をHTMLファイルとしてDriveの `daily/YYYY-MM-DD/` に保存
- 日次インデックス（`index.html`）を生成
- **実行タイミング**: 毎日（スケジュールタスクで自動実行）

### `/weekly-analysis` — 週次分析レポート
- 過去7日間の全ニュースをDriveから読み取り
- Claude AIで要約・トレンド分析・大局的洞察を生成
- Chart.js を使ったビジュアルHTMLレポートを生成して保存
- **実行タイミング**: 毎週月曜日（スケジュールタスクで自動実行）

## 設定ファイル

### `config/news_config.yaml`
- 収集トピック（`news.topics`）
- カテゴリ分類（`news.categories`）
- Google Drive フォルダID（`google_drive.*`）
- 分析設定（`analysis.*`）

**トピックのカスタマイズ**: `config/news_config.yaml` の `news.topics` リストを編集して追加・変更する。

## ファイル構成

```
test-AI-coding/
├── CLAUDE.md                           # このファイル
├── config/
│   └── news_config.yaml                # 収集設定
├── scripts/
│   └── html_templates.py               # HTML生成ユーティリティ
├── .claude/
│   └── commands/
│       ├── fetch-news.md               # /fetch-news コマンド定義
│       └── weekly-analysis.md          # /weekly-analysis コマンド定義
└── requirements.txt
```

## スケジュールタスク設定方法

Claude Code on the Web でスケジュールタスクを設定する手順：
1. claude.ai/code でセッション設定を開く
2. 「Scheduled Tasks」に以下を追加：
   - **毎日**: `/fetch-news` を実行
   - **毎週月曜 9:00**: `/weekly-analysis` を実行

詳細: https://code.claude.com/docs/en/claude-code-on-the-web

## 週次レポートの見方

`news-archive/weekly/YYYY-WW/weekly-report.html` を開くと：
1. **統計サマリー**: 総記事数・カテゴリ数など
2. **AI週次要約**: その週のニュース全体像
3. **ビジュアルチャート**: カテゴリ分布（ドーナツ）＋日別推移（棒グラフ）
4. **トレンドキーワード**: 頻出キーワードとその出現回数
5. **大局的分析**: 構造的変化・マクロトレンド・注目動向
6. **全記事一覧**: 検索可能なテーブル形式
