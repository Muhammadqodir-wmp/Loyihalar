import telebot

def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('Asosiy sahifa')
    button2 = types.KeyboardButton('Natijalar')
    button3 = types.KeyboardButton('Hisobim')
    button4 = types.KeyboardButton('Yordamchi')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "Iltimos, tugmalardan birini tanlang: ", reply_markup=keyboard)


def yakun(message):
    keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
    button10 = types.KeyboardButton('Yakunlash ')
    keyboard3.add(button10)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=keyboard3)

def get_name(message):
    # Get the user's name
    name = message.text
    # Get the user's telegram_id
    telegram_id = message.from_user.id

    # Ask the user for their city
    msg = bot.send_message(message.chat.id, "Iltimos, shaharingizni kiriting.")
    bot.register_next_step_handler(msg, get_city, name, telegram_id)

def get_city(message, name, telegram_id):
    # Get the user's city
    city = message.text

    # Insert the user's data into the database
    cursor.execute("INSERT INTO hisoblar (tr, ismi, viloyat, telegram_tr) VALUES ( NULL, %s, %s, %s)", (name, city, telegram_id))
    db.commit()

    # Send a confirmation message
    bot.send_message(message.chat.id, f"Rahmat, {name}! Siz ro'yxatdan o'tdingiz. /start bosing ")
