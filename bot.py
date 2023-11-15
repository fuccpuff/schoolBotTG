import telebot
from telebot import types
from config import BOT_TOKEN
import database

bot = telebot.TeleBot(BOT_TOKEN)  # инициализирую бота с токеном из файла конфигурации

# словарь для отслеживания состояний пользователей
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user = database.get_user_by_chat_id(chat_id)  # проверяю, есть ли пользователь в базе данных
    if user:
        bot.send_message(chat_id, "Ты уже зарегистрирован.")
        print(f"Пользователь {chat_id} уже зарегистрирован")  # добавляю отладочное сообщение
    else:
        user_states[chat_id] = 'AWAITING_NAME'  # устанавливаю состояние пользователя на ожидание имени
        bot.send_message(chat_id, "Добро пожаловать! Давай зарегистрируем тебя. Как тебя зовут?")
        print(f"Запрашиваю имя у пользователя {chat_id}")  # добавляю отладочное сообщение
        bot.register_next_step_handler(message, process_name_step)  # перехожу к следующему шагу

def process_name_step(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == 'AWAITING_NAME':
        name = message.text  # сохраняю имя пользователя
        user_states[chat_id] = 'AWAITING_CLASS'  # меняю состояние пользователя на ожидание класса
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        class_buttons = [types.KeyboardButton(f'{i}') for i in range(5, 12)]  # создаю кнопки для выбора класса
        markup.add(*class_buttons)
        msg = bot.reply_to(message, 'В каком ты классе?', reply_markup=markup)
        print(f"Запрашиваю класс у пользователя {chat_id}")  # добавляю отладочное сообщение
        bot.register_next_step_handler(msg, process_class_step, name)

def process_class_step(message, name):
    chat_id = message.chat.id
    if user_states.get(chat_id) == 'AWAITING_CLASS':
        class_number = message.text  # сохраняю номер класса
        user_states[chat_id] = 'AWAITING_CLASS_LETTER'  # меняю состояние пользователя на ожидание буквы класса
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        class_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж']  # создаю кнопки для выбора буквы класса
        for letter in class_letters:
            markup.add(types.KeyboardButton(letter))
        msg = bot.reply_to(message, 'Какая буква твоего класса?', reply_markup=markup)
        print(f"Запрашиваю букву класса у пользователя {chat_id}")  # добавляю отладочное сообщение
        bot.register_next_step_handler(msg, process_class_letter_step, name, class_number)

def process_class_letter_step(message, name, class_number):
    chat_id = message.chat.id
    if user_states.get(chat_id) == 'AWAITING_CLASS_LETTER':
        class_letter = message.text  # сохраняю букву класса
        database.add_user((chat_id, name, class_number, class_letter))  # добавляю пользователя в базу данных
        bot.send_message(chat_id, f'Ты успешно зарегистрирован: {name}, класс {class_number}{class_letter}')
        print(f"Пользователь {chat_id} зарегистрирован как {name}, класс {class_number}{class_letter}")  # добавляю отладочное сообщение
        del user_states[chat_id]  # удаляю состояние пользователя после завершения регистрации

# главный цикл для запуска бота
bot.polling(none_stop=True)
