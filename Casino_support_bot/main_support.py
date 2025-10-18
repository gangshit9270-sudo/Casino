import telebot
from AI_support.ai_support import ai_answer_support

BOT_API = '8370783217:AAG6iWembVf_FqHGikW_L3xwlnTvOwXX-KI'

bot = telebot.TeleBot(BOT_API)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Привет! 👋  

Я — твой виртуальный помощник.  
Я здесь, чтобы помочь тебе быстро и удобно разобраться с любыми вопросами.  

Просто напиши свой вопрос, и я дам подробный, понятный и дружелюбный ответ.  
Если что-то окажется сложным, я подскажу, как связаться с администратором.  

Давай сделаем твой опыт комфортным и приятным! 🙂
''')



@bot.message_handler(func=lambda m: True)
def support_message(message):
    prompt = message.text

    ai_response_data = ai_answer_support(prompt)

    # Безопасное извлечение текста из ответа
    if "choices" in ai_response_data:
        answer = ai_response_data["choices"][0]["message"]["content"]
    elif "output" in ai_response_data:
        answer = ai_response_data["output"][0]["content"][0]["text"]
    else:
        answer = "Извини, я не смог получить ответ от AI. Попробуй ещё раз."

    bot.send_message(message.chat.id, answer)







bot.polling(non_stop=True)

