from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pickle
import re
import sqlite3
#import main

piastr = 678484052
TARGET_CHAT_ID = '678484052'
MESSAGE_THREAD_ID = 'General'
prices4090MM = ['280000', '55']


"""options = Options()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
driver.maximize_window()"""


def get_products_maxmarket(bot, timesleep):
    conn3 = sqlite3.connect('mydatabase.db', check_same_thread=False)
    cursor3 = conn3.cursor()

    # Функция для добавления данных в базу
    def get_data():
        cursor3.execute("SELECT data FROM mytable")
        rows = cursor3.fetchall()
        return [row[0] for row in rows]

    bot = bot
    options = Options()
    #options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    #driver = webdriver.Chrome()
    #driver.maximize_window()

    driver.get('https://megamarket.ru/catalog/videokarty/set-rtx-4090/page-1/#?related_search=4090&filters=%7B"4CB2C27EAAFC4EB39378C4B7487E6C9E"%3A%5B"1"%5D%7D')
    time.sleep(5)
    """cookies = pickle.load(open("cookies", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)"""

    time.sleep(5)
    driver.refresh()
    time.sleep(5)

    while True:
        print('MM работаю')
        products = []
        hide_list = get_data()
        for i in range(3):
            try:
                driver.get(f'https://megamarket.ru/catalog/videokarty/set-rtx-4090/page-{i+1}/#?related_search=4090&filters=%7B"4CB2C27EAAFC4EB39378C4B7487E6C9E"%3A%5B"1"%5D%7D')
                time.sleep(2)
            except:
                break

            x = driver.find_elements(By.CLASS_NAME, 'item-block')
            xxx = driver.find_elements(By.CLASS_NAME, 'ddl_product_link')
            result = [xxx[i] for i in range(len(xxx)) if i % 2 == 1]
            for i in range(len(result)):
                element = []
                element.append(result[i].text)
                try:
                    rub = x[i].find_element(By.CLASS_NAME, 'item-price').find_element(By.CSS_SELECTOR, 'span').get_attribute('innerHTML')[:-7]
                    rub = re.sub(r'\W', '', rub)
                    element.append(int(rub))
                    sber_spasibo = x[i].find_element(By.CLASS_NAME, 'item-bonus').find_element(By.CLASS_NAME, 'bonus-amount').get_attribute('innerHTML')
                    sber_spasibo = re.sub(r'\W', '', sber_spasibo)
                    element.append(int(sber_spasibo))
                    percent = (int(sber_spasibo) / int(rub)) * 100
                    element.append("{:.0f}".format(percent))
                    product_id = x[i].find_element(By.CSS_SELECTOR, 'a').get_attribute('data-product-id')
                    element.append(product_id)
                    element.append(result[i].get_attribute('href'))
                    products.append(element)
                except:
                    continue
        try:
            for i in range(len(products)):
                if (products[i][1] < int(prices4090MM[0])) and (int(products[i][3]) > int(prices4090MM[1])):
                    if products[i][4] not in hide_list:
                        print(products[i])
                        name = products[i][0]
                        price = products[i][1]
                        bonus = products[i][2]
                        percent = products[i][3]
                        product_id = products[i][4]
                        href = products[i][5]
                        answer =  f'{name}\nЦена: {price}\nБонусы: {bonus}({percent}%)\n{href}\nid: {product_id}'
                        bot.send_message(TARGET_CHAT_ID, answer, message_thread_id=MESSAGE_THREAD_ID)
        except:
            pass
        time.sleep(timesleep)


if __name__ == '__main__':
    products = get_products_maxmarket('https://megamarket.ru/shop/gadzhet-stor/#?page=1')
    print(len(products))
    for i in products:
        if int(i[1]) < 280000 and int(i[3]) > 36:
            print(i)


