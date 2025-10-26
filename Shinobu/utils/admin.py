# Shinobu/utils/admin.py
from pyrogram.errors import FloodWait, RPCError

# ---------------- Check if user is admin ---------------- #
async def is_admin(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False

# ---------------- Check if user is owner ---------------- #
async def is_owner(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status == "creator"
    except Exception:
        return False

# ---------------- Check if user is member (non-admin) ---------------- #
async def is_member(client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status == "member"
    except Exception:
        return False

# ---------------- Get all admins list ---------------- #
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