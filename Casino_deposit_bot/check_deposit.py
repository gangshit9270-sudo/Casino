from flask import Flask, request, jsonify
import json
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

NOWPAYMENT_API = os.getenv('NOWPAYMENT_API')
NOWPAYMENT_URL = os.getenv('NOWPAYMENT_URL')
NGROK_SELF_URL = os.getenv('NGROK_SELF_URL')
NGROK_SERVER_URL = os.getenv('NGROK_SERVER_URL')
SERVER_SECRET = os.getenv('SERVER_SECRET')


@app.route('/api/payment/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    header_secret_api = request.headers.get('auth-token')

    if header_secret_api != SERVER_SECRET:
        print("[DEBUG] Ошибка авторизации: неверный токен")
        return jsonify({"status": "error", "message": "unauthorized"}), 401


    if not data:
        print("[DEBUG] Пустой или некорректный JSON")

        return jsonify({"status": "error", "message": "invalid json"}), 400

    print("[DEBUG] Webhook получен:", data)
    print("[DEBUG] Authorization:", header_secret_api)


    payment_system = 'usdt'
    currency = data.get("currency", "Не указано").lower()
    amount = data.get("amount", "Не указано")
    txn_type = data.get("type", "Не указано")

    if payment_system == "usdt":
        payment_system = "usdttrc20"

    # Формируем payload для NowPayments
    payload = {
        'price_amount': amount,
        'price_currency': currency,
        'pay_currency': payment_system,
        "ipn_callback_url": NGROK_SELF_URL,
    }
    headers = {
        'x-api-key': NOWPAYMENT_API,
        'Content-Type': 'application/json',

    }

    try:
        response = requests.post(NOWPAYMENT_URL, data=json.dumps(payload), headers=headers)
        result = response.json()
        # кошелек берется только из ответа NowPayments
        print(result)
    except Exception as e:
        print("[DEBUG] Ошибка при запросе к NowPayments:", e)
        return jsonify({"status": "error", "message": str(e)}), 500



    print("[DEBUG] Ответ NowPayments:")

    requests.post(
        NGROK_SERVER_URL,
        json=result,
        headers={
            "Content-Type": "application/json"
        }
    )

    return jsonify(result), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
