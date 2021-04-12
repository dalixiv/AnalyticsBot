import requests
import telebot
from telebot import types

import json  # импортим для парсинга сайта

from app.utils import serialize_ex, get_exchange
from app.config import ctx
from app.db import User, add_user, create_tables

bot = telebot.TeleBot(ctx.tg_bot_token)  # АПИ бота, для его подключения


@bot.message_handler(commands=["start"])  # команда старт
def start_command(message):
    if message.text == "/start":
        bot.send_message(
            message.chat.id,
            "Greetings! I can show you exchange rates.\n"
            + "To get the exchange rates press /exchange.\n"
            + "To get Current price and EnterpriseVAluetype type /ticker\n."
            + "To get help press /help.",
        )


@bot.message_handler(commands=["reg"])  # команда реги
def start(message):
    if message.text == "/reg":
        bot.send_message(message.from_user.id, "What is your name?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Type /reg")


@bot.message_handler(commands=["exchange"])  # команда показывает курс
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("USD", callback_data="get-USD"))
    keyboard.row(
        telebot.types.InlineKeyboardButton("EUR", callback_data="get-EUR"),
        telebot.types.InlineKeyboardButton("RUB", callback_data="get-RUR"),
    )

    bot.send_message(
        message.chat.id, "Click on the currency of choice:", reply_markup=keyboard
    )


@bot.message_handler(commands=["ticker"])  # команда показывает акции
def start(message):
    if message.text == "/ticker":
        keyboard = types.InlineKeyboardMarkup()
        key_Information = types.InlineKeyboardButton(text="Information", callback_data="Information_ticker")
        keyboard.add(key_Information)
        key_News = types.InlineKeyboardButton(text="News", callback_data="News_ticker")
        keyboard.add(key_News)
        bot.send_message(message.from_user.id, text="What whould u like to see", reply_markup=keyboard)
        bot.register_next_step_handler(message, getinfo)
    else:
        bot.send_message(message.from_user.id, "Type /ticker")


@bot.message_handler(commands=["help"])  # команда help
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "Message the developer", url="telegram.me/ivanovskayaaaaa"
        )
    )
    bot.send_message(
        message.chat.id,
        "1) To receive a list of available currencies press /exchange.\n"
        + "1.1) Click on the currency you are interested in.\n"
        + "1.2) You will receive a message containing information regarding the source and the target currencies, "
        + "buying rates and selling rates.\n"
        + "2) The bot supports inline. Type @AnalitDBot in any chat and the first letters of a currency.\n"
        + "3) To register in the bot type /reg.\n"
        + "4)To get Current price and EnterpriseVAluetype type /ticker",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)  # распределение кнопок
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)
    elif query.data == "Information_ticker":
        bot.send_message(query.message.chat.id, "send a ticker plz")

    else:
        if query.data == "yes":
            bot.send_message(query.message.chat.id, "That's great, to continue type /help")
        elif query.data == "no":
            bot.send_message(query.message.chat.id, "Ok,one more time! What is your name?")
            bot.register_next_step_handler(query.message, get_name)


@bot.message_handler(content_types=["text"])  # распознавание текста
def get_text_messages(message):
    if message.text == "Hi":
        bot.send_message(message.from_user.id, "Hi, you can type /reg to register")
    else:
        bot.send_message(message.from_user.id, "I can't understand you. Type /help.")


def get_name(message):  # получаем имя
    name = message.text
    bot.send_message(message.from_user.id, "What is your surname?")
    bot.register_next_step_handler(message, get_surname, name=name)


def get_surname(message, name: str = None):  # получаем фамилию
    surname = message.text
    bot.send_message(message.from_user.id, "How old are you?")
    bot.register_next_step_handler(message, get_age, name=name, surname=surname)


def get_age(message, name: str = None, surname: str = None):  # получаем возраст
    age = message.text
    if age.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text="Yes!", callback_data="yes")
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text="No", callback_data="no")
        keyboard.add(key_no)
        question = (
                "You are " + str(age) + " years, your name is " + name + " " + surname + "?"
        )
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        add_user(User(name=name, surname=surname, age=int(age)))
    else:
        bot.send_message(message.from_user.id, "Type with numbers, please")
        bot.register_next_step_handler(message, get_age)


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])


def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, "typing")
    ex = get_exchange(ex_code)
    bot.send_message(
        message.chat.id,
        serialize_ex(ex),
        reply_markup=get_update_keyboard(ex),
        parse_mode="HTML",
    )


def getinfo(ticker):  # получаем инфу по акциям
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
    querystring = {"symbol": ticker.text, "region": "US"}
    headers = {
        'x-rapidapi-key': "7d2a5f774amshbee3475d315e704p1bd9e6jsnc7de2c4c43d6",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    qwe = json.loads(response.text)
    bot.send_message(ticker.from_user.id,
                     f" {ticker.text}\nCurrent price - {qwe['financialData']['currentPrice']['raw']}\nEnterpriseVAlue - {qwe['defaultKeyStatistics']['enterpriseValue']['raw']}")


def get_update_keyboard(ex):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            "",
            callback_data=json.dumps(
                {"t": "u", "e": {"b": ex["buy"], "s": ex["sale"], "c": ex["ccy"]}}
            ).replace(" ", ""),
        ),
        telebot.types.InlineKeyboardButton("", switch_inline_query=ex["ccy"]),
    )
    return keyboard


def main():

    create_tables()
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
