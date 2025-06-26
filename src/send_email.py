import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_summary_email(subject, content, to_email, from_email):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(f"Email sent successfully. Status Code: {response.status_code}")
        print(response.body)
        print(response.headers)
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
