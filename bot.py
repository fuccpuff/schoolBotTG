import telebot
from telebot import types

bot = telebot.TeleBot('6613138162:AAHyJ9fpD0FaWw8Cw3PHfk-PN0hwgX9ifT4')

# Обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start(message):
    # Создаю клавиатуру с кнопками для каждого класса
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    class_buttons = [types.KeyboardButton(f'В {i}-м') for i in range(5, 12)]
    markup.add(*class_buttons)
    # Отправляю сообщение пользователю с вопросом о классе
    bot.reply_to(message, 'В каком классе ты учишься?', reply_markup=markup)

# Обработчик выбора класса
def on_click(message):
    class_number = message.text.split()[1][:-2]  # Извлекаю номер класса из сообщения
    bot.send_message(message.chat.id, f'Ты выбрал {class_number}-й класс')
    process_class_selection(message, class_number)

# Обработчик выбора буквы класса
def letter_selected(message):
    bot.send_message(message.chat.id, f'Ты в классе {message.text}')

# Функция для обработки выбора класса и буквы класса
def process_class_selection(message, class_number):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # Создаю кнопки для каждой буквы класса от А до Ж
    class_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж']
    letter_buttons = [types.KeyboardButton(f'В {class_number}{letter} классе') for letter in class_letters]
    markup.add(*letter_buttons)
    # Отправляю сообщение пользователю с вопросом о букве класса
    bot.send_message(message.chat.id, f'Какая у тебя буква в {class_number}-м классе?', reply_markup=markup)
    # Устанавливаю следующий шаг в обработке сообщений
    bot.register_next_step_handler(message, letter_selected)

# Регистрирую обработчик сообщений после стартовой команды
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    on_click(message)

# Главный цикл для запуска бота
bot.polling(none_stop=True)
