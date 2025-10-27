from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_admin(bot: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        status = member.status
        logger.info(f"Checking admin status for user {user_id} in chat {chat_id}: Status = {status}")

        # ✅ Pyrogram v2.2.9 uses only ADMINISTRATOR and OWNER
        if status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True

        # Extra fallback string check (safe for future/past versions)
        if str(status).lower() in ["administrator", "owner", "creator"]:
            return True

        return False

    except Exception as e:
        logger.error(
            f"Error checking admin status for user {user_id} in chat {chat_id}: "
            f"{type(e).__name__}: {e}"
        )
        return False