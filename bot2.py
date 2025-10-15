# import telebot
# from telebot import types
# from utils import *
#
# # Initialize the bot with your token
# bot = telebot.TeleBot("8350673621:AAGN6l8JG3zIoP-KHmXgFBmACbS2lcTdabg")
#
#
# def load_message(name):
#     with open("resources/" + name + ".txt", "r", encoding="utf8") as file:
#         return file.read()
#
# # --- /start command handler ---
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     """
#     Handles the /start command and sends a welcome message
#     with inline buttons for Support and Sales.
#     """
#     # Create inline keyboard
#     keyboard = types.InlineKeyboardMarkup()
#     support_btn = types.InlineKeyboardButton(text="Support", callback_data="support")
#     sales_btn = types.InlineKeyboardButton(text="Sales", callback_data="sales")
#
#     # Add buttons to the keyboard
#     keyboard.add(support_btn, sales_btn)
#
#     # Send welcome message
#     welcome_text = (
#         "Welcome to Pond Mobile! How can I help you?\n\n"
#         "To talk to our support, please click below.\n"
#         "To contact sales, please click below."
#     )
#     bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)
#
#
# # --- Callback query handler ---
# @bot.callback_query_handler(func=lambda call: True)
# def handle_callback(call):
#     """
#     Handles button clicks from the inline keyboard.
#     """
#     if call.data == "support":
#         bot.send_message(
#             call.message.chat.id,
#             "You selected *Support*. Please describe your issue, "
#             "and our support team will contact you shortly.",
#             parse_mode="Markdown"
#         )
#     elif call.data == "sales":
#         bot.send_message(
#             call.message.chat.id,
#             "You selected *Sales*. Please provide some details about your inquiry, "
#             "and our sales team will reach out to you.",
#             parse_mode="Markdown"
#         )
#
#
# # --- Run the bot ---
# if __name__ == "__main__":
#     print("Pond Mobile bot is running...")
#     bot.polling(none_stop=True)



import telebot
from telebot import types
import re

# --- Bot token ---
bot = telebot.TeleBot("8350673621:AAGN6l8JG3zIoP-KHmXgFBmACbS2lcTdabg")

# --- Function to load messages from txt files ---
def load_message(name):
    with open(f"resources/{name}.txt", "r", encoding="utf8") as file:
        return file.read()

# --- Escape text for MarkdownV2 ---
def escape_markdown(text):
    escape_chars = r"\_*[]()~`>#+-=|{}.! "
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

# --- /start command handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text="Support", callback_data="support"),
        types.InlineKeyboardButton(text="Sales", callback_data="sales")
    )

    # Load welcome message from txt file
    welcome_text = load_message("welcome")
    welcome_text = escape_markdown(welcome_text)  # Escape for MarkdownV2

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=keyboard,
        parse_mode="MarkdownV2"
    )

# --- Callback query handler ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "support":
        support_text = load_message("support")
        support_text = escape_markdown(support_text)
        bot.send_message(
            call.message.chat.id,
            support_text,
            parse_mode="MarkdownV2"
        )
    elif call.data == "sales":
        sales_text = load_message("sales")
        sales_text = escape_markdown(sales_text)
        bot.send_message(
            call.message.chat.id,
            sales_text,
            parse_mode="MarkdownV2"
        )

# --- Run the bot ---
if __name__ == "__main__":
    print("Pond Mobile bot is running...")
    bot.polling(none_stop=True, interval=0, timeout=20)
