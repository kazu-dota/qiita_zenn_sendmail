import os
from dotenv import load_dotenv
from src.fetch_trends import fetch_qiita_trends, fetch_zenn_trends
from src.fetch_content import fetch_articles_content
from src.summarize import summarize_articles
from src.send_email import send_summary_email
from src.format_email import create_email_content

def main():
    load_dotenv() # .envファイルから環境変数を読み込む

    # 環境変数の取得
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not receiver_email:
        print("Error: SENDER_EMAIL or RECEIVER_EMAIL is not set in .env file.")
        return

    # Qiitaトレンドの取得
    print("Fetching Qiita trends...")
    qiita_articles = fetch_qiita_trends()
    
    # Qiita記事の内容を取得（上位5件）
    print("Fetching Qiita article contents...")
    qiita_articles_with_content = fetch_articles_content(qiita_articles, max_articles=5)
    
    # Qiitaトレンドの要約
    print("Summarizing Qiita trends...")
    qiita_summary = summarize_articles(qiita_articles_with_content, "Qiita")

    # Zennトレンドの取得
    print("Fetching Zenn trends...")
    zenn_articles = fetch_zenn_trends()
    
    # Zenn記事の内容を取得（上位5件）
    print("Fetching Zenn article contents...")
    zenn_articles_with_content = fetch_articles_content(zenn_articles, max_articles=5)
    
    # Zennトレンドの要約
    print("Summarizing Zenn trends...")
    zenn_summary = summarize_articles(zenn_articles_with_content, "Zenn")

    # メール内容の作成
    subject = "今日のQiitaとZennのトレンド要約"
    html_content = create_email_content(qiita_summary, zenn_summary)

    # メール送信
    print("Sending summary email...")
    send_summary_email(subject, html_content, receiver_email, sender_email)
    print("Done.")

if __name__ == "__main__":
    main()
