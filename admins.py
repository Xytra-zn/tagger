import os
from pymongo import MongoClient
from telethon.sync import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

# MongoDB connection
mongo_client = MongoClient(os.getenv("MONGODB_URL"))
db = mongo_client.get_database()
admins_collection = db["admins"]

# Function to refresh admin list
async def refresh_admins(client, chat_id):
    try:
        participant = await client(GetParticipantRequest(chat_id, client.get_me().id))
        if not isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return False
    except UserNotParticipantError:
        return False

    current_admins = [participant.id for participant in await client.get_participants(chat_id, filter=ChannelParticipantAdmin)]
    admins_collection.replace_one({"chat_id": chat_id}, {"chat_id": chat_id, "admins": current_admins}, upsert=True)
    return True
  
