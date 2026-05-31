"""HTML template generation for news articles and weekly reports."""

from datetime import datetime


def news_article_html(
    title: str,
    url: str,
    source: str,
    date: str,
    category: str,
    summary: str,
    keywords: list[str],
    content: str = "",
    article_number: int = 1,
) -> str:
    keywords_str = ", ".join(keywords)
    keywords_badges = "".join(
        f'<span class="keyword">{kw}</span>' for kw in keywords
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="news-date" content="{date}">
  <meta name="news-source" content="{source}">
  <meta name="news-category" content="{category}">
  <meta name="news-keywords" content="{keywords_str}">
  <meta name="news-url" content="{url}">
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f5f7fa; color: #2d3748; line-height: 1.7; padding: 20px; }}
    .container {{ max-width: 800px; margin: 0 auto; background: white;
                 border-radius: 12px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
    .category-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px;
                      font-size: 12px; font-weight: 600; margin-bottom: 16px; }}
    .cat-Technology {{ background: #ebf8ff; color: #2b6cb0; }}
    .cat-Business {{ background: #f0fff4; color: #276749; }}
    .cat-Science {{ background: #faf5ff; color: #6b46c1; }}
    .cat-Society {{ background: #fff5f5; color: #c53030; }}
    .cat-Startup {{ background: #fffaf0; color: #c05621; }}
    h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 12px; line-height: 1.4; }}
    .meta {{ display: flex; gap: 16px; font-size: 13px; color: #718096; margin-bottom: 20px;
            padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; }}
    .summary {{ font-size: 16px; color: #4a5568; margin-bottom: 20px;
               padding: 16px; background: #f7fafc; border-left: 4px solid #4299e1;
               border-radius: 0 8px 8px 0; }}
    .content {{ font-size: 15px; color: #4a5568; margin-bottom: 24px; }}
    .keywords {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px; }}
    .keyword {{ padding: 4px 12px; background: #edf2f7; border-radius: 16px;
               font-size: 12px; color: #4a5568; }}
    .source-link {{ display: inline-block; padding: 10px 20px; background: #4299e1;
                   color: white; text-decoration: none; border-radius: 8px; font-size: 14px; }}
    .source-link:hover {{ background: #3182ce; }}
    .article-id {{ font-size: 11px; color: #a0aec0; margin-top: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="category-badge cat-{category}">{category}</span>
    <h1>{title}</h1>
    <div class="meta">
      <span>📅 {date}</span>
      <span>📰 {source}</span>
      <span>🔢 #{article_number:03d}</span>
    </div>
    <div class="summary">{summary}</div>
    {f'<div class="content">{content}</div>' if content else ''}
    <div class="keywords">{keywords_badges}</div>
    <a class="source-link" href="{url}" target="_blank">元記事を読む →</a>
    <div class="article-id">Archived: {datetime.now().isoformat()}</div>
  </div>
</body>
</html>"""


def daily_index_html(date: str, articles: list[dict]) -> str:
    categories = {}
    for a in articles:
        cat = a.get("category", "Other")
        categories.setdefault(cat, []).append(a)

    category_sections = ""
    for cat, items in sorted(categories.items()):
        items_html = "".join(
            f"""<li class="article-item">
              <a href="{item['filename']}" class="article-link">{item['title']}</a>
              <span class="article-source">{item['source']}</span>
            </li>"""
            for item in items
        )
        category_sections += f"""
        <div class="category-section">
          <h2 class="cat-header">{cat} ({len(items)})</h2>
          <ul class="article-list">{items_html}</ul>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="index-date" content="{date}">
  <title>News Archive - {date}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f5f7fa; color: #2d3748; padding: 20px; }}
    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
              color: white; padding: 24px 32px; border-radius: 12px; margin-bottom: 24px; }}
    h1 {{ font-size: 28px; font-weight: 700; }}
    .subtitle {{ opacity: 0.85; margin-top: 4px; }}
    .stats {{ display: flex; gap: 16px; margin-top: 16px; }}
    .stat {{ background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; font-size: 14px; }}
    .category-section {{ background: white; border-radius: 12px; padding: 24px;
                        margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .cat-header {{ font-size: 18px; font-weight: 600; color: #4a5568; margin-bottom: 16px;
                  padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }}
    .article-list {{ list-style: none; }}
    .article-item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; display: flex;
                    align-items: baseline; gap: 12px; }}
    .article-item:last-child {{ border-bottom: none; }}
    .article-link {{ color: #3182ce; text-decoration: none; font-weight: 500; flex: 1; }}
    .article-link:hover {{ color: #2c5282; text-decoration: underline; }}
    .article-source {{ font-size: 12px; color: #a0aec0; white-space: nowrap; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>📰 Daily News Archive</h1>
    <div class="subtitle">{date}</div>
    <div class="stats">
      <div class="stat">総記事数: {len(articles)}</div>
      <div class="stat">カテゴリ数: {len(categories)}</div>
    </div>
  </div>
  {category_sections}
</body>
</html>"""


def weekly_report_html(
    week_label: str,
    date_range: str,
    articles: list[dict],
    ai_summary: str,
    category_counts: dict[str, int],
    top_keywords: list[tuple[str, int]],
    timeline_data: list[dict],
    macro_analysis: str,
) -> str:
    # Chart.js data
    cat_labels = list(category_counts.keys())
    cat_values = list(category_counts.values())
    cat_colors = [
        "#4299e1", "#48bb78", "#9f7aea", "#fc8181", "#ed8936",
        "#38b2ac", "#667eea", "#f6ad55"
    ][:len(cat_labels)]

    timeline_labels = [d["date"] for d in timeline_data]
    timeline_values = [d["count"] for d in timeline_data]

    keyword_items = "".join(
        f'<div class="kw-item"><span class="kw-text">{kw}</span>'
        f'<span class="kw-count">{count}</span></div>'
        for kw, count in top_keywords[:20]
    )

    article_rows = "".join(
        f"""<tr>
          <td>{a.get('date', '')}</td>
          <td><a href="{a.get('url', '#')}" target="_blank">{a.get('title', '')}</a></td>
          <td><span class="badge badge-{a.get('category', 'Other')}">{a.get('category', '')}</span></td>
          <td>{a.get('source', '')}</td>
        </tr>"""
        for a in sorted(articles, key=lambda x: x.get("date", ""), reverse=True)
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="report-week" content="{week_label}">
  <meta name="report-date-range" content="{date_range}">
  <title>週次ニュース分析レポート - {week_label}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #f5f7fa; color: #2d3748; }}
    .page-header {{ background: linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #4a5568 100%);
                   color: white; padding: 40px; }}
    .page-header h1 {{ font-size: 32px; font-weight: 700; }}
    .page-header .meta {{ opacity: 0.8; margin-top: 8px; font-size: 16px; }}
    .content {{ max-width: 1200px; margin: 0 auto; padding: 32px 20px; }}
    .section {{ background: white; border-radius: 12px; padding: 28px;
               margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
    .section h2 {{ font-size: 20px; font-weight: 600; color: #2d3748;
                 margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #e2e8f0; }}
    .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
    .chart-box {{ background: white; border-radius: 12px; padding: 24px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
    .chart-box h3 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #4a5568; }}
    .ai-summary {{ font-size: 15px; line-height: 1.8; color: #4a5568;
                  padding: 20px; background: #f0f4ff; border-radius: 8px;
                  border-left: 4px solid #667eea; }}
    .macro-analysis {{ font-size: 15px; line-height: 1.8; color: #4a5568;
                      padding: 20px; background: #f0fff4; border-radius: 8px;
                      border-left: 4px solid #48bb78; white-space: pre-wrap; }}
    .keywords-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .kw-item {{ display: flex; align-items: center; gap: 6px; padding: 6px 12px;
               background: #edf2f7; border-radius: 20px; }}
    .kw-text {{ font-size: 13px; color: #4a5568; font-weight: 500; }}
    .kw-count {{ font-size: 11px; color: white; background: #718096;
               border-radius: 10px; padding: 1px 7px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th {{ background: #f7fafc; padding: 12px; text-align: left; font-weight: 600;
         color: #4a5568; border-bottom: 2px solid #e2e8f0; }}
    td {{ padding: 10px 12px; border-bottom: 1px solid #f0f0f0; }}
    td a {{ color: #3182ce; text-decoration: none; }}
    td a:hover {{ text-decoration: underline; }}
    .badge {{ padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
    .badge-Technology {{ background: #ebf8ff; color: #2b6cb0; }}
    .badge-Business {{ background: #f0fff4; color: #276749; }}
    .badge-Science {{ background: #faf5ff; color: #6b46c1; }}
    .badge-Society {{ background: #fff5f5; color: #c53030; }}
    .badge-Startup {{ background: #fffaf0; color: #c05621; }}
    .stats-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;
                margin-bottom: 24px; }}
    .stat-card {{ background: white; border-radius: 12px; padding: 20px; text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .stat-number {{ font-size: 36px; font-weight: 700; color: #667eea; }}
    .stat-label {{ font-size: 13px; color: #718096; margin-top: 4px; }}
    @media (max-width: 768px) {{
      .charts-grid {{ grid-template-columns: 1fr; }}
      .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
    }}
  </style>
</head>
<body>
  <div class="page-header">
    <h1>📊 週次ニュース分析レポート</h1>
    <div class="meta">{week_label} | {date_range} | 総記事数: {len(articles)}</div>
  </div>

  <div class="content">
    <!-- 統計サマリー -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-number">{len(articles)}</div>
        <div class="stat-label">総記事数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{len(category_counts)}</div>
        <div class="stat-label">カテゴリ数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{len(top_keywords)}</div>
        <div class="stat-label">抽出キーワード数</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{len(timeline_data)}</div>
        <div class="stat-label">集計日数</div>
      </div>
    </div>

    <!-- AI要約 -->
    <div class="section">
      <h2>🤖 AI による週次要約</h2>
      <div class="ai-summary">{ai_summary}</div>
    </div>

    <!-- チャート -->
    <div class="charts-grid">
      <div class="chart-box">
        <h3>📊 カテゴリ別記事数</h3>
        <canvas id="categoryChart" height="250"></canvas>
      </div>
      <div class="chart-box">
        <h3>📈 日別記事数 (時系列)</h3>
        <canvas id="timelineChart" height="250"></canvas>
      </div>
    </div>

    <!-- キーワード -->
    <div class="section">
      <h2>🏷️ トレンドキーワード</h2>
      <div class="keywords-grid">{keyword_items}</div>
    </div>

    <!-- 大局的分析 -->
    <div class="section">
      <h2>🔭 大局的分析・洞察</h2>
      <div class="macro-analysis">{macro_analysis}</div>
    </div>

    <!-- 記事一覧 -->
    <div class="section">
      <h2>📋 全記事一覧</h2>
      <table>
        <thead>
          <tr><th>日付</th><th>タイトル</th><th>カテゴリ</th><th>ソース</th></tr>
        </thead>
        <tbody>{article_rows}</tbody>
      </table>
    </div>
  </div>

  <script>
    // カテゴリ円グラフ
    new Chart(document.getElementById('categoryChart'), {{
      type: 'doughnut',
      data: {{
        labels: {cat_labels},
        datasets: [{{ data: {cat_values}, backgroundColor: {cat_colors} }}]
      }},
      options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom' }} }} }}
    }});

    // 時系列棒グラフ
    new Chart(document.getElementById('timelineChart'), {{
      type: 'bar',
      data: {{
        labels: {timeline_labels},
        datasets: [{{
          label: '記事数',
          data: {timeline_values},
          backgroundColor: 'rgba(102, 126, 234, 0.6)',
          borderColor: '#667eea',
          borderWidth: 1
        }}]
      }},
      options: {{
        responsive: true,
        scales: {{ y: {{ beginAtZero: true, ticks: {{ stepSize: 1 }} }} }}
      }}
    }});
  </script>
</body>
</html>"""
