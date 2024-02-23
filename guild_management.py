import json
import ring

from db.client import connect as db_connect, disconnect as db_disconnect, db


cache = {}


@ring.dict(cache)
async def get_guild_settings_cached(guild_id: str):
    try:
        await db_connect()
        guild_settings = await db.guilds.find_unique(where={"id": guild_id})
        if guild_settings is None:
            raise ValueError(f"Guild settings for {guild_id} not found")

        return guild_settings

    finally:
        await db_disconnect()


async def get_guild_settings(guild_id: str):
    cached_guild_settings = await get_guild_settings_cached.get(guild_id)

    if cached_guild_settings is not None:
        print("Fetching guild settings from cache...")
        return cached_guild_settings
    else:
        print("Fetching guild settings from database...")
        guild_settings = await get_guild_settings_cached(guild_id)
        return guild_settings


async def set_target(guild_id: str, target: str):
    try:
        print(f"Setting target for guild {guild_id} to {target}")
        await db_connect()
        updated_guild = await db.guilds.update(
            where={"id": guild_id},
            data={"target": target},
        )

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = updated_guild

    finally:
        await db_disconnect()


async def set_level(guild_id: str, level: int):
    try:
        print(f"Setting level for guild {guild_id} to {level}")
        await db_connect()
        updated_guild = await db.guilds.update(
            where={"id": guild_id},
            data={"level": level},
        )

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = updated_guild

    finally:
        await db_disconnect()


async def set_webhook(guild_id: str, channel_id: str, webhook_url: str):
    try:
        print(f"Setting webhook for guild {guild_id} in channel {channel_id}")
        await db_connect()

        guild_settings = await get_guild_settings(guild_id)
        webhooks = guild_settings.webhooks

        print(f"Webhooks: {webhooks}")


        webhooks[channel_id] = webhook_url
        
        print(f"Webhooks: {webhooks}")

        updated_guild = await db.guilds.update(
            where={"id": guild_id},
            data={"webhooks": json.dumps(webhooks)},
        )

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = updated_guild

    finally:
        await db_disconnect()


async def initialize_guild_settings(guild_id: str):
    try:
        print(f"Initializing guild settings for guild {guild_id}")
        await db_connect()
        await db.guilds.create({"id": guild_id})

    except Exception as e:
        raise "Something went wrong while initializing guild settings"
    finally:
        await db_disconnect()
