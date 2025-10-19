import telebot
from AI_support.ai_support import ai_answer_support
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import re

BOT_API = '8370783217:AAG6iWembVf_FqHGikW_L3xwlnTvOwXX-KI'
SUPPORT_ID = 1180361085

ai_answer = True
active_chats = {}

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

@bot.message_handler(commands=['close'])
def close_dialog(message):
    if message.chat.id != SUPPORT_ID:
        bot.send_message(message.chat.id, "⛔ Команда доступна только администратору.")
        return

    # Попробуем извлечь ID из текста команды
    match = re.search(r"/close\s+(\d+)", message.text)
    if not match:
        bot.send_message(SUPPORT_ID, "⚠️ Используй команду так:\n/close <user_id>")
        return

    user_id = int(match.group(1))
    global ai_answer
    ai_answer = True
    if user_id in active_chats:
        del active_chats[user_id]
        bot.send_message(user_id, "✅ Ваш диалог с поддержкой завершён. Если понадобится помощь — просто напишите снова!")
        bot.send_message(SUPPORT_ID, f"🔒 Диалог с пользователем {user_id} закрыт.")

    else:
        bot.send_message(SUPPORT_ID, "⚠️ Диалог с этим пользователем уже закрыт или не найден.")

@bot.message_handler(commands=['list'])
def list_active_chats(message):
    if message.chat.id != SUPPORT_ID:
        bot.send_message(message.chat.id, "⛔ Команда доступна только администратору.")
        return

    if not active_chats:
        bot.send_message(SUPPORT_ID, "📭 Активных диалогов нет.")
        return

    chat_list = "\n".join(
        [f"👤 @{username} — ID: {user_id}" for user_id, username in active_chats.items()]
    )
    bot.send_message(SUPPORT_ID, f"📋 Активные диалоги:\n\n{chat_list}\n\nЧтобы закрыть диалог, напиши: /close <user_id>")





@bot.message_handler(commands=['admin'])
def connect_with_admin(message):
    global ai_answer
    ai_answer = False
    bot.send_message(message.chat.id, 'Оставьте ваше сообщение — скоро с вами свяжутся 👨‍💻')
    bot.register_next_step_handler(message, send_message_to_admin)

def send_message_to_admin(message):
    user_id = message.chat.id
    username = message.from_user.username or "Без никнейма"
    active_chats[user_id] = username

    caption = f"💬 Сообщение от @{username} (ID: {user_id}):"

    if message.text:
        bot.send_message(SUPPORT_ID, f"{caption}\n\n{message.text}")
    elif message.photo:
        bot.send_photo(SUPPORT_ID, message.photo[-1].file_id, caption=caption)
    elif message.video:
        bot.send_video(SUPPORT_ID, message.video.file_id, caption=caption)
    elif message.document:
        bot.send_document(SUPPORT_ID, message.document.file_id, caption=caption)
    elif message.voice:
        bot.send_voice(SUPPORT_ID, message.voice.file_id, caption=caption)
    else:
        bot.send_message(SUPPORT_ID, f"{caption}\n\n(Неизвестный тип сообщения)")

    bot.send_message(user_id, "✅ Ваше сообщение отправлено в поддержку. Ожидайте ответа!")



@bot.message_handler(func=lambda m: m.chat.id == SUPPORT_ID and m.reply_to_message)
def admin_reply(message):
    reply = message.reply_to_message

    # используем текст или подпись
    content = reply.text or reply.caption
    if not content:
        bot.send_message(SUPPORT_ID, "⚠️ Не удалось извлечь ID пользователя из сообщения.")
        return

    match = re.search(r"ID:\s*(\d+)", content)
    if not match:
        bot.send_message(SUPPORT_ID, "⚠️ Не удалось определить ID пользователя для ответа.")
        return

    user_id = int(match.group(1))

    # отправка ответа пользователю
    if message.text:
        bot.send_message(user_id, f"📩 Ответ поддержки:\n{message.text}")
    elif message.photo:
        bot.send_photo(user_id, message.photo[-1].file_id, caption="📩 Ответ поддержки:")
    elif message.video:
        bot.send_video(user_id, message.video.file_id, caption="📩 Ответ поддержки:")
    elif message.document:
        bot.send_document(user_id, message.document.file_id, caption="📩 Ответ поддержки:")
    elif message.voice:
        bot.send_voice(user_id, message.voice.file_id, caption="📩 Голосовое сообщение от поддержки:")
    else:
        bot.send_message(user_id, "⚠️ Поддержка отправила неизвестный тип сообщения.")

    bot.send_message(SUPPORT_ID, "✅ Ответ отправлен пользователю.")





@bot.message_handler(func=lambda m: m.chat.id != SUPPORT_ID)
def user_message(message):
    user_id = message.chat.id
    username = message.from_user.username or "Без никнейма"

    # Если диалог активен — пересылаем админу
    if user_id in active_chats:
        caption = f"💬 Сообщение от @{username} (ID: {user_id}):"
        if message.text:
            bot.send_message(SUPPORT_ID, f"{caption}\n\n{message.text}")
        elif message.photo:
            bot.send_photo(SUPPORT_ID, message.photo[-1].file_id, caption=caption)
        elif message.video:
            bot.send_video(SUPPORT_ID, message.video.file_id, caption=caption)
        elif message.document:
            bot.send_document(SUPPORT_ID, message.document.file_id, caption=caption)
        elif message.voice:
            bot.send_voice(SUPPORT_ID, message.voice.file_id, caption=caption)
        else:
            bot.send_message(SUPPORT_ID, f"{caption}\n\n(Неизвестный тип сообщения)")
        bot.send_message(user_id, "✅ Ваше сообщение отправлено в поддержку. Ожидайте ответа!")
        return  # Важно: прерываем обработку, чтобы ИИ не срабатывал

    # Если диалога нет — используем ИИ
    prompt = message.text
    ai_response_data = ai_answer_support(prompt)

    if "choices" in ai_response_data:
        answer = ai_response_data["choices"][0]["message"]["content"]
    elif "output" in ai_response_data:
        answer = ai_response_data["output"][0]["content"][0]["text"]
    else:
        answer = "Извини, я не смог получить ответ от AI. Попробуй ещё раз."

    bot.send_message(user_id, answer)







bot.polling(non_stop=True)

