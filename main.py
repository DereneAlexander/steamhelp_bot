import telebot
from config import api_key

bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=["start"])
def bot_start(message):
    currency_buttons(message)

def currency_buttons(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_kzt = telebot.types.InlineKeyboardButton("KZT", callback_data="KZT")
    button_cny = telebot.types.InlineKeyboardButton("CNY", callback_data="CNY")
    markup.row(button_kzt, button_cny)
    bot.send_message(message.chat.id, "Choose the currency", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id)
    if call.data == "KZT":
        bot.send_message(call.message.chat.id, "Enter the currency to convert to KZT")
        bot.register_next_step_handler(call.message, kzt_selected)
    elif call.data == "CNY":
        bot.send_message(call.message.chat.id, "Enter the currency to convert to CNY")
        bot.register_next_step_handler(call.message, cny_selected)

global actual_kzt_currency
actual_kzt_currency = 450
def kzt_selected(message):
    kzt_currency = message.text
    if message.text.lower().startswith("kzt"):
        kzt_currency = float(message.text.split(" ")[1])
    usd_currency = float(kzt_currency) / actual_kzt_currency
    bot.send_message(message.chat.id, f"🇰🇿 - {round(float(kzt_currency), 2)}₸ \n\n🇺🇸 - ${round(usd_currency, 2)}")
    currency_buttons(message)

global actual_cny_currency
actual_cny_currency = 7.24
def cny_selected(message):
    cny_currency = message.text
    if message.text.lower().startswith("cny"):
        cny_currency = float(message.text.split(" ")[1])
    usd_currency = float(cny_currency) / actual_cny_currency
    bot.send_message(message.chat.id, f"🇨🇳 - ￥{round(float(cny_currency), 2)} \n\n🇺🇸 - ${round(usd_currency, 2)}")
    currency_buttons(message)

@bot.message_handler(commands=["currency"])
def bot_currency(message):
    actual_currency = "🇺🇸 - $1.00 \n\n"
    actual_currency += f"🇰🇿 - {actual_kzt_currency}₸\n"
    actual_currency += f"🇨🇳 - {actual_cny_currency}￥"
    bot.send_message(message.chat.id, actual_currency)

@bot.message_handler(content_types=["text"])
def bot_text(message):
    if message.text.startswith("kzt"):
        kzt_selected(message)
    elif message.text.startswith("cny"):
        cny_selected(message)
    else:
        bot.send_message(message.chat.id, "FORTNITE BALLS, I'M GAY, I LIKE BOYS")

def main():
    bot.infinity_polling()
main()