import os
import discord
from dotenv import load_dotenv
from uwuipy import uwuipy

from db.client import connect as db_connect, disconnect as db_disconnect
from uwu_levels import levels

from guild_management import (
    get_guild_settings,
    set_target,
    set_level,
    initialize_guild_settings,
)

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
        initialize_guild_settings()
        print(f"Joined {guild.name}!")

    async def on_message(self, message: discord.Message):
        try:
            if message.author.bot:
                return

            message_parts = message.content.split(" ")

            if message_parts[0] == PREFIX and len(message_parts) > 1:
                if message.guild is None:
                    await message.channel.send("UwU bot only works in servers!")
                    return

                guild_id = str(message.guild.id)

                command = message_parts[1]
                if command == "target":
                    if len(message_parts) < 3:
                        await message.channel.send("Please provide a target")
                        return

                    target = message_parts[2]
                    await set_target(guild_id, target)
                    await message.channel.send(f"Target set to {target}")
                elif command == "level":
                    if len(message_parts) < 3:
                        await message.channel.send("Please provide a level")
                        return

                    level = message_parts[2]
                    if not level.isdigit():
                        await message.channel.send("Level must be a number")
                        return

                    level = int(level)

                    if level < 0 or level > 5:
                        await message.channel.send("Level must be between 0 and 5")
                        return

                    await set_level(guild_id, level)
                    await message.channel.send(f"Level set to {level}")
                elif command == "dingdongbingbong":
                    await message.channel.send("Initializing guild settings...")
                    await initialize_guild_settings(guild_id)
                    await message.channel.send("Guild settings initialized!")
                else:
                    await message.channel.send("Unknown command")
            else:
                guild_settings = await get_guild_settings(str(message.guild.id))
                if not guild_settings.target or guild_settings.level == 0:
                    return

                level = levels[guild_settings.level - 1]

                uwu = uwuipy(
                    None,
                    level["stutter_chance"],
                    level["face_chance"],
                    level["action_chance"],
                    level["exclamation_chance"],
                    level["nsfw_actions"],
                )

                print(f"UwUifying message with level {guild_settings.level}")
                await message.delete()
                await message.channel.send(uwu.uwuify(message.content))
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
