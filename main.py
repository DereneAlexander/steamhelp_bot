import telebot
from config import api_key

bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=["start"])
def bot_start(message):
    bot.send_message(message.chat.id, "Hello, " + message.from_user.first_name + "! Write 'KZT' or 'CNY' to convert your currency, or you can use /currency to see the actual currency.")
    currency_buttons(message)

def currency_buttons(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_usd = telebot.types.InlineKeyboardButton("USD", callback_data="USD")
    button_kzt = telebot.types.InlineKeyboardButton("KZT", callback_data="KZT")
    button_cny = telebot.types.InlineKeyboardButton("CNY", callback_data="CNY")
    markup.row(button_usd, button_kzt, button_cny)
    bot.send_message(message.chat.id, "Choose the currency", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.answer_callback_query(call.id)
    if call.data == "USD":
        bot.send_message(call.message.chat.id, "Enter the currency to convert to USD")
        bot.register_next_step_handler(call.message, usd_selected)
    elif call.data == "KZT":
        bot.send_message(call.message.chat.id, "Enter the currency to convert to KZT")
        bot.register_next_step_handler(call.message, kzt_selected)
    elif call.data == "CNY":
        bot.send_message(call.message.chat.id, "Enter the currency to convert to CNY")
        bot.register_next_step_handler(call.message, cny_selected)

global actual_usd_currency
actual_usd_currency = 1.00
def usd_selected(message):
    try:
        usd_currency = float(message.text.replace(",", "."))
        kzt_currency = usd_currency * actual_kzt_currency
        cny_currency = usd_currency * actual_cny_currency
        bot.send_message(message.chat.id, f"🇺🇸 - ${round(usd_currency, 2)} \n\n🇰🇿 - {round(kzt_currency, 2)}₸ \n🇨🇳 - ￥{round(cny_currency, 2)}")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Please enter a valid amount to convert to KZT.")
    currency_buttons(message)

global actual_kzt_currency
actual_kzt_currency = 450
def kzt_selected(message):
    try:
        kzt_currency = float(message.text.replace(",", "."))
        usd_currency = kzt_currency / actual_kzt_currency
        bot.send_message(message.chat.id, f"🇰🇿 - {round(kzt_currency, 2)}₸ \n\n🇺🇸 - ${round(usd_currency, 2)}")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Please enter a valid amount to convert to KZT.")
    currency_buttons(message)

global actual_cny_currency
actual_cny_currency = 7.24
def cny_selected(message):
    try:
        cny_currency = float(message.text.replace(",", "."))
        usd_currency = cny_currency / actual_cny_currency
        bot.send_message(message.chat.id, f"🇨🇳 - ￥{round(cny_currency, 2)} \n\n🇺🇸 - ${round(usd_currency, 2)}")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Please enter a valid amount to convert to CNY.")
    currency_buttons(message)

@bot.message_handler(commands=["currency"])
def bot_currency(message):
    actual_currency = "🇺🇸 - $1.00 \n\n"
    actual_currency += f"🇰🇿 - {actual_kzt_currency}₸\n"
    actual_currency += f"🇨🇳 - {actual_cny_currency}￥"
    bot.send_message(message.chat.id, actual_currency)

@bot.message_handler(content_types=["text"])
def bot_text(message):
    if message.text.lower().startswith("usd"):
        message.text = message.text.lower().replace("usd", "")
        usd_selected(message)
    elif message.text.lower().startswith("kzt"):
        message.text = message.text.lower().replace("kzt", "")
        kzt_selected(message)
    elif message.text.lower().startswith("cny"):
        message.text = message.text.lower().replace("cny", "")
        cny_selected(message)
    else:
        bot.send_message(message.chat.id, "FORTNITE BALLS, I'M GAY, I LIKE BOYS")
        currency_buttons(message)

def main():
    bot.infinity_polling()
if __name__ == "__main__":
    main()

