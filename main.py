from email import message_from_string

import flask
import telebot
from pyexpat.errors import messages
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import Flask, request, jsonify
import threading
import re
import hashlib


telegram_API = '8444261511:AAGPMcQKIhJS5vixoDnOQnkaFGierK4gLRk'
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

data = {}

def menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎮 Перейти в мини-игры')
    markup.row('📞 Поддержка')
    return markup


#=== Получение данных от пользователя ===
@bot.message_handler(func=lambda m: m.text == '🎮 Перейти в мини-игры')
def get_user_info(message):

    userTelegramid = message.chat.id
    userLogo = bot.get_user_profile_photos(userTelegramid)
    usernameTelegram = message.from_user.username

    if userLogo.total_count > 0:
        file_id = userLogo.photos[0][-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)
    else:
        downloaded = None

    data['username'] = usernameTelegram
    data['telegram_id'] = userTelegramid
    data['logo'] = downloaded

    open_miniapp(message)

# === Открытие mini app ===
def open_miniapp(message):
    url = ''

    # создаём inline кнопку с mini app
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(url=url)
    button = InlineKeyboardButton('🎮 Играть', web_app=web_app)
    markup.add(button)

    bot.send_message(message.chat.id, 'Нажми, чтобы открыть mini app:', reply_markup=markup)




#=== ПОДДЕРЖКА ===
@bot.message_handler(func=lambda m: m.text == '📞 Поддержка')
def support(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Написать в тех. поддержку')
    markup.row('Назад')
    bot.send_message(message.chat.id, 'Выбери один из пунктов снизу 👇', reply_markup=markup)


#=== ПИСЬМО В ТЕХ, ПОДДЕРЖКУ ===

@bot.message_handler(func=lambda m: m.text == 'Написать в тех. поддержку')
def create_message(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Опишите вашу проблему', reply_markup=markup)
    bot.register_next_step_handler(message, send_message)

def send_message(message):
    userMessage = message.text
    user_info = f"📩 Сообщение от @{message.from_user.username or 'Без ника'} (ID: {message.chat.id}):\n\n{message.text}"
    bot.send_message(ADMIN_ID, user_info)
    bot.send_message(message.chat.id, '✅ Сообщение отправлено. Ожидайте ответа.')




@bot.message_handler(func=lambda m: m.text == 'Назад')
def back(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, 'Выбери, с чего начнём 👇',reply_markup=menu_markup())


# === API ЭНДПОИНТЫ ===
app = flask.Flask(__name__)

@app.route('/users', methods=['GET'])



bot.polling(non_stop=True)
