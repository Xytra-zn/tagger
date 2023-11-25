import os
import asyncio
from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

# Replace these with your actual environment variable names
API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELETHON_SESSION = os.getenv('TELETHON_SESSION')

# Check if required environment variables are provided
if not (API_ID and API_HASH and BOT_TOKEN and TELETHON_SESSION):
    raise ValueError("TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, and TELETHON_SESSION are required.")

# Initialize the Telethon client
client = TelegramClient(StringSession(TELETHON_SESSION), API_ID, API_HASH)

# Track ongoing tagging processes by chat_id
spam_chats = []

@client.on(events.NewMessage(pattern="^/tagall"))
@client.on(events.NewMessage(pattern="^@all"))
@client.on(events.NewMessage(pattern="^#all"))
async def tag_all(event):
    chat_id = event.chat_id

    # Check if the chat is already in the process of tagging
    if chat_id in spam_chats:
        return await event.respond("Tagging is already in progress. Use /cancel to stop.")

    # Add the chat to the list of ongoing tagging processes
    spam_chats.append(chat_id)

    # Tag all participants in the chat
    try:
        admins = await client.get_participants(chat_id, filter=ChannelParticipantAdmin)
        await event.respond(f"ALL USERS TAGGING PROCESS STARTED... STARTED BY: {event.sender_id} {event.sender.username}")

        async for user in client.iter_participants(chat_id):
            if user.id == event.sender_id or user.bot:
                continue

            if user.username:
                await event.respond(f"@{user.username}")
            else:
                await event.respond(user.first_name)

        await event.respond(f"TAGGING PROCESS COMPLETED. TOTAL NUMBER OF USERS TAGGED: {len(admins)}")
    except Exception as e:
        await event.respond(f"Error: {str(e)}")

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
