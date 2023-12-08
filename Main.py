import telebot

from Extensions import *
from Config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def info_message(message: telebot.types.Message):
    if message.text == "/start":
        bot.send_message(message.chat.id, "Приветствую Вас!")
        Valutes.update_valutes()
        bot.reply_to(message, "Готов к работе")

    bot.send_message(message.chat.id, "Чтобы начать работу, используя кодировки, предоставьте следующую информацию:\n \
<Название конвертируемой валюты> <Валюту в которую переводим> <Значение для конвертируемой валюты> \n \
Например: RUB USD 1\n\n \
Доступные валюты можно узнать с помощью команды: /values")

@bot.message_handler(commands=["values"])
def value_message(message: telebot.types.Message):
    if len(Valutes.base_value_dict) < 1:
        Valutes.update_valutes()
    text = "Доступные валюты:\n"
    for key in Valutes.base_value_dict.keys():
        text = "\n".join( (text, f"{key} - {Valutes.base_value_dict[key]['Name']}") )
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert_user_value(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            bot.reply_to(message, "Invalid parametrs")
            raise ConvertionExeptions("Invalid parameters")
        if len(Valutes.base_value_dict) < 1:
            Valutes.update_valutes()
        quote, base, amount = values
        total_amount = ValuteConverter.convert(quote, base, amount)
    except ConvertionExeptions as e:
        bot.reply_to(message, f'Ошибка пользователя!\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не могу обработать команду!\n {e}')
    else:
        text = (f"Стоимость {amount} {quote} эквивалентно {total_amount} {base}. \n\
информация обновлена от: {Valutes.update_time}")
        bot.reply_to(message, f"Информация с сайта cbr.ru:\n{text}")

bot.polling()
