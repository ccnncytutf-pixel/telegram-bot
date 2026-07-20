import telebot

TOKEN = "8641592656:AAHirlMfRDTo3SCefY0lJKcoVmEHZj3ywiw"

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
        "кто я — мой профиль\n"
        "/help — помощь"
    )


@bot.message_handler(func=lambda message: message.text.lower().startswith("ударить"))
def hit(message):
    text = message.text.split()

    if len(text) > 1:
        target = " ".join(text[1:])
        bot.reply_to(message, f"👊 {message.from_user.first_name} ударил {target} 😄")
    else:
    bot.reply_to(message, "Кого ударить? Напиши: ударить @ник")


bot.infinity_polling()
