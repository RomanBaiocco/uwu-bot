import os
import requests
import discord
from dotenv import load_dotenv
from uwuipy import uwuipy

from logger import log_message
import traceback

from uwu_levels import levels

from guild_management import (
    get_guild_settings,
    set_target,
    set_level,
    set_webhook,
    initialize_guild_settings,
    mark_channel_off_limits,
    mark_channel_on_limits,
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
        log_message("info", f"Logged on as {self.user}!")

    async def on_guild_join(self, guild: discord.Guild):
        initialize_guild_settings()
        log_message("info", f"Joined {guild.name}", {"guild_id": str(guild.id)})

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

                elif command == "register":
                    force_arg = message_parts[2] if len(message_parts) > 2 else None
                    guild_settings = await get_guild_settings(guild_id)

                    if (str(message.channel.id) not in guild_settings["webhooks"]) or (
                        force_arg == "-f"
                    ):
                        new_webhook = await message.channel.create_webhook(
                            name="UwU Bot"
                        )

                        new_webhook_url = new_webhook.url
                        await set_webhook(
                            str(guild_id), str(message.channel.id), new_webhook_url
                        )

                        await message.channel.send("Channel registered")

                    else:
                        await message.channel.send("This channel is already registered")

                elif command == "dingdongbingbong":
                    await message.channel.send("Initializing guild settings...")
                    await initialize_guild_settings(guild_id)
                    await message.channel.send("Guild settings initialized!")
                elif command == "offlimits":
                    await mark_channel_off_limits(guild_id, message.channel.id)
                    await message.channel.send(
                        "This channel is now off limits for UwU bot"
                    )
                elif command == "onlimits":
                    await mark_channel_on_limits(guild_id, message.channel.id)
                    await message.channel.send(
                        "This channel is now on limits for UwU bot"
                    )
                else:
                    await message.channel.send("Unknown command")
            elif message_parts[0].startswith("-"):
                return
            else:
                guild_settings = await get_guild_settings(str(message.guild.id))
                if (
                    not guild_settings["target"]
                    or guild_settings["target"] != str(message.author.id)
                    or guild_settings["level"] == 0
                    or message.channel.id in guild_settings["off_limits_channels"]
                ):
                    return

                level = levels[guild_settings["level"] - 1]

                uwu = uwuipy(
                    None,
                    level["stutter_chance"],
                    level["face_chance"],
                    level["action_chance"],
                    level["exclamation_chance"],
                    level["nsfw_actions"],
                )

                if str(message.channel.id) in guild_settings["webhooks"]:
                    webhooks = guild_settings["webhooks"]
                    channel_id = str(message.channel.id)
                    webhook_url = webhooks[channel_id]

                    avatar_url = "https://cdn.discordapp.com/avatars/803083553411170305/62902b44f60c9277a01f9f102d15b040.webp?size=240"

                    if message.author.guild_avatar:
                        avatar_url = message.author.guild_avatar.url
                    elif message.author.avatar:
                        avatar_url = message.author.avatar.url

                    requests.post(
                        webhook_url,
                        json={
                            "username": message.author.display_name,
                            "avatar_url": avatar_url,
                            "content": uwu.uwuify(message.content),
                        },
                    )
                else:
                    await message.channel.send(uwu.uwuify(message.content))

                await message.delete()
        except ValueError as e:
            log_message(
                "error",
                "ValueError encountered",
                exception=str(e),
            )
            traceback.print_exc()

            return
        except Exception as e:
            error_info = {
                "guild_id": str(message.guild.id),
                "exception": str(e),
            }
            log_message("error", "Unexpected error occurred", **error_info)
            traceback.print_exc()

            await message.channel.send(f"An error occurred: {e}")


intents = discord.Intents.default()
intents.message_content = True
intents.webhooks = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
