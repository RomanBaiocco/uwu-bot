import os
import discord
from dotenv import load_dotenv

load_dotenv()

# Validate environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    print("BOT_TOKEN is not set")
    exit(1)

PREFIX = os.getenv("PREFIX")
if PREFIX is None:
    print("PREFIX is not set")
    exit(1)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_guild_join(self, guild: discord.Guild):
        print(f"Joined {guild.name}!")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        print(f"Received message: {message.content}")
        message_parts = message.content.split(" ")

        if message_parts[0] == PREFIX:
            await message.channel.send("uwu")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
