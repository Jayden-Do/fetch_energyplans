
from motor.motor_asyncio import AsyncIOMotorClient


# Replace the placeholder with your Atlas connection string
uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = AsyncIOMotorClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["mainappdatabase"]


async def get_database():
    return db
