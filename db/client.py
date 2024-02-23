from prisma import Prisma

# Initialize the Prisma Client
db = Prisma()

async def connect():
    # Connect to the database
    await db.connect()

async def disconnect():
    # Disconnect from the database
    await db.disconnect()
