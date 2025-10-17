import os
from dotenv import load_dotenv
import telebot
from utils import load_prompt

# --- Загрузка токена из .env ---
dotenv_path = 'token.env'
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"File token.env not found on {dotenv_path}")

load_dotenv(dotenv_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Token not found in the file! Check file token.env")

bot = telebot.TeleBot(TOKEN)

# --- /start command handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text="Support", callback_data="support"),
        telebot.types.InlineKeyboardButton(text="Sales", callback_data="sales")
    )

    welcome_text = load_prompt("welcome")
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
