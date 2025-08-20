# Daily Trend Summary Mailer

このプロジェクトは、QiitaとZennのトレンド記事を毎日取得し、Google Gemini APIを使用して要約し、指定されたメールアドレスに送信するシステムです。

## 機能

- QiitaとZennのトレンド記事をRSSフィードから取得
- 取得した記事リストをGemini APIで要約
- 要約された内容をSendGrid経由でメール送信
- GitHub Actionsによる日次自動実行

## 送信例

> 今日のトレンド要約
> Qiitaトレンド
> Qiitaのトレンド記事リストを要約します。今回は、AI/開発支援ツール、JavaScriptの基礎、セキュリティ、個人開発、インフラ、そして学習・概念理解に関する幅広いトピックが注目されています。

> ---

> **Qiitaトレンド記事要約**

> 今回のQiitaトレンドでは、**AIの活用**が特に目立ち、開発支援ツール、議事録作成、個人開発アプリなど多岐にわたります。また、**JavaScriptの基礎**や、**セキュリティ関連**の解説記事も人気です。

> 以下に記事をカテゴリ別にまとめます。

> ### AI・開発支援・自動化
> AIを活用した開発効率化やツールに関する記事が多数ランクインしています。
> * **1. お盆休みに「AIで議事録ツールをつくって。簡単なのでいいから」と言われたときのレシピ** (https://qiita.com/R_28/items/dbcce690a69bf7964423?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * AIを用いた議事録ツールの簡単な作成レシピ。
> * **4. Claude Code で GitHub Projects管理効率化** (https://qiita.com/hgkcho/items/50eb441e1ea88df33387?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * Claude Codeを活用したGitHub Projectsの管理効率化について。
> * **5. 【実案件使用】Cursorプロンプト × コード公開！ ②バグ修正編** (https://qiita.com/ShotaFukuyama/items/1d2f3dae7e1598a3a532?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * Cursorプロンプトを使ったバグ修正の実例とコード公開。
> * **10. 簡単！M365 Copilot で MS Docs MCP を使う** (https://qiita.com/aktsmm/items/928cbcbd61d1s54091e0?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * M365 CopilotでMicrosoft Docsの認定資格対策を行う方法。
> * **17. From Early Adopter to AI Skeptic... and Back** (https://qiita.com/qngdt/items/2171a9b4bcba762bdc8a?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * AIに対する懐疑から再び肯定するまでの個人の視点の変化。
> * **20. TDDでClaudeCodeのビックバン変更と向き合おう** (https://qiita.com/katamotokosuke/items/b254a793e2d5a6633841?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * TDD（テスト駆動開発）を用いてClaude Codeの大規模な変更に対応する方法。
> * **25. GitHub Copilotと仲良くなろう！** (https://qiita.com/im_yoneda/items/fae79d30df9ed900efa3?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * GitHub Copilotの活用術や親しみ方について。
> * **27. 【Amazon Q】AWSミートアップ参加レポート：LT初登壇！多彩な発表が教えてくれたゲーム制作裏側の苦労・工夫** (https://qiita.com/melknzw/items/03dfe8aa4c8b1fb8fa6f?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)
> * Amazon Qを含むAWSミートアップの参加レポート、ゲーム制作の裏側に関する発表内容。

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
