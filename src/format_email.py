import markdown
from markdown.extensions import tables, toc, codehilite

def markdown_to_html(markdown_text):
    """
    Markdownテキストを適切にフォーマットされたHTMLに変換する
    
    Args:
        markdown_text (str): Markdownフォーマットのテキスト
        
    Returns:
        str: HTMLフォーマットされたテキスト
    """
    if not markdown_text:
        return ""
    
    # Markdownの拡張を設定
    extensions = [
        'tables',        # テーブル対応
        'toc',          # 目次対応
        'codehilite',   # コードシンタックスハイライト
        'fenced_code',  # フェンスコードブロック対応
        'nl2br'         # 改行を<br>に自動変換
    ]
    
    # MarkdownをHTMLに変換
    html = markdown.markdown(markdown_text, extensions=extensions)
    
    return html

def create_email_content(qiita_summary, zenn_summary):
    """
    Qiita・Zennの要約からHTMLメール本文を作成する
    
    Args:
        qiita_summary (str): Qiitaトレンドの要約（Markdown形式）
        zenn_summary (str): Zennトレンドの要約（Markdown形式）
        
    Returns:
        str: HTMLフォーマットされたメール本文
    """
    # Markdownを適切なHTMLに変換
    qiita_html = markdown_to_html(qiita_summary)
    zenn_html = markdown_to_html(zenn_summary)
    
    # HTMLメール本文を構築
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
            今日のトレンド要約
        </h1>
        
        <h2 style="color: #e74c3c; margin-top: 30px;">
            📈 Qiitaトレンド
        </h2>
        <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #17a2b8; margin-bottom: 20px;">
            {qiita_html}
        </div>
        
        <h2 style="color: #28a745; margin-top: 30px;">
            📊 Zennトレンド
        </h2>
        <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #28a745;">
            {zenn_html}
        </div>
        
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #dee2e6;">
        <p style="font-size: 12px; color: #6c757d; text-align: center;">
            このメールは自動生成されました。
        </p>
    </body>
    </html>
    """
    
    return html_content.strip()

if __name__ == "__main__":
    # テスト用のMarkdownテキスト
    test_qiita_summary = """
    **今日の注目記事**

    1. **Python入門ガイド** - https://example.com/python
       - 基本的な文法から応用まで
       - サンプルコード付き

    2. **React最新情報** - https://example.com/react
       - 新機能の紹介
       - パフォーマンス改善のポイント
    """
    
    test_zenn_summary = """
    **人気の技術記事**

    1. **TypeScript実践テクニック** - https://example.com/typescript
       - 型安全性の向上
       - 実用的な使用例

    2. **Docker入門** - https://example.com/docker
       - コンテナ化の基礎
       - 開発環境の構築方法
    """
    
    html_output = create_email_content(test_qiita_summary, test_zenn_summary)
    print("Generated HTML content:")
    print(html_output)