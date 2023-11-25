from pymongo import MongoClient

async def refresh_admins(client, chat_id):
    try:
        admins = await client.get_participants(chat_id, filter=ChannelParticipantAdmin)
        admin_ids = [admin.id for admin in admins]
        
        # Save admin IDs to MongoDB
        mongo_client = MongoClient(os.getenv("MONGODB_URL"))
        db = mongo_client.get_database()
        admins_collection = db["admins"]
        admins_collection.update_one({"chat_id": chat_id}, {"$set": {"admin_ids": admin_ids}}, upsert=True)

        return True
    except Exception as e:
        print(f"Error refreshing admins: {e}")
        return False
