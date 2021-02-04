import telebot
from telebot import types

bot = telebot.TeleBot("1567492258:AAHSB2NW60E_eOReP47OytVrQW1EHItBvQc")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Cool : )")
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Sad(")

name = ""
surname = ""
age = 0

@bot.message_handler(commands=["reg"])
def start(message):
    if message.text == "/reg":
        bot.send_message(message.from_user.id, "What is your name?")
        bot.register_next_step_handler(
            message, get_name
        )
    else:
        bot.send_message(message.from_user.id, "Type /reg")


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "What is your surname?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "How old are you?")
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Type with numbers, please")
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Yes!", callback_data="yes")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="No", callback_data="no")
    keyboard.add(key_no)
    question = "You are " + str(age) + " years, your name is " + name + " " + surname + "?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == "Hi":
        bot.send_message(message.from_user.id, "Hi, you can type /reg to register")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Type /reg to register")
    else:
        bot.send_message(message.from_user.id, "I can't understand you. Type /help.")

bot.polling(none_stop=True, interval=0)
