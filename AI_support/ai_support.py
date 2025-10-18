from http.client import responses
import requests
import json


AI_TOKEN = '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'

def ai_answer_support(prompt, message_file='C:/Users/Zephirus/OneDrive/Desktop/Casino-main/AI_support/ai_settings.json'):
    with open(message_file, 'r', encoding='utf-8') as f:
        ai_settings = json.load(f)

    messages = ai_settings.get('messages', [])
    messages.append({
        "role": "user",
        "content": prompt
    })

    headers = {'Authorization': f'Bearer {AI_TOKEN}',
               "Content-Type": "application/json"
               }

    response = requests.post(
        url='https://openrouter.ai/api/v1/chat/completions',
        headers=headers,
        data=json.dumps({
            'model': "openai/gpt-4o",
            'messages': messages
        })
    )


    data = response.json()
    return data





