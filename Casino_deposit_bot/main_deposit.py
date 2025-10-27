import telebot
from flask import Flask
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import json
import requests


BOT_API = '8278586337:AAFfz3FILNW_4U33XPiCA0-T4coK59KkGIY'
EXCHANGE_ID = '1180361085'
NOWPAYMENT_API  = 'T9P6GM2-94D4TRJ-H4K7NH3-JGH0EF5'
NOWPAYMENT_URL = 'https://api.nowpayments.io/v1/payment'
app = Flask(__name__)


payments_value = {}

bot = telebot.TeleBot(BOT_API)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Отправьте запрос')


@bot.message_handler(func=lambda m: True)
def get_request(message):
    try:
        data = json.loads(message.text)  # превращаем строку в словарь
    except json.JSONDecodeError:
        bot.send_message(message.chat.id, "❌ Ошибка! Отправьте корректный JSON.")
        return


    payments_value['payment_system'] = data.get("payment_system", "Не указано")
    payments_value['currency'] = data.get("currency", "Не указано")
    payments_value['amount'] = data.get("amount", "Не указано")
    payments_value['wallet'] = data.get("wallet", "Не указано")
    payments_value['type'] = data.get("type", "Не указано")

    if payments_value['currency'] == "USDT":
        payments_value['currency'] = "USDTTRC20"

    # Формируем сообщение
    formatted_request = f"""
💰 Тип транзакции: {payments_value['type']}
🧾 Платежная система: {payments_value['payment_system']}
💵 Валюта: {payments_value['currency']}
💰 Сумма: {payments_value['amount']}
👛 Кошелек: {payments_value['wallet']}
"""


    payload = json.dumps({
        'price_amount': payments_value['amount'],
        'price_currency': 'usd',
        'pay_currency': payments_value['currency'].lower(),
        "ipn_callback_url": "https://joleen-resalable-song.ngrok-free.dev/nowpayments/webhook",

    })
    headers = {
        'x-api-key': NOWPAYMENT_API,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", NOWPAYMENT_URL, data=payload, headers=headers)
    result = response.json()

    wallet_address = result.get('pay_address')

    if not wallet_address:
        bot.send_message(
            message.chat.id,
            f"❌ Ошибка при создании платежа:\n{result.get('message', 'Неизвестная ошибка.')}"
        )
        print("[DEBUG] Ответ NowPayments:", result)
        return

    bot.send_message(message.chat.id, wallet_address)

    # Отправляем другому пользователю
    bot.send_message(EXCHANGE_ID, formatted_request)
    bot.send_message(message.chat.id, "✅ Запрос успешно отправлен!")






