import os
from dotenv import load_dotenv
import telebot
from utils import load_prompt
import auth
import features

# --- Загрузка токена из .env ---
dotenv_path = '.env'
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"File .env not found on {dotenv_path}")

load_dotenv(dotenv_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Token not found in the file! Check file .env")

bot = telebot.TeleBot(TOKEN)


# --- /start command handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(text="Support", callback_data="support"),
        telebot.types.InlineKeyboardButton(text="Sales", callback_data="sales"),
        telebot.types.InlineKeyboardButton(text="Check usage", callback_data="check_usage")
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

    elif call.data == "check_usage":
        bot.send_message(call.message.chat.id, "Please enter your MDN (phone number) to verify your account:")
        bot.register_next_step_handler(call.message, process_mdn)


# --- Проверка MDN и показ usage ---
def process_mdn(message):
    mdn = message.text.strip()

    if auth.is_customer(mdn):
        # Получаем usage из features.py
        user_usage = features.check_usage(mdn)

        usage_text = (
            "📊 *Usage Information*\n\n"
            "Here you can check your current balance, data usage, and plan limits.\n"
            "For detailed reports, please log in to your POND Mobile account or contact support at @pondsupport."
        )

        bot.send_message(
            message.chat.id,
            f"{usage_text}\n\n📊 Your current usage: {user_usage} MB",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Access denied. Your number is not registered as a POND Mobile customer."
        )


# --- Запуск бота ---
if __name__ == "__main__":
    print("Pond Mobile bot is running...")
    bot.polling(none_stop=True, interval=0, timeout=20)
