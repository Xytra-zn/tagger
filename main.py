import os
import asyncio
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Replace these with your actual environment variable names
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELETHON_SESSION = os.getenv('TELETHON_SESSION')

# Check if required environment variables are provided
if not (API_ID and API_HASH and BOT_TOKEN and TELETHON_SESSION):
    raise ValueError("API_ID, API_HASH, TOKEN, and TELETHON_SESSION are required.")

# Initialize the Telethon client
client = TelegramClient(StringSession(TELETHON_SESSION), API_ID, API_HASH)

# Track ongoing tagging processes by chat_id
spam_chats = []

# Example event handling for tagging users
@client.on(events.NewMessage(pattern="^/tagall"))
async def tag_all(event):
    chat_id = event.chat_id

    # Check if the chat is already in the process of tagging
    if chat_id in spam_chats:
        return await event.respond("Tagging is already in progress. Use /cancel to stop.")

    # Add the chat to the list of ongoing tagging processes
    spam_chats.append(chat_id)

    # Tag all participants in the chat
    async for user in client.iter_participants(chat_id):
        await event.respond(f"Tagging {user.first_name}!")

    # Remove the chat from the list after tagging is complete
    try:
        spam_chats.remove(chat_id)
    except ValueError:
        pass  # If chat_id is not in the list

# Example event handling for canceling tagging process
@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
    chat_id = event.chat_id

    # Check if the chat is in the list of ongoing tagging processes
    if chat_id in spam_chats:
        # Remove the chat from the list to stop tagging
        spam_chats.remove(chat_id)
        return await event.respond("Tagging process stopped.")
    else:
        return await event.respond("No ongoing tagging process to stop.")

# Add more event handlers and bot functionality as needed

# Run the bot
client.start()
client.run_until_disconnected()
