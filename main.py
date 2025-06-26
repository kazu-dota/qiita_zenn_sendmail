import os
from dotenv import load_dotenv
from src.fetch_trends import fetch_qiita_trends, fetch_zenn_trends
from src.summarize import summarize_articles
from src.send_email import send_summary_email

def main():
    load_dotenv() # .envファイルから環境変数を読み込む

    # 環境変数の取得
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not sender_email or not receiver_email:
        print("Error: SENDER_EMAIL or RECEIVER_EMAIL is not set in .env file.")
        return

    # Qiitaトレンドの取得と要約
    print("Fetching Qiita trends...")
    qiita_articles = fetch_qiita_trends()
    qiita_summary = summarize_articles(qiita_articles, "Qiita")

    # Zennトレンドの取得と要約
    print("Fetching Zenn trends...")
    zenn_articles = fetch_zenn_trends()
    zenn_summary = summarize_articles(zenn_articles, "Zenn")

    # メール内容の作成
    subject = "今日のQiitaとZennのトレンド要約"
    html_content = f"<h1>今日のトレンド要約</h1>"
    html_content += f"<h2>Qiitaトレンド</h2><p>{qiita_summary.replace("\n", "<br>")}</p>"
    html_content += f"<h2>Zennトレンド</h2><p>{zenn_summary.replace("\n", "<br>")}</p>"

    # メール送信
    print("Sending summary email...")
    send_summary_email(subject, html_content, receiver_email, sender_email)
    print("Done.")

if __name__ == "__main__":
    main()
