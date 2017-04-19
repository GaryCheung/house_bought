from bs4 import BeautifulSoup
import requests
from datetime import date,datetime
import time
import pymysql
import re

config = {
    'host':'127.0.0.1',
    'port':8889,
    'user':'root',
    'password':'root',
    'db':'house_bought',
    'charset':'utf8',
    'unix_socket':'/Applications/MAMP/tmp/mysql/mysql.sock'
}

present_date = datetime.now().date()

def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM house_bought where import_date = '%s'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_bouhgt_house(config,source):
    url = 'http://sh.lianjia.com/chengjiao/'
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    #print(soup)
    house_pages = soup.select('div.c-pagination > a')
    #print(pages)
    for page in house_pages:
        if page.get_text().isdigit():
            pages = page.get_text()
            print(pages)
        else:
            break
    url_base = 'http://sh.lianjia.com/chengjiao/'
    for page in range(1,int(pages)+1):
        print('present page is------------------',page,'------------------','\n')
        more_page = 'd'+str(page)
        url = url_base + more_page
        print(url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        house_name = soup.select('span.cj-text')
        #print(house_name)
        prices_per_area = soup.select('div.info-row > div.info-col.price-item.minor')
        #print(prices_per_area)
        bought_date = soup.select('div.info-col.deal-item.main.strong-num')
        #print(bought_date)
        prices = soup.select('div.info-col.price-item.main > span.strong-num')
        print(prices)
        area = soup.select('div.info-row > a')
        #print(area)
        for name,price_per_area,date,price,areas in zip(house_name,prices_per_area,bought_date,prices,area):
            names = name.get_text()
            print(names)
            print(type(names))
            #flag = '西凌新邨'
            #print(flag)
            #if names == flag:
             #   print('FIND ONE!!')
              #  continue
            #print('names',names,'-----------------','\n')
            #print('prices',prices,'---------------','\n')
            #name_layout_area = names.split(' ')
            #print(name_layout_area)
            #name = name_layout_area[0].encode('UTF-8','ignore')
            areas = areas.get_text()
            #print(areas)
            #print(type(areas))
            layout = re.findall(r'(\s[0-9]+\w+[0-9]+\w+)',areas)
            #print(type(layout))
            layout = re.findall(r'([0-9]+\w+[0-9]+\w+)',layout[0])
            #layout = re.findall(r'([0-9]+\w+[0-9]+\w+)',layout)
            print(layout,'@@@@@')
            #print(areas)
            area = re.findall(r'([0-9]+\.+[0-9]+)\w*',areas)
            print(area)
            #print(names,'---------------',layout[1],'---------------------',area[1],'-------------------','\n')
            price_per_area = re.findall(r'([0-9]+\.*[0-9]+)\w*',price_per_area.get_text())
            #print(price_per_area)
            date = date.get_text()
            price = re.findall(r'(\w*[0-9]+\.*[0-9]*)\w*',price.get_text())
            print(price)
            #print(type(price_per_area),price_per_area)
            print('house----------',names,'---',price,'----',area,'---',layout,'---',price_per_area,'---',date,'---')
            connection = pymysql.connect(**config)
            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO house_bought (name, price, area, layout, source, price_per_area, bought_date, import_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    cursor.execute(sql, (names, price, area, layout, source, price_per_area, date, present_date))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            finally:
                connection.close()
    time.sleep(1)

source = 'lianjia'
print('execute time:-------------------',present_date)
delete_today_data(config)
get_bouhgt_house(config,source)
