import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set up any additional configurations needed for Heroku
# For example, setting environment variables
os.environ.setdefault("TELEGRAM_API_ID", "your_api_id")
os.environ.setdefault("TELEGRAM_API_HASH", "your_api_hash")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "your_bot_token")
os.environ.setdefault("TELETHON_SESSION", "your_telethon_session")

# You can add more Heroku-specific configurations if needed
