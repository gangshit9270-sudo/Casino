import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


telegram_API = '8311865673:AAFMPF8vWbfewiCoe78SFRFbvCE1LPfHax4'
ADMIN_ID = 1180361085

bot = telebot.TeleBot(telegram_API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''👋 Привет! Добро пожаловать в GameZone — место, где классика встречается с азартом 🎲  

Здесь ты можешь играть онлайн в:
♠️ Покер  
🎴 Белот  
🎯 Нарды  

💰 Управляй балансом, участвуй в турнирах и выигрывай реальные призы!

Выбери, с чего начнём 👇''', reply_markup=menu_markup())


# === MARKUPS ==
def menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎮 Перейти в мини-игры')
    markup.row('📞 Поддержка')
    return markup


# === Открытие mini app ===
@bot.message_handler(func=lambda m: m.text == '🎮 Перейти в мини-игры')
def open_miniapp(message):
    url = 'https://minibotaurore.vercel.app/'
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(url=url)
    button = InlineKeyboardButton('🎮 Играть', web_app=web_app)
    markup.add(button)

    bot.send_message(message.chat.id, 'Нажми, чтобы открыть mini app:', reply_markup=markup)




#=== РЕФЕРАЛЬНЫЕ ПРОЦЕССЫ ===
# @bot.message_handler(func=lambda m: m.text == '🔗 Рефералы')
# def referal_link(message):
#     username_id = message.from_user.id
#     referalLink = f'https://t.me/casinoTestgbot?start=ref_{username_id}'
#     bot_message = f'''Хочешь получать бонусы за приглашение друзей?
# Поделись своей уникальной ссылкой, чтобы каждый новый друг приносил тебе награду! 💰
#
# 🔗 Твоя реферальная ссылка:
# {referalLink}
#
# Каждый, кто перейдет по ней и запустит бота, станет твоим рефералом, а тебе начислят бонус! 🎁
#
# Удачи и больших выигрышей в GameZone! 🎲'''
#
#     bot.send_message(message.chat.id, bot_message)




#=== ПОДДЕРЖКА ===
@bot.message_handler(func=lambda m: m.text == '📞 Поддержка')
def support(message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text='Написать в тех поддержку',
        url='https://t.me/luckyton77supportbot'
    )
    markup.add(button)
    bot.send_message(message.chat.id,'Нажмите чтобы перейти', reply_markup=markup)








bot.polling(non_stop=True)
