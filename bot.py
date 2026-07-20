import telebot

TOKEN = "8641592656:AAGMLhGeggs05mCwFFXAZnh3vUyNOIr0pFg"

bot = telebot.TeleBot(TOKEN)

msg_count = {}
relations = {}
marriages = {}


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
        "/start\n/help\n"
        "кто я\n"
        "/стата\n"
        "/отношение @ник\n"
        "/брак @ник\n"
        "/clean\n\n"
        "💕 Действия:\n"
        "погладить\nобнять\nпоцеловать\n"
        "укусить\nударить\nвебать\n"
        "подарить\nдать печеньку"
    )


@bot.message_handler(commands=["стата"])
def stats(message):
    bot.send_message(
        message.chat.id,
        f"📊 Всего твоих сообщений: {msg_count.get(message.from_user.id,0)}"
    )


@bot.message_handler(commands=["брак"])
def marry(message):
    p = message.text.split(maxsplit=1)

    if len(p) < 2:
        bot.reply_to(message,"Напиши: /брак @ник")
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
        bot.reply_to(message,"Напиши: /отношение @ник")
        return

    target = p[1]

    bot.reply_to(
        message,
        f"💞 Отношение к {target}: {relations.get(target,'нет')}"
    )


@bot.message_handler(commands=["clean"])
def clean(message):
    try:
        bot.delete_message(message.chat.id,message.message_id)
        bot.send_message(message.chat.id,"🧹 Чистка выполнена!")
    except:
        bot.reply_to(message,"❌ Нет прав на удаление")


@bot.message_handler(func=lambda m: True)
def actions(message):

    if not message.text:
        return

    msg_count[message.from_user.id] = msg_count.get(message.from_user.id,0)+1

    text = message.text.lower()
    name = message.from_user.first_name

    actions = {
        "погладить":"💕 {name} погладил {target}",
        "обнять":"🤗 {name} обнял {target}",
        "поцеловать":"😘 {name} поцеловал {target}",
        "укусить":"🦷 {name} укусил {target}",
        "ударить":"👊 {name} ударил {target}",
        "вебать":"🖕 {name} вебал {target}",
        "пнуть":"🦶 {name} пнул {target}",
        "дать печеньку":"🍪 {name} дал печеньку {target}",
        "подарить":"🎁 {name} подарил {target}",
        "дать пять":"✋ {name} дал пять {target}",
        "похвалить":"⭐ {name} похвалил {target}",
        "люблю":"❤️ {name} любит {target}",
        "дружу":"🤝 {name} дружит с {target}"
    }

    for a,r in actions.items():
        if text.startswith(a):

            p = message.text.split(maxsplit=1)
            target = p[1] if len(p)>1 else "кого-то"

            if a=="люблю":
                relations[target]="❤️ любовь"

            if a=="дружу":
                relations[target]="🤝 дружба"

            bot.reply_to(
                message,
                r.format(name=name,target=target)
            )
            return


bot.infinity_polling()import telebot
