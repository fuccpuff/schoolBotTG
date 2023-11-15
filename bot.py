import telebot
from telebot import types
from config import BOT_TOKEN
import database

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = database.get_user_by_chat_id(message.chat.id)
    if user:
        bot.send_message(message.chat.id, "Ты уже зарегистрирован.")
    else:
        bot.send_message(message.chat.id, "Добро пожаловать! Давай зарегистрируем тебя. Как тебя зовут?")
        bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    class_buttons = [types.KeyboardButton(f'{i}') for i in range(5, 12)]
    markup.add(*class_buttons)
    msg = bot.reply_to(message, 'В каком ты классе?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_class_step, name)

def process_class_step(message, name):
    class_number = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    class_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж']
    for letter in class_letters:
        markup.add(types.KeyboardButton(letter))
    msg = bot.reply_to(message, 'Какая буква твоего класса?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_class_letter_step, name, class_number)

def process_class_letter_step(message, name, class_number):
    class_letter = message.text
    chat_id = message.chat.id
    database.add_user((chat_id, name, class_number, class_letter))
    bot.send_message(chat_id, f'Ты успешно зарегистрирован: {name}, класс {class_number}{class_letter}')

# Главный цикл для запуска бота
bot.polling(none_stop=True)