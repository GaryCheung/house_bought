from bs4 import BeautifulSoup
import requests
from _datetime import date,datetime
import time
import pymysql
import re

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'house_bought',
    'charset':'gb2312'
}

present_date = datetime.now().date()
source = 'lianjia'

url = 'http://sh.lianjia.com/chengjiao/'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
#print(soup)

house_pages = soup.select('body > div.wrapper > div.main-box.clear > div > div.page-box.house-lst-page-box > a')
#print(pages)
for page in house_pages:
    if page.get_text().isdigit():
        pages = page.get_text()
    else:
        break
url_base = 'http://sh.lianjia.com/chengjiao/'
#for page in range(1,int(pages)+1):
page=60
more_page = 'd'+str(page)
url = url_base + more_page
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')
house_name = soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > h2 > a')
prices_per_area = soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(2) > div')
bought_date = soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div:nth-of-type(1) > div')
prices = soup.select('body > div.wrapper > div.main-box.clear > div > div.list-wrap > ul > li > div.info-panel > div > div.col-2.fr > div > div.fr > div')
for name,price_per_area,date,price in zip(house_name,prices_per_area,bought_date,prices):
    names = name.get_text()
    #print('name',type(name),name,'-----------------','\n')
    #print('prices',prices,'---------------','\n')
    name_layout_area = names.split(' ')
    name = name_layout_area[0].encode('UTF-8','ignore')
    layout = name_layout_area[1]
    area = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',name_layout_area[2])
    #print(name,'---------------',layout,'---------------------',area,'-------------------','\n')
    price_per_area = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',price_per_area.get_text())
    date = date.get_text()
    price = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',price.get_text())
    #print(type(price_per_area),price_per_area)
    #print('house----------',name,layout,area,price_per_area,date,price)
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            #sql = 'INSERT INTO house_bought (name, price, area, layout, source, price_per_area, bought_date) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            #cursor.execute(sql, (name, price, area, layout, source, price_per_area[0], date))
            sql = 'INSERT INTO house_bought (name) VALUES (%s)'
            cursor.execute(sql, (name))
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()

