import telebot
from telebot import types
from transliterate import to_cyrillic,to_latin
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
      host="localhost",
    user="root",
    password="",
    database="loyiha"
)

cursor = db.cursor()

token='6677443957:AAHBDc8pKSKbJybJoAbJP43KMkxGhFEgSp8'

bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    # Get the user's telegram_id
    telegram_id = message.from_user.id
   
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM lkhisob2 WHERE tg_tr = %s", (telegram_id,))
    result = cursor.fetchone()
    if result:
        # The user is already registered
        bot.send_message(message.chat.id, f"Salom, {result[1]}! Siz ro'yxatdan o'tgansiz.\n Istalgan so'zni kiriting : lotindan kirilLga yoki aksincha !")
    else:
        # The user is new and needs to register
        bot.send_message(message.chat.id, "Salom, yangi foydalanuvchi! Siz ro'yxatdan o'tish uchun ismingizni kiriting.")
        # Set the next step handler to get the user's name
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    # Get the user's name
    name = message.text
    # Get the user's telegram_id
    telegram_id = message.from_user.id
    # Insert the user's data into the database
    cursor.execute("INSERT INTO lkhisob2 (tr, ism, tg_tr) VALUES ( NULL, %s, %s)", (name, telegram_id))
    db.commit()
    # Send a confirmation message
    bot.send_message(message.chat.id, f"Rahmat, {name}! Siz ro'yxatdan o'tdingiz. /start bosing")

@bot.message_handler(func=lambda message:True)
def echo_all(message):
    xabar= message.text
    javob = lambda xabar: to_cyrillic(xabar) if xabar.isascii() else to_latin(xabar)
    bot.reply_to(message, javob(xabar))
bot.polling()

'''
@bot.message_handler(commands=['start'])
def start(message):
    # Get the user's telegram_id
    telegram_id = message.from_user.id
   
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM account WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()
    if result:
        # The user is already registered
        bot.send_message(message.chat.id, f"Salom, {result[1]}! Siz ro'yxatdan o'tgansiz.")


        @bot.message_handler(commands=['start'])
def send_welcome(message):
  javob = "Assalomu alaykum, Botimizga tashrif buyurganingizdan mamnunmiz!!!"
  javob+="\nMatnni kiriting: "
    # Get the user's telegram_id
     telegram_id = message.from_user.id
   
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM account WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()
    if result:
        # The user is already registered
        bot.send_message(message.chat.id, f"Salom, {result[1]}! Siz ro'yxatdan o'tgansiz.")
      bot.reply_to(message, javob)
'''