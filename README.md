# Daily Trend Summary Mailer

このプロジェクトは、QiitaとZennのトレンド記事を毎日取得し、Google Gemini APIを使用して要約し、指定されたメールアドレスに送信するシステムです。

## 機能

- QiitaとZennのトレンド記事をRSSフィードから取得
- 取得した記事リストをGemini APIで要約
- 要約された内容をSendGrid経由でメール送信
- GitHub Actionsによる日次自動実行

## 送信例
![Uploading image.png…]()

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-username/trend-summary-mailer.git
cd trend-summary-mailer
```

### 2. 依存関係のインストール

Poetryを使用して依存関係を管理します。Poetryがインストールされていない場合は、[公式ドキュメント](https://python-poetry.org/docs/#installation)を参照してインストールしてください。

```bash
poetry install
```

### 3. 環境変数の設定

`.env.template` ファイルをコピーして `.env` ファイルを作成し、必要なAPIキーとメールアドレスを設定します。

```bash
cp .env.template .env
```

`.env` ファイルを以下のように編集してください。

```
QIITA_RSS_URL=https://qiita.com/popular-items/feed
ZENN_RSS_URL=https://zenn.dev/topics/trend/feed
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
SENDER_EMAIL=your-sender-email@example.com
RECEIVER_EMAIL=your-receiver-email@example.com
```

- `QIITA_RSS_URL`: QiitaのトレンドRSSフィードのURL。デフォルトで人気記事のRSSを設定しています。
- `ZENN_RSS_URL`: ZennのトレンドRSSフィードのURL。
- `GEMINI_API_KEY`: Google Gemini APIのキー。 [Google AI Studio](https://aistudio.google.com/app/apikey) で取得できます。
- `SENDGRID_API_KEY`: SendGridのAPIキー。 [SendGrid](https://sendgrid.com/) でアカウントを作成し、APIキーを生成してください。
- `SENDER_EMAIL`: 送信元メールアドレス。SendGridで認証済みのSender Emailである必要があります。
- `RECEIVER_EMAIL`: 受信者メールアドレス。

### 4. GitHub Secretsの設定

GitHub Actionsで自動実行するために、以下の環境変数をGitHubリポジトリのSecretsに設定する必要があります。

- `GEMINI_API_KEY`
- `SENDGRID_API_KEY`
- `SENDER_EMAIL`
- `RECEIVER_EMAIL`

リポジトリの `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret` から追加してください。

## 実行方法

### ローカルでの実行

```bash
poetry run python main.py
```

### GitHub Actionsでの自動実行

リポジトリにプッシュすると、`.github/workflows/daily_summary.yml` に設定されたスケジュール（デフォルトでは毎日UTC 11:00、日本時間午前8時）で自動的に実行されます。手動で実行したい場合は、GitHub Actionsのワークフローページから `Run workflow` をクリックしてください。

## 注意事項

- QiitaのトレンドRSSフィードは公式に提供されていないため、人気記事のRSSを使用しています。より正確なトレンドが必要な場合は、Qiita APIの利用を検討してください。
- SendGridのAPIキーとSender Emailは、SendGridの認証済みである必要があります。
