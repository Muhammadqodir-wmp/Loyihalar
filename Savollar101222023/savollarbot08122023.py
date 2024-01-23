from aloqa import db, TOKEN
import telebot
from telebot import types
import time

#Aloqa

bot = telebot.TeleBot(TOKEN)

cursor = db.cursor()

#Ro'yxatdan o'tish

@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id
    cursor.execute("SELECT * FROM hisoblar WHERE telegram_tr = %s", (telegram_id,))
    result = cursor.fetchone()
    if result:
        bot.send_message(message.chat.id, f"Salom, {result[1]}! Siz ro'yxatdan o'tgansiz.")
        send_welcome(message)

    else:
       
        bot.send_message(message.chat.id, "Salom, yangi foydalanuvchi! Siz ro'yxatdan o'tish uchun ismingizni kiriting.")
        bot.register_next_step_handler(message, get_name)
       
        
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('Asosiy sahifa')
    button2 = types.KeyboardButton('Natijalar')
    button3 = types.KeyboardButton('Hisobim')
    button4 = types.KeyboardButton('Yordamchi')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, "Iltimos, tugmalardan birini tanlang: ", reply_markup=keyboard)
    
@bot.message_handler(func=lambda message: message.text == 'Asosiy sahifa')
def asosiy (message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
    button5 = types.KeyboardButton('Savollar')
    button6 = types.KeyboardButton('Mantiqiy savollar')
    
    keyboard.add(button5, button6)
    bot.send_message(message.chat.id, "Iltimos, tugmalardan birini tanlang: ", reply_markup=keyboard)
    
@bot.message_handler(func=lambda message: message.text == 'Savollar')
def asosiy2 (message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
    button51 = types.KeyboardButton('Tasodifiy')
    button62 = types.KeyboardButton('Matematika')
    keyboard.add(button51, button62)
    bot.send_message(message.chat.id, "Iltimos, tugmalardan birini tanlang: ", reply_markup=keyboard)
def get_name(message):
    name = message.text
    telegram_id = message.from_user.id
    msg = bot.send_message(message.chat.id, "Iltimos, shaharingizni kiriting.")
    bot.register_next_step_handler(msg, get_city, name, telegram_id)

def get_city(message, name, telegram_id):
    city = message.text
    cursor.execute("INSERT INTO hisoblar (tr, ismi, viloyat, telegram_tr) VALUES ( NULL, %s, %s, %s)", (name, city, telegram_id))
    db.commit()
    chat_id = message.chat.id
    if chat_id == 1942108422:
        bot.send_message(message.chat.id,"Yangi foydalanuvchi")   
    bot.send_message(message.chat.id, f"Rahmat, {name}! Siz ro'yxatdan o'tdingiz. /start bosing ")


@bot.message_handler(func=lambda message: message.text == 'Hisobim')
def get_user_info(message):
    cursor.execute("SELECT ismi, telegram_tr, natija , viloyat FROM hisoblar WHERE telegram_tr = %s", (message.chat.id,))
    result = cursor.fetchone()
    if result:
        bot.reply_to(message, f"Foydalanuvchi nomi: {result[0]}, \nTelegram ID: {result[1]}, \nNatija: {result[2]}, \nViloyat: {result[3]}")
    else:
        bot.reply_to(message, "Foydalanuvchi topilmadi.")
        
#Natijalar bo'limi
 
@bot.message_handler(func=lambda message: message.text == 'Natijalar')
def natja(message):
    cursor.execute("SELECT * FROM hisoblar ORDER BY natija DESC LIMIT 10;")
    jadval = cursor.fetchall()
    if jadval:
        reply = ""
        for i, user in enumerate(jadval, start=1):
            reply += f"{i}: {user[1]}, {user[3]}\n"
        bot.reply_to(message,"Natijalar Yuqori 10talik: \n" + reply)
    else:
        bot.reply_to(message, "Foydalanuvchi topilmadi.")
        
#Tasodifiy savollar

def yakun(message):
    keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,one_time_keyboard=True)
    button10 = types.KeyboardButton('Yakunlash ')
    keyboard3.add(button10)
    bot.send_message(message.chat.id, "Yakunlash uchun tugmani bosing:", reply_markup=keyboard3)


javoblar = 0
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
       data = call.data.split(",")
       cursor.execute("SELECT `tr` , `javob`  FROM savollar WHERE `tr` = %s AND `javob` = %s", (data[0],data[1])) 
       result = cursor.fetchone()
       if result is not None:
           global javoblar
           bot.answer_callback_query(call.id, "To`g`ri!")
           cursor.execute("UPDATE hisoblar SET natija = natija + 10 WHERE telegram_tr = %s", (call.from_user.id,))
           javoblar = javoblar + 1
                    
           bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
           db.commit()
       else:
           bot.answer_callback_query(call.id, "Xato!")
           cursor.execute("UPDATE hisoblar SET natija = natija -1 WHERE telegram_tr = %s", (call.from_user.id,))
           bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
           db.commit()
           
@bot.message_handler(commands=['hisobot'])
def send_stats(message):
    chat_id = message.chat.id
    if chat_id == 1942108422:  # Replace with your admin chat ID
        cursor.execute("SELECT COUNT(*) FROM hisoblar ")
        total_users = cursor.fetchone()[0]
        bot.reply_to(message, f"Jami foydalanuvchilar: {total_users}")
    else:
        bot.reply_to(message, "Sizga ko'rish mumkin emas.")


run_flag = True
@bot.message_handler(func=lambda message: message.text == 'Tasodifiy')
def quiz(message):
    global run_flag
    run_flag = True
    bot.send_message(message.chat.id, "Savollar 11tadan berib boriladi.Har biriga 11soniyadan vaqt beriladi.Har bir to`g`ri javob uchun 10 bahodan  qo'shilib boriladi .Xato javob uchun -1 bahodan ayirilib boriladi .Jami nechta to`g`ri javob berganingizni 180 soniyadan keyin ko'rishingiz mumkin!")
    yakun(message)
    for savollar in range(1,12):
        if not run_flag:
            break
        
        cursor.execute("SELECT * FROM savollar WHERE tr BETWEEN 1 AND 999 ORDER BY RAND() LIMIT %s; ", ())
        question = cursor.fetchone()
                
        markup = types.InlineKeyboardMarkup(row_width=2)
                
        markup.add(types.InlineKeyboardButton("A", callback_data=str(question[0])+","+"A"),
        types.InlineKeyboardButton(text="B", callback_data=str(question[0])+","+"B"),
        types.InlineKeyboardButton(text="D", callback_data=str(question[0])+","+"D"),
        types.InlineKeyboardButton(text="E", callback_data=str(question[0])+","+"E"))
                
        bot.send_message(message.chat.id, str(savollar) + "-savol: \n" + question[1], reply_markup=markup)
        time.sleep(1)
       
    
    bot.send_message(message.chat.id, "Savollar to'plami tugadi! To`g`ri javoblar soni : " + str(javoblar))
    send_welcome(message)
#matematika bo'limi
    @bot.message_handler(func=lambda message: message.text == 'Matematika')
    def quiz2(message):
        global run_flag
        run_flag = True
        bot.send_message(message.chat.id, "Savollar 11tadan berib boriladi.Har biriga 11soniyadan vaqt beriladi!")
        yakun(message)
        for savollar in range(1,12):
            if not run_flag:
                break
            
            cursor.execute("SELECT * FROM savollar WHERE tr BETWEEN 999 AND 1999 ORDER BY RAND() LIMIT 1;")
            question = cursor.fetchone()
                    
            markup = types.InlineKeyboardMarkup(row_width=2)
                    
            markup.add(types.InlineKeyboardButton("A", callback_data=str(question[0])+","+"A"),
            types.InlineKeyboardButton(text="B", callback_data=str(question[0])+","+"B"),
            types.InlineKeyboardButton(text="D", callback_data=str(question[0])+","+"D"),
            types.InlineKeyboardButton(text="E", callback_data=str(question[0])+","+"E"))
                    
            bot.send_message(message.chat.id, str(savollar) + "-savol: \n" + question[1], reply_markup=markup)
            time.sleep(11)
        
        bot.send_message(message.chat.id, "Savollar to'plami tugadi! To`g`ri javoblar soni : " + str(javoblar))

@bot.message_handler(func=lambda message: message.text == 'Yakunlash')
def stop_quiz(message):
    global run_flag
    run_flag = False
    
    bot.send_message(message.chat.id, "Savollar to'plami to'xtatildi!\n Bosh bo'limga o'tish uchun /start bosing")

bot.infinity_polling()
