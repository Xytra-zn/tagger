import os

# Set up Heroku environment variables
os.environ.setdefault("TELEGRAM_API_ID", "your_api_id")
os.environ.setdefault("TELEGRAM_API_HASH", "your_api_hash")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "your_bot_token")
os.environ.setdefault("TELETHON_SESSION", "your_telethon_session")
