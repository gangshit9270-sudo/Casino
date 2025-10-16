from email import message_from_string

import telebot
from pyexpat.errors import messages
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
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
def menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎮 Перейти в мини-игры')
    markup.row('📞 Поддержка')
    return markup




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
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_all_users():
    db = sqlite3.connect('usersDB.db')
    cursor = db.cursor()
    cursor.execute('SELECT telegram_id, player_id, username FROM users')
    users = cursor.fetchall()
    db.close()
    return jsonify([
        {'telegram_id': row[0], 'player_id': row[1], 'username': row[2]} for row in users
    ])

@app.route('/user/<int:telegram_id>', methods=['GET'])
def get_user(telegram_id):
    db = sqlite3.connect('usersDB.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchone()
    db.close()
    if row:
        return jsonify({
            'id': row[0],
            'telegram_id': row[1],
            'player_id': row[2],
            'username': row[3],
            'password': row[4],
            'pin': row[5]
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    db = sqlite3.connect('usersDB.db')
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO users (telegram_id, player_id, username, password, pin)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['telegram_id'],
        data['player_id'],
        data['username'],
        data['password'],
        data['pin']
    ))
    db.commit()
    db.close()
    return jsonify({'message': 'User created successfully'}), 201

# === ЗАПУСК БОТА И СЕРВЕРА ===
def start_flask():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=start_flask).start()


bot.polling(non_stop=True)
