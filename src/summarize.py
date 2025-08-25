import google.generativeai as genai
import os

def summarize_articles(articles, platform_name):
    """個別記事の詳細要約を生成（既存機能を保持）"""
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

def generate_overall_trend_summary(qiita_articles, zenn_articles):
    """全体のトレンド概要と領域別サマリーを生成"""
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-2.5-flash')

    # 全記事のタイトルと内容を収集
    all_articles_info = ""
    
    all_articles_info += "**Qiita記事:**\n"
    for article in qiita_articles:
        title = article['title']
        content = article.get('content', '')[:300] if article.get('content') else ''
        all_articles_info += f"- {title}\n"
        if content:
            all_articles_info += f"  概要: {content}...\n"
    
    all_articles_info += "\n**Zenn記事:**\n"
    for article in zenn_articles:
        title = article['title']
        content = article.get('content', '')[:300] if article.get('content') else ''
        all_articles_info += f"- {title}\n"
        if content:
            all_articles_info += f"  概要: {content}...\n"

    prompt = f"""以下はQiitaとZennから収集した今日のトレンド記事です：

{all_articles_info}

以下の構造で全体のトレンド分析を生成してください：

1. **今日のトレンド概要**
   - 全体的な傾向を2-3文で要約
   - 注目すべき技術動向があれば言及

2. **領域別分析**
   技術領域ごとに分類・分析（該当する記事がある場合のみ）：
   - 🤖 AI・機械学習
   - 🔒 セキュリティ
   - 💻 Web開発（フロントエンド・バックエンド）
   - 📱 モバイル開発
   - ☁️ クラウド・インフラ
   - 🛠 開発ツール・環境
   - 📊 データサイエンス・分析
   - その他の注目領域

各領域について：
- どのような記事があったか簡潔に記述
- その領域での注目ポイントや傾向

記事が少ない領域は省略し、実際にトレンドが見られる領域のみ取り上げてください。"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating overall trend summary: {e}")
        return f"全体トレンドの要約中にエラーが発生しました: {e}"

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
    dummy_qiita_articles = [
        {"title": "Pythonの新しい機能", "link": "https://example.com/python", "content": "Pythonの最新バージョンでは新しい機能が追加されました。"},
        {"title": "Web開発のトレンド", "link": "https://example.com/web", "content": "最新のWeb開発技術とフレームワークについて解説します。"},
        {"title": "AIの進化", "link": "https://example.com/ai", "content": "機械学習とAI技術の最新動向を紹介します。"},
    ]
    
    dummy_zenn_articles = [
        {"title": "TypeScriptベストプラクティス", "link": "https://example.com/typescript", "content": "TypeScriptでの効率的な開発手法を紹介します。"},
        {"title": "Dockerコンテナ活用法", "link": "https://example.com/docker", "content": "Dockerを使った開発環境の構築方法を解説します。"},
    ]
    
    print("Testing new functions...")
    print("=" * 50)
    
    # Test without API access - just show function structure works
    print("Functions imported successfully:")
    print("- summarize_articles: Available")
    print("- generate_overall_trend_summary: Available") 
    print("- summarize_articles_with_content: Available")
    
    print("\nTest data prepared:")
    print(f"Qiita articles: {len(dummy_qiita_articles)}")
    print(f"Zenn articles: {len(dummy_zenn_articles)}")
    
    print("\nNote: API functions require GEMINI_API_KEY to run actual summarization.")
