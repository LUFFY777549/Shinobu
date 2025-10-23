from motor.motor_asyncio import AsyncIOMotorClient
#MONGO_CLIENT
MONGO_URI = "mongodb+srv://sufyan532011:5042@auctionbot.5ms20.mongodb.net/?retryWrites=true&w=majority&appName=AuctionBot"
mongo_client = AsyncIOMotorClient(MONGO_URI)
DB = mongo_client["Shinobu"]
#All Database
Users = DB["USERS"]
Banned = []