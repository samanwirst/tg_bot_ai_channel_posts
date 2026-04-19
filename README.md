# Telegram AI Channel Posts Bot

A lightweight Telegram bot that generates and publishes channel posts with OpenAI on a schedule.

The bot is focused on short motivational phrases and can auto-post every hour to a configured Telegram channel.

## What It Does

- Generates post text with OpenAI (`gpt-3.5-turbo` in current code).
- Uses prompt context from:
  - `examples.json` (style/reference examples)
  - `posted.json` (already published posts, to reduce repetition)
- Sends generated text directly to your Telegram channel.
- Supports manual posting and start/stop control via admin commands.
- Keeps only the latest 30 generated entries in `posted.json`.

## How It Works

1. Bot starts with `aiogram`.
2. On startup, it loads:
   - `examples.json` -> `examples` list
   - `posted.json` -> `posted` list
3. Admin can control behavior through bot commands:
   - `/post` -> send one post immediately
   - `/start` -> start hourly posting loop
   - `/stop` -> stop hourly posting loop
4. Every generation result is appended to `posted.json`.

## Project Structure

- `main.py` - bot handlers, scheduling loop, posting logic
- `chat_gpt_manager.py` - OpenAI request wrapper
- `config.py` - environment-based config
- `json_db_tool.py` - JSON read/write helper
- `examples.json` - prompt style examples
- `posted.json` - generated post history
- `Dockerfile`, `docker-compose.yml` - containerized run

## Requirements

- Python 3.11+
- Telegram bot token
- OpenAI API key
- A Telegram channel where the bot has posting permissions

Dependencies from `requirements.txt`:

- `aiogram==2.25`
- `openai==0.28`

## Environment Variables

Create a `.env` file in the project root:

```dotenv
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
CHANNEL_ID=@your_channel_username_or_-100xxxxxxxxxx
ADMIN_LIST=123456789,987654321
```

### Notes on Variables

- `CHANNEL_ID` can be `@channel_name` or numeric chat ID (`-100...`).
- `ADMIN_LIST` is currently treated as a raw string in code (`if str(user_id) in ADMIN_LIST`), so keep it clean and predictable (comma-separated IDs without spaces).

## Local Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Docker Run

```bash
docker compose up --build -d
```

The compose setup expects environment variables from `.env`:

```yaml
services:
  bot:
    build: .
    env_file:
      - .env
    restart: always
```

## Bot Commands

- `/start` - start auto-posting every 3600 seconds
- `/stop` - stop auto-posting loop
- `/post` - publish one post immediately

Only users from `ADMIN_LIST` can trigger these commands.

## Data Files Format

`examples.json`:

```json
{
  "examples": [
    "example phrase 1",
    "example phrase 2"
  ]
}
```

`posted.json`:

```json
{
  "posted": [
    "already published phrase 1",
    "already published phrase 2"
  ]
}
```

## Known Limitations

- OpenAI integration is implemented with the legacy `openai==0.28` interface.
- If generation fails, the returned error text may be stored in `posted.json` (current behavior in `main.py`).
- The scheduler loop runs inside command flow and is intentionally simple for a small single-bot deployment.

## Project Context

This repository is a small practical automation bot for Telegram channel posting with AI-generated text.
