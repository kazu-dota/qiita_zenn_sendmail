import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_summary_email(subject, content, to_email, from_email):
    # メール本文をMIMETextオブジェクトとして作成
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        # GmailのSMTPサーバーに接続
        # ポート587はTLS暗号化を使用
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.ehlo() # EHLOコマンドでSMTPサーバーに自己紹介
            smtp_server.starttls() # TLS暗号化を開始
            smtp_server.ehlo() # TLS開始後に再度EHLO

            # Gmailアカウントにログイン
            # パスワードはアプリパスワードを使用
            smtp_server.login(from_email, os.getenv('GMAIL_APP_PASSWORD'))

            # メールを送信
            smtp_server.send_message(msg)
            print("Email sent successfully using Gmail SMTP.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # テスト用のダミーデータ
    test_subject = "テスト要約メール"
    test_content = "<h1>これはテストメールです</h1><p>要約内容がここに表示されます。</p>"
    test_to_email = "your.email@example.com" # ここを実際のメールアドレスに置き換えてください
    test_from_email = "your.email@example.com" # ここを実際のメールアドレスに置き換えてください

    # .envファイルから環境変数を読み込む（テスト時のみ）
    from dotenv import load_dotenv
    load_dotenv()

    print("Sending test email...")
    send_summary_email(test_subject, test_content, test_to_email, test_from_email)
