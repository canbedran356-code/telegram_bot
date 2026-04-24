import time
from collections import defaultdict
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from config import FLOOD_MAX_MESSAGES, FLOOD_TIME_WINDOW

# {(chat_id, user_id): [timestamp1, timestamp2, ...]}
flood_tracker = defaultdict(list)


async def check_flood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    now = time.time()
    key = (chat_id, user_id)

    # Eski mesajları temizle
    flood_tracker[key] = [
        t for t in flood_tracker[key]
        if now - t < FLOOD_TIME_WINDOW
    ]
    flood_tracker[key].append(now)

    if len(flood_tracker[key]) > FLOOD_MAX_MESSAGES:
        flood_tracker[key] = []  # Sayacı sıfırla

        try:
            from datetime import datetime, timedelta
            until = datetime.now() + timedelta(minutes=5)
            await context.bot.restrict_chat_member(
                chat_id,
                user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until
            )
            await update.message.reply_text(
                f"🚨 *{update.effective_user.full_name}* flood yaptığı için 5 dakika susturuldu!",
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Flood mute hatası: {e}")
