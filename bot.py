import COVID19Py
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

covid19 = COVID19Py.COVID19()

#start

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Италия')
btn2 = types.KeyboardButton('Украина')
btn3 = types.KeyboardButton('Россия')
btn4 = types.KeyboardButton('США')
btn5 = types.KeyboardButton('Во всём мире')
markup.add(btn1, btn2, btn3, btn4, btn5)

@bot.message_handler(commands=['start'])
def start(message):

	description = 'Привет, {0.first_name}!\nЯ бот сообщающий актуальную статистику о короновирусе\n \nНажми на интересующую тебя страну, или же ты можешь узнать о ситуации во всем мире\n \nЯ могу сообщить информацию о таких странах как:\n\n<b>Россия, США, Италия, Бразилия, Испания, Франция, Великобритания, Украина, Германия, Турция, Индия</b> \n \n Напиши название страны или нажми на кнопки \n (Названия стран писать с большой буквы)'
	bot.send_message(message.chat.id, description.format(message.from_user, bot.get_me), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def info(message):

	info = ''

	if message.text == 'США':
		location = covid19.getLocationByCountryCode("US")
	elif message.text == 'Россия':
		location = covid19.getLocationByCountryCode("RU")
	elif message.text == 'Италия':
		location = covid19.getLocationByCountryCode("IT")
	elif message.text == 'Бразилия':
		location = covid19.getLocationByCountryCode("BR")
	elif message.text == 'Испания':
		location = covid19.getLocationByCountryCode("ES")
	elif message.text == 'Франция':
		location = covid19.getLocationByCountryCode("FR")
	elif message.text == 'Великобритания':
		location = covid19.getLocationByCountryCode("GB")
	elif message.text == 'Германия':
		location = covid19.getLocationByCountryCode("DE")
	elif message.text == 'Индия':
		location = covid19.getLocationByCountryCode("IN")
	elif message.text == 'Украина':
		location = covid19.getLocationByCountryCode("UA")
			
	else:
		location = covid19.getLatest()
		info = f"<b>Актуальная статистика по всему миру:</b>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

	if info == "":
		date = location[0]['last_updated'].split("T")
		time = date[1].split(".")
		info = f"<b>Актуальная статистика:</b>\n<b>" \
			   f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
			   f"{location[0]['latest']['deaths']:,}"

	bot.send_message(message.chat.id, info, parse_mode='html')

bot.polling()