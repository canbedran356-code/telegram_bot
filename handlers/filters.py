import re
from telegram import Update
from telegram.ext import ContextTypes
from config import BANNED_WORDS, BANNED_LINKS, ALLOW_LINKS

# Basit URL regex
URL_PATTERN = re.compile(
    r"(https?://|www\.)\S+|t\.me/\S+",
    re.IGNORECASE
)


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    # ─── Yasaklı kelime kontrolü ───
    for word in BANNED_WORDS:
        if word and word in text:
            try:
                await update.message.delete()
                await update.effective_chat.send_message(
                    f"🚫 *{update.effective_user.full_name}* yasaklı kelime içeren mesaj gönderdi ve silindi.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Silme hatası: {e}")
            return

    # ─── Link kontrolü ───
    urls = URL_PATTERN.findall(update.message.text)
    if urls:
        if not ALLOW_LINKS:
            # Tüm linkler yasak
            try:
                await update.message.delete()
                await update.effective_chat.send_message(
                    f"🔗 *{update.effective_user.full_name}* link gönderdi, bu grupta link paylaşımı yasak.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Link silme hatası: {e}")
            return
        else:
            # Sadece belirli domainler yasak
            full_text = update.message.text.lower()
            for banned in BANNED_LINKS:
                if banned and banned in full_text:
                    try:
                        await update.message.delete()
                        await update.effective_chat.send_message(
                            f"🔗 *{update.effective_user.full_name}* yasaklı link içeren mesaj gönderdi.",
                            parse_mode="Markdown"
                        )
                    except Exception as e:
                        print(f"Yasaklı link silme hatası: {e}")
                    return
