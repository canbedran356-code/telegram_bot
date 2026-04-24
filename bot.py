import logging
import os
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ChatMemberHandler
)
from config import BOT_TOKEN
from handlers.admin import (
    ban_user, unban_user, warn_user, unwarn_user,
    mute_user, unmute_user, warn_list
)
from handlers.filters import check_message
from handlers.flood import check_flood
from database import init_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "🛡️ *Security Bot aktif!*\n\n"
        "Komutlar:\n"
        "/ban @kullanici - Kullanıcıyı banla\n"
        "/unban @kullanici - Banı kaldır\n"
        "/warn @kullanici - Uyarı ver\n"
        "/unwarn @kullanici - Uyarıyı kaldır\n"
        "/mute @kullanici [dakika] - Sustur\n"
        "/unmute @kullanici - Susturmayı kaldır\n"
        "/warns @kullanici - Uyarı listesi",
        parse_mode="Markdown"
    )


def main():
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    # Komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("warn", warn_user))
    app.add_handler(CommandHandler("unwarn", unwarn_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))
    app.add_handler(CommandHandler("warns", warn_list))

    # Mesaj filtreleri (flood + yasaklı kelime/link)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_flood
    ), group=1)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        check_message
    ), group=2)

    logger.info("Bot başlatılıyor...")
    app.run_polling(allowed_updates=["message", "chat_member"])


if __name__ == "__main__":
    main()
