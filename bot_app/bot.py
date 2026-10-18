import telebot
import secrets
from django.conf import settings
from .models import User

bot = telebot.TeleBot(settings.BOT_TOKEN)

def run_bot():
    print("Бот запущен...")
    bot.infinity_polling()

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_or_create_user(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    
    user, created = User.objects.get_or_create(
        telegram_id=user_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "referral_code": secrets.token_urlsafe(6)
        }
    )
    if not created:
        user.username = username
        user.first_name = first_name
        user.save()
    return user

# --- КОМАНДЫ БОТА ---

@bot.message_handler(commands=["start"])
def cmd_start(message):
    user = get_or_create_user(message)
    if user.is_banned:
        return

    parts = message.text.split(maxsplit=1)
    payload = parts[1] if len(parts) > 1 else None

    # ЛОГИКА КУРСА
    if payload and payload.startswith("course_"):
        course_code = payload.replace("course_", "")
        teacher = User.objects.filter(course_code=course_code).first()
        
        if teacher:
            try:
                bot.send_message(
                    teacher.telegram_id,
                    f"🔥 <b>Новый ученик на курсе Python!</b>\n\n"
                    f"Имя: {user.first_name}\n"
                    f"Юзернейм: @{user.username or 'нет'}",
                    parse_mode="HTML"
                )
            except Exception:
                pass
            
            bot.send_message(
                user.telegram_id,
                f"👋 Привет, {user.first_name}!\n\nТы успешно записался на курс Python. Жди дальнейших инструкций!"
            )
            return

    # ЛОГИКА ОБЫЧНОЙ РЕФЕРАЛЬНОЙ СИСТЕМЫ
    if payload and not payload.startswith("course_"):
        referrer = User.objects.filter(referral_code=payload).first()
        if referrer and referrer.telegram_id != user.telegram_id and user.referred_by is None:
            user.referred_by = referrer.telegram_id
            user.save()
            referrer.referrals_count += 1
            referrer.save()
            try:
                bot.send_message(
                    referrer.telegram_id, 
                    f"🎉 По вашей ссылке пришёл новый пользователь!"
                )
            except Exception:
                pass

    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={user.referral_code}"
    
    text = (
        f"👋 Привет, <b>{user.first_name}</b>!\n\n"
        f"👥 Приглашено друзей: <b>{user.referrals_count}</b>\n\n"
        f"Твоя ссылка для друзей:\n<code>{ref_link}</code>"
    )
    bot.send_message(user.telegram_id, text, parse_mode="HTML")


@bot.message_handler(commands=["my_course"])
def cmd_my_course(message):
    user = get_or_create_user(message)
    if user.is_banned: return

    if not user.course_code:
        user.course_code = secrets.token_urlsafe(6)
        user.save()

    bot_username = bot.get_me().username
    course_link = f"https://t.me/{bot_username}?start=course_{user.course_code}"
    
    bot.send_message(
        message.chat.id, 
        f"🎓 <b>Твоя ссылка на курс Python:</b>\n\n<code>{course_link}</code>\n\n"
        f"Отправь её ученикам. Когда они нажмут Start, тебе придет уведомление!",
        parse_mode="HTML"
    )

# Блокировка забаненных
@bot.message_handler(func=lambda m: User.objects.filter(telegram_id=m.from_user.id, is_banned=True).exists(), content_types=["text"])
def block_banned(message):
    return
