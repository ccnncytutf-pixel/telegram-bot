import telebot

TOKEN = "ТВОЙ_НОВЫЙ_ТОКЕН"

bot = telebot.TeleBot(TOKEN)

msg_count = {}
relations = {}
marriages = {}

warns = {}
muted = set()
banned = set()


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
        f"👤 Ты: {name}\n"
        f"🔹 @{username}\n"
        f"💬 Сообщений: {msg_count.get(uid,0)}"
    )


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(
        message.chat.id,
        "📋 Команды:\n"
        "/start\n"
        "/help\n"
        "/стата\n"
        "/отношение @ник\n"
        "/брак @ник\n"
        "/варн\n"
        "/мут\n"
        "/размут\n"
        "/бан\n"
        "/разбан\n"
        "/clean\n"
        "кто я"
    )


@bot.message_handler(commands=["стата"])
def stats(message):
    bot.send_message(
        message.chat.id,
        f"📊 Всего сообщений: {msg_count.get(message.from_user.id,0)}"
    )


@bot.message_handler(commands=["варн"])
def warn(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return

    user = message.reply_to_message.from_user
    warns[user.id] = warns.get(user.id, 0) + 1

    try:
        if warns[user.id] >= 3:
            bot.restrict_chat_member(
                message.chat.id,
                user.id,
                can_send_messages=False
            )
            bot.reply_to(message, f"🔇 {user.first_name} получил 3 варна и автоматически замучен.")
        else:
            bot.reply_to(message, f"⚠️ Варн {warns[user.id]}/3")
    except:
        bot.reply_to(message, "❌ Нет прав.")
        @bot.message_handler(commands=["мут"])
def mute(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return

    user = message.reply_to_message.from_user

    try:
        bot.restrict_chat_member(
            message.chat.id,
            user.id,
            can_send_messages=False
        )
        bot.reply_to(message, f"🔇 {user.first_name} замучен.")
    except:
        bot.reply_to(message, "❌ Нет прав на мут.")


@bot.message_handler(commands=["размут"])
def unmute(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return

    user = message.reply_to_message.from_user

    try:
        bot.restrict_chat_member(
            message.chat.id,
            user.id,
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
        bot.reply_to(message, f"🔊 {user.first_name} размучен.")
    except:
        bot.reply_to(message, "❌ Нет прав.")


@bot.message_handler(commands=["бан"])
def ban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return

    user = message.reply_to_message.from_user

    try:
        bot.ban_chat_member(message.chat.id, user.id)
        bot.reply_to(message, f"⛔ {user.first_name} забанен.")
    except:
        bot.reply_to(message, "❌ Нет прав на бан.")


@bot.message_handler(commands=["разбан"])
def unban(message):
    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответь на сообщение.")
        return

    user = message.reply_to_message.from_user

    try:
        bot.unban_chat_member(message.chat.id, user.id)
        bot.reply_to(message, f"✅ {user.first_name} разбанен.")
    except:
        bot.reply_to(message, "❌ Не удалось разбанить.")
@bot.message_handler(commands=["брак"])
def marry(message):
    p = message.text.split(maxsplit=1)

    if len(p) < 2:
        bot.reply_to(message, "Напиши: /брак @ник")
        return

    target = p[1]
    marriages[message.from_user.first_name] = target

    bot.reply_to(
        message,
        f"💍 {message.from_user.first_name} заключил брак с {target}"
    )


@bot.message_handler(commands=["отношение"])
def relation(message):
    p = message.text.split(maxsplit=1)

    if len(p) < 2:
        bot.reply_to(message, "Напиши: /отношение @ник")
        return

    target = p[1]

    bot.reply_to(
        message,
        f"💞 Отношение к {target}: {relations.get(target,'нет')}"
    )


@bot.message_handler(commands=["clean"])
def clean(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "🧹 Чистка выполнена!")
    except:
        bot.reply_to(message, "❌ Нет прав на удаление")
        @bot.message_handler(func=lambda m: True)
def actions(message):

    if not message.text:
        return

    msg_count[message.from_user.id] = msg_count.get(message.from_user.id, 0) + 1

    text = message.text.lower()
    name = message.from_user.first_name

    actions = {
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

    for a, r in actions.items():
        if text.startswith(a):

            p = message.text.split(maxsplit=1)
            target = p[1] if len(p) > 1 else "кого-то"

            if a == "люблю":
                relations[target] = "❤️ любовь"

            if a == "дружу":
                relations[target] = "🤝 дружба"

            bot.reply_to(
                message,
                r.format(name=name, target=target)
            )
            return


bot.infinity_polling()
