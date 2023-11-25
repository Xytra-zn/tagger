import os
from pymongo import MongoClient

# MongoDB connection (removed since we're not using it)

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

    # Check if the bot is an admin
    if not await client.is_bot_admin(chat_id):
        return await event.respond("I need to be an admin to run this command.")

    # Check if the user is an admin
    if not await client.is_user_admin(chat_id, event.sender_id):
        return await event.respond("You need to be an admin to run this command.")

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

# Run the bot
try:
    client.start()
    client.run_until_disconnected()
finally:
    # Close MongoDB client connection (removed since we're not using it)
