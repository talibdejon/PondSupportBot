import os
from dotenv import load_dotenv
import telebot
from utils import load_prompt
import auth
import features

# --- loading token.env ---
dotenv_path = 'telega.env'
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(f"File telega.env not found on {dotenv_path}")

load_dotenv(dotenv_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Token not found in the file! Check file telega.env")

bot = telebot.TeleBot(TOKEN)


# --- /start command handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    # button vertically
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Support", callback_data="support")
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Sales", callback_data="sales")
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Check usage", callback_data="check_usage")
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton(text="Coverage", url='https://www.pondmobile.com/coverage-map-pm/')
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
        bot.send_message(call.message.chat.id, "Please enter your 10-digits POND mobile number:")
        bot.register_next_step_handler(call.message, process_mdn)


# --- checking MDN & preview usage ---
def process_mdn(message):
    mdn = message.text.strip()

    # The mdn should be 10 digits
    if not mdn.isdigit() or len(mdn) != 10:
        bot.send_message(
            message.chat.id,
            "⚠️ Invalid input. Please enter a valid 10-digit phone number (digits only, no + or text)."
        )
        bot.register_next_step_handler(message, process_mdn)
        return

    # checking authorisation via auth.py
    if auth.is_customer(mdn):
        # getting usage из features.py
        user_usage = features.check_usage(mdn)

        # text usage from file usage.txt
        try:
            with open("usage.txt", "r", encoding="utf-8") as f:
                usage_text = f.read()
        except FileNotFoundError:
            usage_text = "📊 Usage information is currently unavailable."

        bot.send_message(
            message.chat.id,
            f"{usage_text}\n\n📊 Your current usage: {user_usage} MB",
            parse_mode="Markdown"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Your number is not registered as a POND mobile customer."
        )


# --- start bot ---
if __name__ == "__main__":
    print("Pond Mobile bot is running...")
    bot.polling(none_stop=True, interval=0, timeout=20)
