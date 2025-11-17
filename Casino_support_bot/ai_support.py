import os
import json
import requests

AI_TOKEN = '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'


def ai_answer_support(prompt, message_file=None):
    try:
        # Если файл не указан, используем путь относительно текущего скрипта
        if message_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            message_file = os.path.join(current_dir, 'ai_settings.json')

        # Проверяем существование файла и создаем его при необходимости
        if not os.path.exists(message_file):
            # Создаем базовый файл настроек
            default_settings = {
                "model": "openai/gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты — бот поддержки казино GameZone. Твоя задача — помогать игрокам быстро и дружелюбно. Отвечай подробно, пошагово и в вежливой форме. Объясняй, как использовать игры, управлять балансом, участвовать в турнирах, получать и активировать бонусы. Если игрок спрашивает о выводе или пополнении средств, объясняй только интерфейс и шаги в приложении, не давай финансовые или юридические советы. Если игрок задает вопрос вне функционала бота или сложный технический вопрос, предлагай связаться с администратором через команду /admin или через Telegram. Отвечай только на вопросы, связанные с казино GameZone. Не придумывай информацию о сторонних сервисах или играх. Всегда используй дружелюбный и понятный язык, избегай профессионального жаргона, чтобы любой игрок мог понять инструкции. Если вопрос многозначный, разбивай ответ на шаги с примерами, и при необходимости уточняй у пользователя детали, прежде чем давать окончательный ответ. Не отвечай на вопросы, связанные с безопасностью аккаунта, паролями или персональными данными; в таких случаях направляй игрока к официальной поддержке или администратору. Всегда помни, что твоя цель — помогать игрокам эффективно и безопасно, делая их опыт в казино GameZone приятным и понятным."
                    }
                ]
            }
            with open(message_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, ensure_ascii=False, indent=2)
            print(f"✅ Создан файл настроек: {message_file}")

        # Читаем настройки
        with open(message_file, 'r', encoding='utf-8') as f:
            ai_settings = json.load(f)

        messages = ai_settings.get('messages', [])
        messages.append({
            "role": "user",
            "content": prompt
        })

        headers = {
            'Authorization': f'Bearer {AI_TOKEN}',
            "Content-Type": "application/json"
        }

        response = requests.post(
            url='https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            data=json.dumps({
                'model': "openai/gpt-4o",
                'messages': messages
            }),
            timeout=30  # Добавляем таймаут
        )

        # Проверяем статус ответа
        if response.status_code != 200:
            return {"error": f"API error: {response.status_code}"}

        data = response.json()
        return data

    except FileNotFoundError as e:
        return {"error": f"File not found: {e}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}"}
    except requests.RequestException as e:
        return {"error": f"Request error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}