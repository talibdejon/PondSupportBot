# bot2.py
import os
import telebot
import auth
import features
from utils import load_token


# List to save mdn inside
user_mdns = {}

telegram_token = load_token("TELEGRAM")
bot = telebot.TeleBot(telegram_token)
print("POND mobile BOT is running...")


# === Load text prompt ===
def load_prompt(name):
    with open(f"resources/{name}.txt", "r", encoding="utf8") as file:
        return file.read()


# === Main menu keyboard ===
def main_menu_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="Contact Support", callback_data="support"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Contact Sales", callback_data="sales"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Check Usage", callback_data="check_usage"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Check Coverage", url="https://www.pondmobile.com/coverage-map-pm/"))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Refresh Line", callback_data="refresh_line"))
    return keyboard


# === Back / Main menu keyboard ===
def back_menu_keyboard(prev_section=None):
    keyboard = telebot.types.InlineKeyboardMarkup()
    if prev_section:
        keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️ Back", callback_data=prev_section))
    keyboard.add(telebot.types.InlineKeyboardButton(text="🏠 Main Menu", callback_data="main_menu"))
    return keyboard


# === /start command ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "📱 Welcome to POND Mobile Bot!\nChoose an option below:",
        reply_markup=main_menu_keyboard()
    )


# === Handle button presses ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "main_menu":
        bot.send_message(
            call.message.chat.id,
            "📱 Welcome to POND Mobile Bot!\nChoose an option below:",
            reply_markup=main_menu_keyboard()
        )

    elif call.data == "check_usage":
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="Share my phone", request_contact=True)
        keyboard.add(button)
        bot.send_message(call.message.chat.id, "Please share your phone number:", reply_markup=keyboard)

    # === Refresh Line (ask for phone number) ===
    elif call.data == "refresh_line":
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="Share my phone", request_contact=True)
        keyboard.add(button)
        bot.send_message(call.message.chat.id, "Please share your phone number to refresh your line:", reply_markup=keyboard)

    elif call.data == "support":
        try:
            content = load_prompt("support")
            bot.send_message(call.message.chat.id, content, reply_markup=back_menu_keyboard())
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "⚠️ File resources/support.txt not found.", reply_markup=back_menu_keyboard())

    elif call.data == "sales":
        try:
            content = load_prompt("sales")
            bot.send_message(call.message.chat.id, content, reply_markup=back_menu_keyboard())
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "⚠️ File resources/sales.txt not found.", reply_markup=back_menu_keyboard())

    elif call.data == "support_back":
        bot.send_message(
            call.message.chat.id,
            "🧑‍💻 Support menu:",
            reply_markup=back_menu_keyboard(prev_section="main_menu")
        )


# === Handle shared phone contact ===
@bot.message_handler(content_types=['contact'])
def process_contact(message):
    phone_number = message.contact.phone_number

    # Save MDN
    user_mdns[message.chat.id] = auth.normalize_mdn(phone_number)

    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Thanks! Verifying your account...", reply_markup=remove_keyboard)

    # Step 1: check if the number exists in BeQuick
    line_id = auth.get_line_id(phone_number)
    if not line_id:
        bot.send_message(message.chat.id, "❌ Your number is not registered as a POND mobile customer.")
        return

    # === Detect if user wanted to refresh line ===
    last_message = message.reply_to_message
    if last_message and "refresh your line" in (last_message.text or "").lower():
        result = features.handle_refresh_request(phone_number)
        if result.startswith("✅"):
            mdn = auth.normalize_mdn(phone_number)
            url = features.refresh_line(mdn)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Open Support Chat", url=url))
            bot.send_message(message.chat.id, "Click below to contact support:", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, result)
        return

    # Step 2: get usage info
    bot.send_message(message.chat.id, "Please wait, I'm checking your data usage...")
    user_usage = features.check_usage(line_id)
    bot.send_message(message.chat.id, f"{user_usage}", reply_markup=back_menu_keyboard(prev_section="main_menu"))


# === Start polling ===
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"[ERROR] Polling crashed: {e}")
