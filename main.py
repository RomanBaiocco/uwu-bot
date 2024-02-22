import os
import discord
from dotenv import load_dotenv

load_dotenv()

# Validate environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    print("BOT_TOKEN is not set")
    exit(1)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
