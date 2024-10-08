from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


print("DB URL : "+settings.DATABASE_URL)
print("DATABASE : "+settings.MONGO_INITDB_DATABASE)

client = AsyncIOMotorClient(settings.DATABASE_URL)

db= client.get_database(settings.MONGO_INITDB_DATABASE)

Users = db.get_collection("Users")
Speakers = db.get_collection("Speakers")
