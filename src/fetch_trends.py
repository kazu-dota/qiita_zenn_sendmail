import feedparser
import os

def fetch_qiita_trends():
    # QiitaのトレンドRSSフィードのURL
    # 公式のトレンドRSSフィードがないため、ここでは人気記事のRSSを使用します。
    # より正確なトレンドが必要な場合は、Qiita APIの利用を検討してください。
    qiita_rss_url = os.getenv("QIITA_RSS_URL", "https://qiita.com/popular-items/feed")
    feed = feedparser.parse(qiita_rss_url)
    articles = []
    for entry in feed.entries:
        articles.append({"title": entry.title, "link": entry.link})
    return articles

def fetch_zenn_trends():
    # ZennのトレンドRSSフィードのURL
    zenn_rss_url = os.getenv("ZENN_RSS_URL", "https://zenn.dev/topics/trend/feed")
    feed = feedparser.parse(zenn_rss_url)
    articles = []
    for entry in feed.entries:
        articles.append({"title": entry.title, "link": entry.link})
    return articles

if __name__ == "__main__":
    # 環境変数を読み込む (テスト実行時のみ)
    from dotenv import load_dotenv
    load_dotenv()

    print("Fetching Qiita trends...")
    qiita_articles = fetch_qiita_trends()
    for article in qiita_articles[:5]: # 上位5件を表示
        print(f"- {article['title']}: {article['link']}")

    print("\nFetching Zenn trends...")
    zenn_articles = fetch_zenn_trends()
    for article in zenn_articles[:5]: # 上位5件を表示
        print(f"- {article['title']}: {article['link']}")

