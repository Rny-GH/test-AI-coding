# 週次ニュース分析レポート生成

過去7日間のアーカイブニュースを分析し、包括的な週次レポートをGoogle Driveに保存する。

## 手順

### 1. 分析対象期間の設定
今日の日付から過去7日間の日付リストを生成する（YYYY-MM-DD形式）。
例: 今日が2026-05-31なら、2026-05-25〜2026-05-31の7日分。
週ラベルは ISO週番号形式：`{YYYY}-W{WW}` （例: `2026-W22`）

### 2. Google Drive からニュースファイルを収集
Google Drive MCP ツールで `daily` フォルダ（ID: `1oLDOHTuLt7J8DhWlo9r5ux8HC56WAEIp`）を検索：

各日付フォルダを探して、その中の全HTMLファイル（`index.html`を除く）を取得する。
メタデータから以下の情報を読み取る：
- `news-date`, `news-source`, `news-category`, `news-keywords`, `news-url`, タイトル

ファイル数が多い場合（20件超）は `read_file_content` でHTMLを読んでメタデータを抽出する。

### 3. データ集計・分析
収集した記事データから：

**統計情報を集計:**
- カテゴリ別記事数: `{Technology: N, Business: N, ...}`
- 日別記事数（時系列）: `[{date: "2026-05-25", count: N}, ...]`
- キーワード出現頻度: 全記事のキーワードを集計し、上位20件を選出

**トレンド分析を実施:**
- 最も多く報じられたトピック・テーマ
- 前週（比較データがあれば）との変化
- カテゴリの重心（何の話題が多かったか）

### 4. AI による分析生成
収集した全記事のタイトルと要約を使って以下を生成する：

**① 週次AI要約（300〜400字）:**
今週のニュースの全体像を把握できる日本語の要約。
主要トピック、注目すべき出来事、業界の動向を含む。

**② 大局的分析・洞察（600〜800字）:**
以下の観点から分析する：
- 複数のカテゴリにまたがるマクロトレンド
- 重要性が高い構造的変化（テクノロジー・経済・社会）
- 来週以降に注目すべき動向
- 長期的文脈での位置づけ（可能であれば過去数週間との比較）

### 5. 週次レポートHTML生成
`scripts/html_templates.py` の `weekly_report_html()` を参考に、以下を含む包括的なHTMLレポートを生成する：

**レポートの構成:**
1. ヘッダー（週ラベル、期間、総記事数）
2. 統計サマリーカード（4枚）
3. AIによる週次要約
4. グラフ（カテゴリ別ドーナツ + 日別棒グラフ）※ Chart.js CDN 使用
5. トレンドキーワード一覧
6. 大局的分析・洞察
7. 全記事一覧（日付・タイトル・カテゴリ・ソース）

Chart.jsのデータはHTMLに直接埋め込む（JSON形式でJS変数として定義）。

### 6. Google Drive への保存
Google Drive の `weekly` フォルダ（ID: `1HaHP36UX5LpFhMtMLW4fUBRJN6wMQzTR`）に保存：
- フォルダ名: `{YYYY}-W{WW}`（存在しなければ作成）
- ファイル名: `weekly-report.html`
- `content_mime_type`: `text/html`
- `disable_conversion_to_google_type`: `true`

### 7. 完了レポート
```
📊 週次分析レポート完成 - {week_label}
=====================================
対象期間: {date_range}
総記事数: {N}
カテゴリ別: Technology({n}), Business({n}), ...
トップキーワード: {kw1}, {kw2}, {kw3}, ...

【大局的分析サマリー】
{macro_analysis の冒頭2文}

Google Drive レポート: {report_url}
```

## 注意事項
- 記事データが少ない（7件未満）場合でもレポートを生成する
- 利用可能なデータがない期間はスキップして集計する
- Chart.jsは必ずCDNから読み込む: `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`
- HTMLファイルはDriveに変換されないよう `disable_conversion_to_google_type: true` を必ず設定する
