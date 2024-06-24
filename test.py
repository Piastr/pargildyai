from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
import sqlite3

#from main import TARGET_CHAT_ID, MESSAGE_THREAD_ID, get_data

TARGET_CHAT_ID = '678484052'
MESSAGE_THREAD_ID = 'General'
piastr = 678484052

conn2 = sqlite3.connect('mydatabase.db', check_same_thread=False)
cursor2 = conn2.cursor()

# Функция для добавления данных в базу
def get_data():
    cursor2.execute("SELECT data FROM mytable")
    rows = cursor2.fetchall()
    return [row[0] for row in rows]

list_urls = ['https://www.ozon.ru/category/videokarty-15721/?deny_category_prediction=true&from_global=true&gpuseries=100429744&sorting=price&text=4090',
                 'https://www.ozon.ru/category/videokarty-15721/?deny_category_prediction=true&from_global=true&gpuseries=100482563&sorting=price&text=4070+ti',
                 'https://www.ozon.ru/category/videokarty-15721/?deny_category_prediction=true&from_global=true&gpuseries=100465304&sorting=price&text=4080']

#        4090    4070ti   4080
prices = [178000, 68000, 90000]


def get_videocard(bot, timesleep):
    #driver = webdriver.Chrome()
    #driver.maximize_window()
    bot = bot
    options = Options()
    options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    while True:
        print('OZON Работаю')
        products = []
        hide_list = get_data()
        for j in range(len(list_urls)):
            driver.get(list_urls[j])
            time.sleep(2)
            #Название + ссылка
            xx = driver.find_elements(By.PARTIAL_LINK_TEXT, "Видеокарта")
            #Цена
            xxx = driver.find_elements(By.CLASS_NAME, 'c3118-a0')
            for i in range(len(xxx)):
                product_name = xx[i].text
                href = xx[i].get_attribute('href')
                product_price = xxx[i].get_attribute('innerHTML')
                ruble_index = product_price.find('₽')
                product_price = product_price[ruble_index - 8:ruble_index]
                price = ''.join([i for i in product_price if i.isdigit()])
                products.append(product_name + "|" + price + "~" + href)

        for i in products:
            if i[:i.find('|')].find('4090') != -1 and int(i[i.find("|") + 1: i.find("~")]) < int(prices[0]):
                product = i[:i.find('|')]
                if product not in hide_list:
                    price = i[i.find("|") + 1: i.find("~")]
                    href = i[i.find("~") + 1:]
                    answer = product + f'\nЦена - {price}\n' + href
                    bot.send_message(TARGET_CHAT_ID, answer, message_thread_id=MESSAGE_THREAD_ID)

            if i[:i.find('|')].find('4070') != -1 and int(i[i.find("|") + 1: i.find("~")]) < int(prices[1]):
                product = i[:i.find('|')]
                if product not in hide_list:
                    price = i[i.find("|") + 1: i.find("~")]
                    href = i[i.find("~") + 1:]
                    answer = product + f'\nЦена - {price}\n' + href
                    bot.send_message(TARGET_CHAT_ID, answer, message_thread_id=MESSAGE_THREAD_ID)

            if i[:i.find('|')].find('4080') != -1 and int(i[i.find("|") + 1: i.find("~")]) < int(prices[2]):
                product = i[:i.find('|')]
                if product not in hide_list:
                    price = i[i.find("|") + 1: i.find("~")]
                    href = i[i.find("~") + 1:]
                    answer = product + f'\nЦена - {price}\n' + href
                    bot.send_message(TARGET_CHAT_ID, answer, message_thread_id=MESSAGE_THREAD_ID)

        time.sleep(timesleep)





if __name__ == '__main__':
    x = get_videocard(list_urls)
    print(len(x))
    for i in x:
        print(i[:i.find('|')])
        print(i[i.find("|") + 1 : i.find("~")])
        print(i[i.find("~") + 1:])