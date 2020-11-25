import telebot

bot = telebot.TeleBot("1483156702:AAFnhYrJ3sYTsxh-6_bePLOvGYv-AjNwQ0o", parse_mode=None)

from pyowm.owm import OWM
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('0c1014b0f372cfaaf2906ca7e72c5b87', config_dict)
reg = owm.city_id_registry()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, где хочешь узнать погоду?')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'кирюша' or message.text.lower() == "сашуля" or message.text.lower() == "александр":
        bot.send_message(message.chat.id, 'прелесть =)')
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        place = message.text.lower()
        mgr = owm.weather_manager()
        try:
            observation = mgr.weather_at_place(place)
            weather = observation.weather
            temp_dict_celsius = weather.temperature('celsius')
            # Температура
            bot.send_message(message.chat.id, "Средняя тепература: " + str(round(temp_dict_celsius['temp'], 1)))
            bot.send_message(message.chat.id, "Ощущается как " + str(round(temp_dict_celsius['feels_like'], 1)))
            # Обзорная инфомация
            current_weather = weather.detailed_status
            bot.send_message(message.chat.id, "На улице " + current_weather)
            # Ветер
            wind_dict_in_meters_per_sec = observation.weather.wind()
            bot.send_message(message.chat.id, "Скорость ветра: " + str(wind_dict_in_meters_per_sec['speed']) + " м/с")
        except NotFoundError:
            bot.send_message(message.chat.id, "Такого города нет в базе данных!")

bot.polling()
