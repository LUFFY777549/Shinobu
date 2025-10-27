from motor.motor_asyncio import AsyncIOMotorClient
#MONGO_CLIENT
MONGO_URI = "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot"
mongo_client = AsyncIOMotorClient(MONGO_URI)
DB = mongo_client["Shinobu"]
#All Database
tag_collection = DB["active_tags"]
Users = DB["USERS"]
Groups = DB["GROUPS"]
Banned = []

# ✅ Get all groups as list
async def get_all_groups():
    return await groups_collection.find().to_list(length=None)

# ✅ Start tagging
async def start_tag(chat_id: int, user_id: int, text: str = None):
    await tag_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "chat_id": chat_id,
            "user_id": user_id,
            "text": text,
            "active": True
        }},
        upsert=True
    )

# ✅ Stop tagging
async def stop_tag(chat_id: int):
    await tag_collection.delete_one({"chat_id": chat_id})

# ✅ Check if active
async def is_tagging_active(chat_id: int):
    data = await tag_collection.find_one({"chat_id": chat_id})
    return bool(data and data.get("active", False))

# ✅ Get tag data
async def get_tag_data(chat_id: int):
    return await tag_collection.find_one({"chat_id": chat_id})

# ✅ Count total users
async def get_total_users():
    return await users_collection.count_documents({})

# ✅ Count total groups
async def get_total_groups():
    return await groups_collection.count_documents({})