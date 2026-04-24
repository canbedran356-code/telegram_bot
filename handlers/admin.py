from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus
from database import add_warning, remove_warning, get_warnings, clear_warnings, log_ban
from config import MAX_WARNINGS


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Komutu kullanan kişinin admin olup olmadığını kontrol et."""
    user = update.effective_user
    chat = update.effective_chat
    member = await context.bot.get_chat_member(chat.id, user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hedef kullanıcıyı mention, reply veya ID'den al."""
    message = update.message

    # Reply ile kullanıldıysa
    if message.reply_to_message:
        return message.reply_to_message.from_user

    # Mention entity'den kullanıcıyı al
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                return entity.user
            elif entity.type == "mention":
                username = message.text[entity.offset:entity.offset + entity.length]
                try:
                    chat = await context.bot.get_chat(username)
                    return chat
                except Exception:
                    pass

    # ID ile
    if context.args:
        arg = context.args[0]
        if arg.lstrip("-").isdigit():
            try:
                member = await context.bot.get_chat_member(
                    update.effective_chat.id, int(arg)
                )
                return member.user
            except Exception:
                return None
    return None

# ─────────────────────────────────────────────
# BAN
# ─────────────────────────────────────────────

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı. Reply at veya @kullanici yaz.")
        return

    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "Belirtilmedi"

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        log_ban(update.effective_chat.id, target.id, reason, update.effective_user.id)
        clear_warnings(update.effective_chat.id, target.id)
        await update.message.reply_text(
            f"🔨 *{target.full_name}* banlandı.\n📝 Sebep: {reason}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ban işlemi başarısız: {e}")


# ─────────────────────────────────────────────
# UNBAN
# ─────────────────────────────────────────────

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    try:
        await context.bot.unban_chat_member(
            update.effective_chat.id, target.id, only_if_banned=True
        )
        await update.message.reply_text(
            f"✅ *{target.full_name}* banı kaldırıldı.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Unban başarısız: {e}")


# ─────────────────────────────────────────────
# WARN
# ─────────────────────────────────────────────

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "Belirtilmedi"
    count = add_warning(update.effective_chat.id, target.id, reason)

    if count >= MAX_WARNINGS:
        # Otomatik ban
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        clear_warnings(update.effective_chat.id, target.id)
        await update.message.reply_text(
            f"🔨 *{target.full_name}* {MAX_WARNINGS} uyarıya ulaştı ve otomatik olarak banlandı!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"⚠️ *{target.full_name}* uyarıldı. ({count}/{MAX_WARNINGS})\n📝 Sebep: {reason}",
            parse_mode="Markdown"
        )


# ─────────────────────────────────────────────
# UNWARN
# ─────────────────────────────────────────────

async def unwarn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    count = remove_warning(update.effective_chat.id, target.id)
    await update.message.reply_text(
        f"✅ *{target.full_name}* için bir uyarı kaldırıldı. Kalan: {count}/{MAX_WARNINGS}",
        parse_mode="Markdown"
    )


# ─────────────────────────────────────────────
# MUTE
# ─────────────────────────────────────────────

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    # Süre argümanı (dakika)
    duration = 10  # varsayılan
    if len(context.args) > 1:
        try:
            duration = int(context.args[1])
        except ValueError:
            pass

    until = datetime.now() + timedelta(minutes=duration)

    try:
        from telegram import ChatPermissions
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            target.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until
        )
        await update.message.reply_text(
            f"🔇 *{target.full_name}* {duration} dakika susturuldu.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Mute başarısız: {e}")


# ─────────────────────────────────────────────
# UNMUTE
# ─────────────────────────────────────────────

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu komutu sadece adminler kullanabilir.")
        return

    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    try:
        from telegram import ChatPermissions
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            target.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(
            f"🔊 *{target.full_name}* susturması kaldırıldı.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Unmute başarısız: {e}")


# ─────────────────────────────────────────────
# WARNS (liste)
# ─────────────────────────────────────────────

async def warn_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = await get_target_user(update, context)
    if not target:
        await update.message.reply_text("❌ Kullanıcı bulunamadı.")
        return

    warnings = get_warnings(update.effective_chat.id, target.id)
    if not warnings:
        await update.message.reply_text(
            f"✅ *{target.full_name}* hiç uyarısı yok.",
            parse_mode="Markdown"
        )
        return

    lines = [f"⚠️ *{target.full_name}* uyarıları ({len(warnings)}/{MAX_WARNINGS}):"]
    for i, w in enumerate(warnings, 1):
        lines.append(f"{i}. {w['reason'] or 'Sebep yok'} — {w['created_at']}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
