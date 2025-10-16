import os
from dotenv import load_dotenv
import telebot
from telebot import types
from utils import load_prompt

# --- Загрузка токена из .env ---
dotenv_path = '.env'
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f".env файл не найден по пути {dotenv_path}")

load_dotenv(dotenv_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден! Проверьте файл .env")

bot = telebot.TeleBot(TOKEN)

# --- /start command handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text="Support", callback_data="support"),
        types.InlineKeyboardButton(text="Sales", callback_data="sales")
    )

    welcome_text = load_prompt("welcome")  # загружаем текст из resources/welcome.txt

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=keyboard
    )

# --- Callback query handler ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "support":
        support_text = load_prompt("support")
        bot.send_message(call.message.chat.id, support_text)
    elif call.data == "sales":
        sales_text = load_prompt("sales")
        bot.send_message(call.message.chat.id, sales_text)

# --- Запуск бота ---
if __name__ == "__main__":
    print("Pond Mobile bot is running...")
    bot.polling(none_stop=True, interval=0, timeout=20)
