# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is a Daily Trend Summary Mailer that fetches trending articles from Qiita and Zenn RSS feeds, summarizes them using Google Gemini API, and sends the summary via email using Gmail SMTP. It's designed to run automatically via GitHub Actions daily.

## Development Setup

The project uses Poetry for dependency management:

```bash
poetry install
poetry run python main.py
```

## Environment Configuration

Copy `.env.template` to `.env` and configure the following variables:
- `QIITA_RSS_URL`: Qiita trending RSS feed URL 
- `ZENN_RSS_URL`: Zenn trending RSS feed URL
- `GEMINI_API_KEY`: Google Gemini API key
- `GMAIL_APP_PASSWORD`: Gmail app password (not regular password)
- `SENDER_EMAIL`: Gmail sender address
- `RECEIVER_EMAIL`: Recipient email address

## Architecture

The application follows a modular pipeline architecture:

1. **Entry point**: `main.py` - Orchestrates the entire pipeline
2. **Data fetching**: `src/fetch_trends.py` - Retrieves RSS feeds from Qiita and Zenn
3. **Content processing**: `src/summarize.py` - Uses Google Gemini API to summarize articles
4. **Email delivery**: `src/send_email.py` - Sends HTML email via Gmail SMTP

**Note**: The current `send_email.py` uses Gmail SMTP, but the README mentions SendGrid. The codebase and GitHub Actions workflow use Gmail SMTP with `GMAIL_APP_PASSWORD`.

## Testing Individual Components

Each module can be tested independently by running them directly:

```bash
# Test RSS feed fetching
poetry run python src/fetch_trends.py

# Test summarization (requires GEMINI_API_KEY)
poetry run python src/summarize.py

# Test email sending (requires email credentials)
poetry run python src/send_email.py
```

## GitHub Actions

The project includes automated daily execution via `.github/workflows/daily_summary.yml`:
- Runs daily at UTC 23:00 (JST 08:00)
- Supports manual workflow dispatch
- Requires these GitHub Secrets: `GEMINI_API_KEY`, `GMAIL_APP_PASSWORD`, `SENDER_EMAIL`, `RECEIVER_EMAIL`

## Key Dependencies

- `feedparser`: RSS feed parsing
- `google-generativeai`: Gemini API integration  
- `python-dotenv`: Environment variable management
- Standard library: `smtplib`, `email.mime` for Gmail SMTP