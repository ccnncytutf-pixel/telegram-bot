import telebot
import os

TOKEN = "8641592656:AAECORq1Rf4r1PqNA25EO-OvcL7G2hEZTuM"  # Лучше вынести в переменные окружения
bot = telebot.TeleBot(TOKEN)

# Хранилища данных
msg_count = {}
relations = {}
marriages = {}
warns = {}
muted = set()
banned = set()

# Вспомогательная функция – проверка прав администратора
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "✅ Я работаю 🤖")

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "кто я")
def who(message):
    uid = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username or "нет"
    bot.reply_to(
        message,
        f"👤 Ты: {name}\n🔹 @{username}\n💬 Сообщений: {msg_count.get(uid, 0)}"
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📋 Команды:\n"
        "/start\n/help\n/стата\n/отношение @ник\n/брак @ник\n"
        "/варн (ответ на сообщение)\n/мут (ответ)\n/размут (ответ)\n"
        "/бан (ответ)\n/разбан (ответ)\n/clean\n"
        "кто я\n\n"
        "Действия: погладить, обнять, поцеловать, укусить, ударить, "
        "вебать, пнуть, дать печеньку, подарить, дать пять, похвалить, "
        "люблю, дружу (с @ник)"
    )

@bot.message_handler(commands=["стата"])
def stats(message):
    bot.send_message(
        message.chat.id,
        f"📊 Всего сообщений: {msg_count.get(message.from_user.id, 0)}"
    )

# ---- Модерация ----
@bot.message_handler(commands=["варн"])
def warn(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ У вас нет прав на выдачу варнов.")
        return

    user = message.reply_to_message.from_user
    warns[user.id] = warns.get(user.id, 0) + 1
    try:
        if warns[user.id] >= 3:
            bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=False)
            muted.add(user.id)
            bot.reply_to(message, f"🔇 {user.first_name} получил 3 варна и автоматически замучен.")
        else:
            bot.reply_to(message, f"⚠️ Варн {warns[user.id]}/3")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=["мут"])
def mute(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Нет прав на мут.")
        return

    user = message.reply_to_message.from_user
    try:
        bot.restrict_chat_member(message.chat.id, user.id, can_send_messages=False)
        muted.add(user.id)
        bot.reply_to(message, f"🔇 {user.first_name} замучен.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=["размут"])
def unmute(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Нет прав на размут.")
        return

    user = message.reply_to_message.from_user
    try:
        bot.restrict_chat_member(
            message.chat.id, user.id,
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        muted.discard(user.id)
        bot.reply_to(message, f"🔊 {user.first_name} размучен.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=["бан"])
def ban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Нет прав на бан.")
        return

    user = message.reply_to_message.from_user
    try:
        bot.ban_chat_member(message.chat.id, user.id)
        banned.add(user.id)
        bot.reply_to(message, f"⛔ {user.first_name} забанен.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=["разбан"])
def unban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Нет прав на разбан.")
        return

    user = message.reply_to_message.from_user
    try:
        bot.unban_chat_member(message.chat.id, user.id)
        banned.discard(user.id)
        bot.reply_to(message, f"✅ {user.first_name} разбанен.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# ---- Игровые / социальные команды ----
@bot.message_handler(commands=["брак"])
def marry(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Напиши: /брак @ник")
        return
    target = parts[1]
    marriages[message.from_user.id] = target  # ключ – ID, а не имя
    bot.reply_to(
        message,
        f"💍 {message.from_user.first_name} заключил брак с {target}"
    )

@bot.message_handler(commands=["отношение"])
def relation(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Напиши: /отношение @ник")
        return
    target = parts[1]
    bot.reply_to(
        message,
        f"💞 Отношение к {target}: {relations.get(target, 'нет')}"
    )

@bot.message_handler(commands=["clean"])
def clean(message):
    # Для удаления сообщения бота нужны права администратора
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "❌ Нет прав на удаление.")
        return
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "🧹 Чистка выполнена!")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# ---- Обработчик текстовых действий (погладить, обнять и т.д.) ----
@bot.message_handler(func=lambda m: True)
def actions(message):
    if not message.text:
        return

    # Считаем сообщения
    msg_count[message.from_user.id] = msg_count.get(message.from_user.id, 0) + 1

    text = message.text.lower()
    name = message.from_user.first_name

    actions_dict = {
        "погладить": "💕 {name} погладил {target}",
        "обнять": "🤗 {name} обнял {target}",
        "поцеловать": "😘 {name} поцеловал {target}",
        "укусить": "🦷 {name} укусил {target}",
        "ударить": "👊 {name} ударил {target}",
        "вебать": "🖕 {name} вебал {target}",
        "пнуть": "🦶 {name} пнул {target}",
        "дать печеньку": "🍪 {name} дал печеньку {target}",
        "подарить": "🎁 {name} подарил {target}",
        "дать пять": "✋ {name} дал пять {target}",
        "похвалить": "⭐ {name} похвалил {target}",
        "люблю": "❤️ {name} любит {target}",
        "дружу": "🤝 {name} дружит с {target}"
    }

    for action, template in actions_dict.items():
        if text.startswith(action):
            parts = message.text.split(maxsplit=1)
            if len(parts) < 2:
                target = "кого-то"
            else:
                target = parts[1]
                # Сохраняем отношение для /отношение
                if action == "люблю":
                    relations[target] = "❤️ любовь"
                elif action == "дружу":
                    relations[target] = "🤝 дружба"
            bot.reply_to(message, template.format(name=name, target=target))
            return

# Запуск бота
if __name__ == "__main__":
    bot.infinity_polling()
