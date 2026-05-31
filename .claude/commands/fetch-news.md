# 日次ニュース収集・アーカイブ

今日のニュースを収集し、Google Driveに HTML形式で保存する。

## 手順

### 1. 日付の確認
今日の日付を取得する（YYYY-MM-DD形式）。現在の日付を使用すること。

### 2. Google Drive の日付フォルダを作成
Google Drive MCP ツールを使って以下の操作を行う：
- `daily` フォルダ（ID: `1oLDOHTuLt7J8DhWlo9r5ux8HC56WAEIp`）内に、`YYYY-MM-DD` という名前のフォルダが存在するか検索する
- 存在しない場合は作成する
- フォルダIDを記録しておく

### 3. ニュースを検索・収集
`config/news_config.yaml` に定義されているトピックごとに WebSearch を実行する：
- `AI 人工知能 最新ニュース site:japan OR site:jp`
- `テクノロジー IT業界 動向 今日`
- `スタートアップ 資金調達 今週`
- `経済 ビジネス トレンド 最新`
- `科学技術 イノベーション ニュース`

各検索結果から **上位5〜6件**の記事を選ぶ。重複は避ける。

### 4. 各記事の詳細取得
各記事について：
1. WebFetch で記事の本文を取得（タイムアウト対策として最大3000文字）
2. 以下の情報を抽出・生成：
   - **title**: 記事タイトル（日本語）
   - **url**: 元記事URL
   - **source**: 出典（メディア名）
   - **date**: 公開日（YYYY-MM-DD）
   - **category**: Technology / Business / Science / Society / Startup のいずれか
   - **summary**: 3〜4文の日本語要約
   - **keywords**: 関連キーワード3〜5個のリスト

### 5. HTML生成・保存
各記事をHTMLファイルとしてGoogle Driveに保存する：

**記事HTMLの構造:**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="news-date" content="{date}">
  <meta name="news-source" content="{source}">
  <meta name="news-category" content="{category}">
  <meta name="news-keywords" content="{keyword1},{keyword2},...">
  <meta name="news-url" content="{url}">
  <title>{title}</title>
  <!-- スタイルは scripts/html_templates.py の news_article_html() を参考に -->
</head>
<body>
  <!-- カテゴリバッジ、タイトル、メタ情報、要約、キーワード、元記事リンク -->
</body>
</html>
```

ファイル名: `news-001.html`, `news-002.html`, ...（3桁連番）

Google Drive に保存する際：
- `content_mime_type`: `text/html`
- `disable_conversion_to_google_type`: `true`（Google Docsに変換しない）
- `parent_id`: 作成した日付フォルダのID

### 6. 日次インデックス（index.html）を作成
その日の全記事をまとめたインデックスページを作成する：
- カテゴリ別に記事をグループ化
- 各記事へのリンクを含む
- ファイル名: `index.html`
- 同じ日付フォルダに保存

### 7. 完了レポート
以下の形式でサマリーを出力する：
```
📰 ニュース収集完了 - {date}
================================
総記事数: {N}
カテゴリ別: Technology({n}), Business({n}), ...
Google Drive フォルダ: {folder_url}
```

## 注意事項
- 1記事のHTML保存が失敗しても次の記事を継続する
- 同じ記事（同一URL）を重複保存しない
- WebFetch が失敗した場合は検索スニペットから要約を生成する
- 記事は日本語・英語両方OK（要約は日本語で）
