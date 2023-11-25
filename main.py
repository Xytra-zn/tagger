import os
import asyncio
from telethon.sync import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from pymongo import MongoClient
from admins import refresh_admins  # Import the function

# MongoDB connection
mongo_client = MongoClient(os.getenv("MONGODB_URL"))
db = mongo_client.get_database()
admins_collection = db["admins"]

# Initialize the Telethon client
client = TelegramClient(StringSession(os.getenv('TELETHON_SESSION')),
                        os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH'))

# Track ongoing tagging processes by chat_id
spam_chats = []

# Example event handling for tagging users
@client.on(events.NewMessage(pattern="^/(tagall|utag|@all|#all)"))
async def mention_all(event):
    chat_id = event.chat_id

    # Check if the chat is already in the process of tagging
    if chat_id in spam_chats:
        return await event.respond("Tagging is already in progress. Use /cancel to stop.")

    # Check if at least one argument is given
    if not event.pattern_match.group(1) and not event.is_reply:
        return await event.respond("Please provide at least one argument (either reply to a message or add a message after the command).")

    # Add the chat to the list of ongoing tagging processes
    spam_chats.append(chat_id)

    # Tag all participants in the chat
    async for user in client.iter_participants(chat_id):
        username = f"@{user.username}" if user.username else user.first_name
        await event.respond(f"Tagging {username}!")

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

# Example event handling for refreshing admin list
@client.on(events.NewMessage(pattern="^/reload$"))
async def reload_admins(event):
    chat_id = event.chat_id

    # Check if the user triggering the command is an admin
    is_admin = await refresh_admins(client, chat_id)
    if not is_admin:
        return await event.respond("Only admins can execute this command.")

    return await event.respond("Admin list refreshed.")

# Your existing event handlers and bot functionality

# Run the bot
client.start()
client.run_until_disconnected()
