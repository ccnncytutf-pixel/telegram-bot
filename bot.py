import telebot

TOKEN = "8641592656:AAFfE4luC7BEdIBZvopcyaWscaZ33wamxTg"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я запущен 🤖")

@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.chat.id, "Ты написал: " + message.text)

bot.infinity_polling()
