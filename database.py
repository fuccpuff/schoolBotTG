import sqlite3

def create_connection():
    # пытаюсь создать соединение с базой данных sqlite
    try:
        conn = sqlite3.connect("school_bot.db")  # указываю название файла базы данных
        return conn  # возвращаю объект соединения
    except Exception as e:
        print("Ошибка при создании соединения с базой данных:", e)  # печатаю ошибку, если она возникает

def add_user(user):
    # функция для добавления нового пользователя в базу данных
    conn = create_connection()  # создаю новое соединение с базой данных
    try:
        sql = ''' INSERT INTO users(chat_id, name, class_number, class_letter)
                  VALUES(?,?,?,?) '''  # sql запрос для вставки данных пользователя
        cur = conn.cursor()  # создаю курсор для выполнения запросов
        cur.execute(sql, user)  # выполняю запрос с данными пользователя
        conn.commit()  # подтверждаю изменения в базе данных
    except Exception as e:
        print("Ошибка при добавлении пользователя:", e)  # печатаю ошибку, если она возникает
    finally:
        conn.close()  # закрываю соединение с базой данных

def get_user_by_chat_id(chat_id):
    # функция для получения пользователя по его chat_id
    conn = create_connection()  # создаю новое соединение с базой данных
    try:
        cur = conn.cursor()  # создаю курсор
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))  # выполняю запрос на поиск пользователя
        return cur.fetchone()  # возвращаю результат запроса (первую найденную запись)
    except Exception as e:
        print("Ошибка при поиске пользователя:", e)  # печатаю ошибку, если она возникает
    finally:
        conn.close()  # закрываю соединение с базой данных

def initialize_db():
    # функция для инициализации базы данных и создания таблицы пользователей
    conn = create_connection()  # создаю соединение с базой данных
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    chat_id integer NOT NULL,
                                    name text NOT NULL,
                                    class_number text,
                                    class_letter text
                                ); """  # sql запрос для создания таблицы пользователей
    try:
        c = conn.cursor()  # создаю курсор
        c.execute(sql_create_users_table)  # выполняю запрос на создание таблицы
    except Exception as e:
        print("Ошибка при создании таблицы пользователей:", e)  # печатаю ошибку, если она возникает
    finally:
        conn.close()  # закрываю соединение с базой данных

initialize_db()  # вызываю функцию инициализации базы данных при запуске скрипта