import telebot

TOKEN = "8641592656:AAFfE4luC7BEdIBZvopcyaWscaZ33wamxTg"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я запущен 🤖")

@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.chat.id, "Ты написал: " + message.text)
@bot.message_handler(func=lambda message: message.text.lower() == "кто я")
def who_am_i(message):
    name = message.from_user.first_name
    username = message.from_user.username

    bot.send_message(
        message.chat.id,
        f"👤 Имя: {name}\n"
        f"🔹 Юзернейм: @{username if username else 'нет'}"
    )
bot.infinity_polling()
