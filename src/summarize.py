import google.generativeai as genai
import os

def summarize_articles(articles, platform_name):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-2.5-flash')

    article_list_str = ""
    for i, article in enumerate(articles):
        article_list_str += f"{i+1}. {article['title']} ({article['link']})\n"

    prompt = f"以下の{platform_name}のトレンド記事のリストを要約してください。\n\n{article_list_str}\n\n要約は、各記事のタイトルとURLを含み、簡潔にまとめてください。"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing articles: {e}")
        return f"記事の要約中にエラーが発生しました: {e}"

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
