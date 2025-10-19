import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


BOT_API = '8278586337:AAFfz3FILNW_4U33XPiCA0-T4coK59KkGIY'
EXCHANGE_ID = ''



bot = telebot.TeleBot(BOT_API)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Отправьте запрос')


@bot.message_handler(func=lambda m: True)
def get_request(message):
    deposit_request = message.text

    request_To_Exchange = f'''
    PAY (status)
    CURRENCY (currency)
    AMOUNT (amount)
    WALLET (hash)
    '''


    bot.send_message(EXCHANGE_ID, request_To_Exchange)


bot.polling(non_stop=True)

