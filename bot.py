import telebot

TOKEN = "8641592656:AAH5ciifqbcuHjv7BcAAUFtJqcB8Ce0sDUE"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я запущен 🤖")


@bot.message_handler(func=lambda message: message.text.lower() == "кто я")
def who_am_i(message):
    name = message.from_user.first_name
    username = message.from_user.username

    bot.reply_to(
        message,
        f"👤 Ты: {name}\n"
        f"🔹 Юзернейм: @{username if username else 'нет'}"
    )


@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "📋 Команды:\n"
        "/start — запуск\n"
        "кто я — профиль\n"
        "/help — помощь\n"
        "погладить @ник\n"
        "обнять @ник\n"
        "ударить @ник"
    )


@bot.message_handler(func=lambda message: True)
def actions(message):
    text = message.text.lower()
    name = message.from_user.first_name

    actions = {
        "погладить": "💕 {name} погладил {target}",
        "обнять": "🤗 {name} обнял {target}",
        "поцеловать": "😘 {name} поцеловал {target}",
        "укусить": "🦷 {name} укусил {target}",
        "ударить": "👊 {name} ударил {target}",
        "дать печеньку": "🍪 {name} дал печеньку {target}",
        "пожать руку": "🤝 {name} пожал руку {target}",
        "пнуть": "🦶 {name} пнул {target}",
        "дать пять": "✋ {name} дал пять {target}",
        "похвалить": "⭐ {name} похвалил {target}",
        "потанцевать": "💃 {name} потанцевал с {target}",
        "испугать": "👻 {name} испугал {target}",
        "подарить": "🎁 {name} подарил подарок {target}",
        "поздравить": "🎉 {name} поздравил {target}"
    }

    for action, reply in actions.items():
        if text.startswith(action):
            parts = message.text.split(maxsplit=1)
            target = parts[1] if len(parts) > 1 else "кого-то"

            bot.reply_to(
                message,
                reply.format(name=name, target=target)
            )
            return


bot.infinity_polling()
