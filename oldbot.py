import telebot
import sqlite3
import time
from random import randint
from config import old_api_key

bot = telebot.TeleBot(old_api_key)

#/start
@bot.message_handler(commands=['start'])
def start(message):
    connection = sqlite3.connect('my_database.sqlite3')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    username TEXT,
    size INTEGER DEFAULT 0,
    regiter INTEGER DEFAULT 0,
    last_used INTEGER DEFAULT -1
    )
    ''')

    chat_id = message.chat.id
    cursor.execute("SELECT chat_id FROM Users WHERE chat_id = ?", (chat_id,))
    find_user = cursor.fetchone()
    if find_user is None:
        cursor.execute('INSERT INTO Users(chat_id) VALUES (?)', (chat_id,))
    connection.commit()

    cursor.execute('SELECT * FROM Users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()
    if user[3] == 0:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.5)
        bot.send_message(chat_id, 'Напиши своё погоняло, воин')
        bot.register_next_step_handler(message, user_firstsize)
    else:
        cursor.execute('SELECT username FROM Users WHERE chat_id = ?', (chat_id,))
        username = cursor.fetchone()[0]
        bot.send_message(chat_id, 'Ты еблан? Какой старт, если ты уже дырявый?')
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(0.5)
        bot.send_message(chat_id, f'/buttons пиши, {username}')
        bot.send_chat_action(chat_id, 'choose_sticker')
        time.sleep(0.5)
        bot.send_sticker(chat_id, sticker='CAACAgIAAxkBAAELWvZlxdZjKNgjR_iPcPWZppLJ9qRVOAACni8AAuf3iUu6dpeCUBYg1DQE')


#continue registration
def user_firstsize(message):
    connection = sqlite3.connect('my_database.sqlite3')
    cursor = connection.cursor()
    username = message.text
    
    cursor.execute("UPDATE Users SET username = ?, regiter = 1 WHERE chat_id = ?", (username, message.chat.id))
    connection.commit()

    cursor.execute('SELECT size FROM Users WHERE chat_id = ?', (message.chat.id,))
    dick_size = cursor.fetchone()
    dick_firstsize = randint(5, 10)
    cursor.execute('UPDATE Users SET size = ? WHERE chat_id = ?', (dick_firstsize, message.chat.id))
    connection.commit()
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, f'Поздравляю с регистрацией, твой размер составляет {dick_size[0] + dick_firstsize}см, а теперь удали доту и можешь продолжить')
    bot.send_chat_action(message.chat.id, 'choose_sticker')
    time.sleep(0.5)
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJuIGWlIIYY840_hY9qTRKvKRvT8utXAAIKOAACey3YS20IA5Mw9cn2NAQ')
    

#/buttons
markup = None
@bot.message_handler(commands=['buttons'])
def buttons(message):
    global markup
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('Теребить🎰', callback_data='dick')
    button2 = telebot.types.InlineKeyboardButton('Топ теребителей👑', callback_data='leaders')
    markup.row(button1, button2)
    button3 = telebot.types.InlineKeyboardButton('Инфо📊', callback_data='info')
    button4 = telebot.types.InlineKeyboardButton('Команды⚙️', callback_data='commands')
    button5 = telebot.types.InlineKeyboardButton('Помощь💻', callback_data='support')
    markup.row(button3, button4, button5)

    bot.send_message(message.chat.id, 'Ну давай, выбирай', reply_markup=markup)


#callback
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    #Теребить
    if callback.data == 'dick':
        connection = sqlite3.connect('my_database.sqlite3')
        cursor = connection.cursor()
        cursor.execute('SELECT size FROM Users WHERE chat_id = ?', (callback.message.chat.id,))
        dick_size = cursor.fetchone()
        dick_dailisize = randint(-5, 10)
        nedotrax = randint(1, 28)
        
        cursor.execute('SELECT username FROM Users WHERE chat_id = ?', (callback.message.chat.id,))
        username = cursor.fetchone()

        if not can_access_changed(callback.message):
            return
        if nedotrax == 28:
            bot.edit_message_text(f'Мне очень жалко, {username[0]}, но.... ХЫХВВХЫЫВХВХЫХВХЫВЫХ, ЛОХ ЕБАНЫЙ, У ТЕБЯ ЧЛЕН ОТСОХ. ТЕПЕРЬ У ТЕБЯ 0СМ, ХЫВАХХЫВАХЫВАХХЫВАХЫВАХХЫВАХ', callback.message.chat.id, callback.message.message_id)
            cursor.execute('UPDATE Users SET size = ? WHERE chat_id = ?', (0, callback.message.chat.id))
        if dick_dailisize > 0:
            bot.edit_message_text(f'Поздравляю, {username[0]}, твой боевой аппарат увеличился на {dick_dailisize}см и теперь составляет: {dick_size[0] + dick_dailisize}см', callback.message.chat.id, callback.message.message_id)
        elif dick_dailisize == 0:
            bot.edit_message_text(f'Поздравляю, {username[0]}, твой агрегат не изменился и по-прежнему составляет: {dick_size[0] + dick_dailisize}см', callback.message.chat.id, callback.message.message_id)
        else:
            bot.edit_message_text(f'К сожалению, {username[0]}, твой одноглазый уменьшился на {abs(dick_dailisize)}см и теперь составляет: {dick_size[0] + dick_dailisize}см', callback.message.chat.id, callback.message.message_id)

        bot.answer_callback_query(callback.id, text='Ебет Эйнштейн Ньютона, а тот чертит квадрат на полу и улыбается. Его Эйнштейн спрашивает: "Хули ты ржешь, я же тебя в жопу ебу. А тот ему...', show_alert=False)
        buttons(callback.message)
    #Рейтинг
    elif callback.data == 'leaders':
        connection = sqlite3.connect('my_database.sqlite3')
        cursor = connection.cursor()
        cursor.execute('SELECT username, size FROM Users ORDER BY size DESC')
        top = cursor.fetchall()
        top_text = ''
        for i in range(min(len(top), 10)):
            top_text += f'{i+1}. {top[i][0]} - {top[i][1]}см\n'
        cursor.execute('SELECT * FROM Users ORDER BY size DESC')
        user_info = cursor.fetchall()
        for user in user_info:
            if user[1] == callback.message.chat.id:
                place = user
                break
        top_text += f'\nТвое место в рейтинге: {place[0]}.\n'
        bot.send_chat_action(callback.message.chat.id, 'typing')
        time.sleep(0.5)
        bot.edit_message_text(f'Топ теребителей: \n{top_text}', callback.message.chat.id, callback.message.message_id)

        buttons(callback.message)
    #Информация
    elif callback.data == 'info':
        markup_back = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton('« Назад', callback_data='back') 
        markup_back.row(button_back)
        bot.edit_message_text('Этот бот создан исключительно в развлекательных целях, автор не пытается оскорбить кого-либо, но ты иди нахуй', callback.message.chat.id, callback.message.message_id, reply_markup=markup_back)
    #Возврат для инфы
    elif callback.data == 'back':
        bot.edit_message_text('Ну давай, выбирай', callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    #Команды
    elif callback.data == 'commands':
        markup_back = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton('« Назад', callback_data='back') 
        markup_back.row(button_back)
        bot.send_chat_action(callback.message.chat.id, 'typing')
        time.sleep(0.5)
        bot.edit_message_text('Вот объясни мне, ты конченный? У тебя кнопка МЕНЮ есть, а ты жмешь "Команды". /dick - сосать мой хуй, вот команда тебе, используй, пока разраб снова не спился', callback.message.chat.id, callback.message.message_id, reply_markup=markup_back)
    #Помощь
    elif callback.data == 'support':
        button_faq = telebot.types.InlineKeyboardButton('FAQ', callback_data='faq')
        button_support = telebot.types.InlineKeyboardButton('Live Support', callback_data='live_support')
        button_back = telebot.types.InlineKeyboardButton('« Назад', callback_data='back')
        global markup_sup
        markup_sup = telebot.types.InlineKeyboardMarkup()
        markup_sup.row(button_faq, button_support)
        markup_sup.row(button_back)
        bot.edit_message_text('Вообще, любая проблема со мной - твоя проблема, так что решай её сам. Но если совсем уже проблемы с головой, то вот:', callback.message.chat.id, callback.message.message_id, reply_markup=markup_sup)
    #FAQ
    elif callback.data == 'faq':
        markup_back = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton('« Назад', callback_data='sup_back') 
        markup_back.row(button_back)
        bot.edit_message_text('Q - Что общего между негром и велосипедом?\nA - И то и то работает на цепи\nQ - Какие 3 белые вещи есть у негра?\nA - Глаза, зубы и хозяин', callback.message.chat.id, callback.message.message_id, reply_markup=markup_back)
    #Live Support
    elif callback.data == 'live_support':
        markup_back = telebot.types.InlineKeyboardMarkup()
        button_back = telebot.types.InlineKeyboardButton('« Назад', callback_data='sup_back') 
        markup_back.row(button_back)
        bot.edit_message_text('Пиши этому додику: @DereneAlexander, если уже совсем конченный', callback.message.chat.id, callback.message.message_id, reply_markup=markup_back)

    elif callback.data == 'sup_back':
        bot.edit_message_text('Вообще, любая проблема со мной - твоя проблема, так что решай её сам. Но если совсем уже проблемы с головой, то вот:', callback.message.chat.id, callback.message.message_id, reply_markup=markup_sup)
    elif callback.data == 'back':
        bot.edit_message_text('Ну давай, выбирай:', callback.message.chat.id, callback.message.message_id, reply_markup=markup)

def can_access_changed(message):
    connection = sqlite3.connect('my_database.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT last_used FROM Users WHERE chat_id = ?", (message.chat.id,))
    last_access_time = cursor.fetchone()
    if last_access_time[0] == -1 or (last_access_time[0] is not None and time.time() - last_access_time[0] >= 600):
        cursor.execute("UPDATE Users SET last_used = ? WHERE chat_id = ?", (time.time(), message.chat.id))
        connection.commit()
        return True
    
    else:
        remaining_time = 60 - (time.time() - last_access_time[0])
        bot.edit_message_text(f'Вы можете использовать эту кнопку только раз в минуту. Подождите еще {round(remaining_time)} секунд', message.chat.id, message.message_id)
        buttons(message)
        return False


#/message
@bot.message_handler(commands=['message'])
def send_message(message):

    admin_id = 936694283

    connection = sqlite3.connect('my_database.sqlite3')
    cursor = connection.cursor()

    if message.from_user.id == admin_id:
        cursor.execute('SELECT chat_id FROM Users')
        users_id = cursor.fetchall()
        text = message.text.split(' ', 1)[1]
        for user in users_id:
            chat_id = user[0]
            bot.send_message(chat_id, text, parse_mode='HTML')
    else:
        bot.send_chat_action('typing')
        time.sleep(0.5)
        bot.send_message(message.chat.id, 'Куда погнал, лысый. Вот представь картину: сидит твоя мать на стуле, на табуретке, а я к ей с двух ног подлетаю и цветы дарю. Представил? Так вот она тебе права не давала делать рассылку всем, кому интересна жизнь')
    

#/dick
@bot.message_handler(commands=['dick'])
def dick(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Думаешь, если я твоей матери выбью зубы прямо щас, она оплатит тебе интернет? Ну вот значит пора делать здравые действия и НАРАЩИВАТЬ ХУ... потенциал. Так вот, я тебе даю всего один вариант, ты его используешь')
    
    doc_file = open('trojan.dickcoin.miner.pdf', 'rb')
    bot.send_document(message.chat.id, document=doc_file)
    doc_file.close()

    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'В данном документе зашифровано послание. Сможешь его разгадать - станешь человеком. Нет - пошел нахуй')
    
    bot.send_chat_action(message.chat.id, 'choose_sticker')
    time.sleep(0.5)
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJuGGWlAAFB3QABCeR0_xjvoS7GlPv_gZQAAik-AAIY3tlLC4vEIT9J0jY0BA')

    buttons(message)


#answers
@bot.message_handler()
def answers(message):
    connection = sqlite3.connect('my_database.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM Users WHERE chat_id = ?', (message.chat.id,))
    username = cursor.fetchone()
    connection.close()
    if username is None:
        bot.send_message(message.chat.id, 'Пройди сначала регистрацию, дурик. Дам подсказку, напиши /start')

    if message.text.lower() == 'привет' or message.text.lower() == 'здарова':
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.5)
        bot.send_message(message.chat.id, 'Ну здарова, кабан. Чё расскажешь?😎')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        time.sleep(0.5)
        bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJuGGWlAAFB3QABCeR0_xjvoS7GlPv_gZQAAik-AAIY3tlLC4vEIT9J0jY0BA')

    elif message.text.lower() == 'пока':
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.5)
        bot.send_message(message.chat.id, f'Давай, катись отсюда, {message.from_user.first_name}')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        time.sleep(0.5)
        bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJuHmWlC_4CnERkzHq5rXbw5MlV6dlXAAJRNQACJsnRS_MfiIrY0D1vNAQ')
    
    elif message.text.lower() == 'как дела?' or message.text.lower() == 'как дела':
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.5)
        bot.send_message(message.chat.id,'Пока все громко смеялись, он тихо занимался в зале. Знакомо такое, нет? А мне до Китая. Я робот, а ты животное, так что у меня всё гуд, а вот мой создатель... Лучше не знать')
        photo_file = open('pavel.jpg', 'rb')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        time.sleep(1)
        bot.send_photo(message.chat.id, photo=photo_file)
        photo_file.close()

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(0.5)
        bot.send_message(message.chat.id, f'{message.text}, {username[0]})')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        time.sleep(0.5)
        bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJuGmWlAAGMVn0XHlbjHqm1-yHRf_I29wACiDYAAlBa2UtjuPuZrC9E-TQE')


bot.polling(non_stop=True, interval=0)