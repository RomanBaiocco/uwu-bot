import re
import json
import ring

from db import get_session, Guild, select

cache = {}


@ring.dict(cache)
async def get_guild_settings_cached(guild_id: str):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()

        guild_data = guild_to_dict(guild)
        return guild_data


async def get_guild_settings(guild_id: str):
    cached_guild_settings = await get_guild_settings_cached.get(guild_id)

    if cached_guild_settings is not None:
        return cached_guild_settings
    else:
        guild_settings = await get_guild_settings_cached(guild_id)
        return guild_settings


async def set_target(guild_id: str, target_tag: str):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()
        pattern = r"<@(\d+)>"

        match = re.search(pattern, target_tag)
        if match:
            target_id = match.group(1)
        else:
            target_id = None

        if target_id is None:
            raise ValueError("Invalid target")


        guild.target = target_id
        session.add(guild)
        session.commit()

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = guild_to_dict(
            guild
        )


async def set_level(guild_id: str, level: int):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()

        guild.level = level
        session.add(guild)
        session.commit()

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = guild_to_dict(
            guild
        )


async def set_webhook(guild_id: str, channel_id: str, webhook_url: str):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()

        webhooks = json.loads(guild.webhooks)
        webhooks[channel_id] = webhook_url
        guild.webhooks = json.dumps(webhooks)
        session.add(guild)
        session.commit()

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = guild_to_dict(
            guild
        )


async def mark_channel_off_limits(guild_id: str, channel_id: str):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()

        off_limits_channels = json.loads(guild.off_limits_channels)
        off_limits_channels.append(channel_id)
        guild.off_limits_channels = json.dumps(off_limits_channels)
        session.add(guild)
        session.commit()

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = guild_to_dict(
            guild
        )


async def mark_channel_on_limits(guild_id: str, channel_id: str):
    with get_session() as session:
        guild = session.exec(select(Guild).where(Guild.id == guild_id)).one()

        off_limits_channels = json.loads(guild.off_limits_channels)
        off_limits_channels.remove(channel_id)
        guild.off_limits_channels = json.dumps(off_limits_channels)
        session.add(guild)
        session.commit()

        cache[f"guild_management.get_guild_settings_cached:{guild_id}"] = guild_to_dict(
            guild
        )


async def initialize_guild_settings(guild_id: str):
    guild = Guild(id=guild_id, webhooks="{}", off_limits_channels="[]")

    with get_session() as session:
        session.add(guild)
        session.commit()


def guild_to_dict(guild: Guild):
    return {
        "id": guild.id,
        "target": guild.target,
        "level": guild.level,
        "webhooks": json.loads(guild.webhooks),
        "off_limits_channels": json.loads(guild.off_limits_channels),
    }
