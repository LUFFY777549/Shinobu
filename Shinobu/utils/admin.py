# Shinobu/utils/admin.py
import asyncio
from pyrogram.errors import FloodWait, RPCError

# -------- Get member info safely -------- #
async def get_member_status(client, chat_id: int, user_id: int):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status.lower()
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await get_member_status(client, chat_id, user_id)
    except Exception:
        return None


# -------- Check if admin -------- #
async def is_admin(client, chat_id: int, user_id: int) -> bool:
    status = await get_member_status(client, chat_id, user_id)
    return status in ["administrator", "creator", "owner"]


# -------- Check if owner -------- #
async def is_owner(client, chat_id: int, user_id: int) -> bool:
    status = await get_member_status(client, chat_id, user_id)
    return status in ["creator", "owner"]


# -------- Check if normal member -------- #
async def is_member(client, chat_id: int, user_id: int) -> bool:
    status = await get_member_status(client, chat_id, user_id)
    return status == "member"


# -------- Get all admins list -------- #
async def get_admins(client, chat_id: int):
    admins = []
    try:
        async for member in client.get_chat_members(chat_id, filter="administrators"):
            admins.append(member.user.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except RPCError:
        pass
    return admins