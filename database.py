import sqlite3

def create_connection():
    """ Создать новое соединение с SQLite базой данных """
    try:
        conn = sqlite3.connect("school_bot.db")
        return conn
    except Exception as e:
        print(e)

def add_user(user):
    """ Добавить нового пользователя в базу данных """
    conn = create_connection()
    try:
        sql = ''' INSERT INTO users(chat_id, name, class_number, class_letter)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_user_by_chat_id(chat_id):
    """ Получить пользователя по его chat_id """
    conn = create_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,))
        return cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        conn.close()

# Инициализация базы данных и создание таблицы
def initialize_db():
    conn = create_connection()
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    chat_id integer NOT NULL,
                                    name text NOT NULL,
                                    class_number text,
                                    class_letter text
                                ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_users_table)
    except Exception as e:
        print(e)
    finally:
        conn.close()

# Вызов функции инициализации при запуске
initialize_db()
