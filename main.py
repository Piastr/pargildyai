import telebot

import apple
import test
import time
import schedule
import threading
import parsing
import json
import sqlite3
import datetime

bot = telebot.TeleBot('token')

piastr = 678484052
TARGET_CHAT_ID = '678484052'
MESSAGE_THREAD_ID = 'General'



products_maxmarket = []
hide_list = []


# Подключение к базе данных
conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS mytable 
                (id INTEGER PRIMARY KEY, data TEXT, timestamp DATETIME)''')


# Функция для добавления данных в базу
def add_data(data):
    timestamp = datetime.datetime.now()
    cursor.execute("INSERT INTO mytable (data, timestamp) VALUES (?, ?)", (data, timestamp))
    conn.commit()

# Функция для удаления старых данных
def delete_old_data():
    twelve_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=12)
    cursor.execute("DELETE FROM mytable WHERE timestamp <= ?", (twelve_hours_ago,))
    conn.commit()

# Функция для получения строк из базы
def get_data():
    cursor.execute("SELECT data FROM mytable")
    rows = cursor.fetchall()
    return [row[0] for row in rows]


@bot.message_handler(commands=['upd_price4090'])
def upd_price(message):
    try:
        p = message.text[15:]
        test.prices[0] = int(p)
        print(p)
        bot.send_message(TARGET_CHAT_ID, f'ОЗОН Новый потолок цены для 4090- {p}', message_thread_id=MESSAGE_THREAD_ID)
    except:
        bot.send_message(TARGET_CHAT_ID, f'Некорректно введена цена', message_thread_id=MESSAGE_THREAD_ID)


@bot.message_handler(commands=['upd_price4070ti'])
def upd_price(message):
    try:
        p = message.text[17:]
        test.prices[1] = int(p)
        print(p)
        bot.send_message(TARGET_CHAT_ID, f'ОЗОН Новый потолок цены для 4070ti- {p}', message_thread_id=MESSAGE_THREAD_ID)
    except:
        bot.send_message(TARGET_CHAT_ID, f'Некорректно введена цена', message_thread_id=MESSAGE_THREAD_ID)


@bot.message_handler(commands=['upd_price4080'])
def upd_price(message):
    try:
        p = message.text[15:]
        test.prices[2] = int(p)
        print(p)
        bot.send_message(TARGET_CHAT_ID, f'ОЗОН Новый потолок цены для 4080- {p}', message_thread_id=MESSAGE_THREAD_ID)
    except:
        bot.send_message(TARGET_CHAT_ID, f'Некорректно введена цена', message_thread_id=MESSAGE_THREAD_ID)


@bot.message_handler(commands=['upd_price_MM_4090'])
def upd_price(message):
    p = message.text[19:]
    if len(p) > 8:
        p = p.split()
        parsing.prices4090MM = p
        bot.send_message(TARGET_CHAT_ID, f'ММ_4090 Новый потолок цены - {p[0]}\nНовый минимум процентов - {p[1]}', message_thread_id=MESSAGE_THREAD_ID)
    else:
        bot.send_message(TARGET_CHAT_ID, f'Некорректно введена цена', message_thread_id=MESSAGE_THREAD_ID)
@bot.message_handler(commands=['hide'])
def hide(message):
    global hide_list
    p = message.text[6:]
    print(p)
    add_data(p)
    hide_list = get_data()
    bot.send_message(TARGET_CHAT_ID, 'Скрыто', message_thread_id=MESSAGE_THREAD_ID)


def bot_start():
    print('Я включился')
    bot.infinity_polling()

def mainloop():
    global hide_list
    delete_old_data()
    hide_list = get_data()
    #test.get_videocard(bot, 30)
    #parsing.get_products_maxmarket(bot, 30)
    schedule.every(1).hours.do(delete_old_data)
    while 1:

        schedule.run_pending()
        time.sleep(1)


bot_start = threading.Thread(target=bot_start)
schedule_loop = threading.Thread(target=mainloop)
ozon_start = threading.Thread(target=test.get_videocard, args=(bot, 30,))
mm_start = threading.Thread(target=parsing.get_products_maxmarket, args=(bot, 30,))
apple_start = threading.Thread(target=apple.get_products_apple, args=(bot, 4000,
                       'https://megamarket.ru/catalog/smartfony-apple/page-~/#?filters=%7B"4CB2C27EAAFC4EB39378C4B7487E6C9E"%3A%5B"1"%5D%7D', 0,))

if __name__ == '__main__':
    time.sleep(5)
    bot_start.start()
    ozon_start.start()
    mm_start.start()
    apple_start.start()
    time.sleep(2)
    schedule_loop.start()

