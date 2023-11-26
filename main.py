import os
from telegram.ext import Updater, CommandHandler, MessageHandler

# Track ongoing tagging processes by chat_id
spam_chats = set()

# Example event handling for tagging users
def mention_all(update, context):
    chat_id = update.message.chat_id

    # Check if the chat is already in the process of tagging
    if chat_id in spam_chats:
        update.message.reply_text("Tagging is already in progress. Use /cancel to stop.")
        return

    # Check if at least one argument is given
    if not context.args and not update.message.reply_to_message:
        update.message.reply_text("Please provide at least one argument (either reply to a message or add a message after the command).")
        return

    # Check if the bot is an admin
    if not context.bot.get_chat_member(chat_id, context.bot.id).status in ['administrator', 'creator']:
        update.message.reply_text("I need to be an admin to run this command.")
        return

    # Check if the user is an admin
    if not context.bot.get_chat_member(chat_id, update.message.from_user.id).status in ['administrator', 'creator']:
        update.message.reply_text("You need to be an admin to run this command.")
        return

    # Add the chat to the list of ongoing tagging processes
    spam_chats.add(chat_id)

    # Tag all participants in the chat
    for for member in context.bot.get_chat_members(chat_id):
        if member.user:
            username = f"@{member.user.username}" if member.user.username else member.user.first_name
            update.message.reply_text(f"Tagging {username}!")

    # Remove the chat from the list after tagging is complete
    spam_chats.remove(chat_id)

# Example event handling for canceling tagging process
def cancel_spam(update, context):
    chat_id = update.message.chat_id

    # Check if the chat is in the list of ongoing tagging processes
    if chat_id in spam_chats:
        # Remove the chat from the list to stop tagging
        spam_chats.remove(chat_id)
        update.message.reply_text("Tagging process stopped.")
    else:
        update.message.reply_text("No ongoing tagging process to stop.")

# Set up the Telegram bot
updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler("tagall", mention_all))
dispatcher.add_handler(CommandHandler("cancel", cancel_spam))

# Start the bot
updater.start_polling()
updater.idle()
