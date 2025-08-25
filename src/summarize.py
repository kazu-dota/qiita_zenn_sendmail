import google.generativeai as genai
import os

def summarize_articles(articles, platform_name):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-2.5-flash')

    article_list_str = ""
    for i, article in enumerate(articles):
        article_info = f"{i+1}. {article['title']} ({article['link']})"
        
        # 記事の内容が含まれている場合は追加
        if 'content' in article and article['content']:
            content_preview = article['content'][:500] + "..." if len(article['content']) > 500 else article['content']
            article_info += f"\n   内容: {content_preview}"
        
        article_list_str += article_info + "\n\n"

    prompt = f"""以下の{platform_name}のトレンド記事のリストを要約してください。

{article_list_str}

要約の要求事項:
1. 各記事のタイトルとURLを含める
2. 記事の内容が提供されている場合は、その要点を簡潔にまとめる
3. 技術的なトピックや興味深いポイントを強調する
4. 読者にとって価値のある情報を抽出する
5. 全体を読みやすい形式で整理する"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing articles: {e}")
        return f"記事の要約中にエラーが発生しました: {e}"

def summarize_articles_with_content(articles_with_content, platform_name):
    """
    記事の内容を含む詳細な要約を生成する（新しい関数）
    
    Args:
        articles_with_content: 記事のタイトル、URL、内容を含むリスト
        platform_name: プラットフォーム名
        
    Returns:
        str: 要約テキスト
    """
    return summarize_articles(articles_with_content, platform_name)

if __name__ == "__main__":
    # テスト用のダミー記事データ
    dummy_articles = [
        {"title": "Pythonの新しい機能", "link": "https://example.com/python"},
        {"title": "Web開発のトレンド", "link": "https://example.com/web"},
        {"title": "AIの進化", "link": "https://example.com/ai"},
    ]
    platform = "テストプラットフォーム"
    summary = summarize_articles(dummy_articles, platform)
    print(f"\nSummary for {platform}:\n{summary}")
