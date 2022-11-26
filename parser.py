import requests
import csv
import time
import psycopg2
import psql_config
from urllib.request import urlopen
from bs4 import BeautifulSoup
from decimal import Decimal

from lxml import html

class Product:
    def __init__(self, name , price, category, origin):
        self.name = name
        self.price = price
        self.category = category
        self.origin = origin

class DataBase:
    conn = None
    cur = None

    def getConnection(self):
        try:
            self.conn = psycopg2.connect(
                host=psql_config.hostname,
                dbname=psql_config.database,
                user=psql_config.username,
                password=psql_config.pswd,
                port=psql_config.port)
            self.cur = self.conn.cursor()
        except Exception as error:
            print(error)


    def insertRecord(self, product):
        try:
            # self.getConnection()
            insert_script = "insert into products(pr_name, pr_price, pr_category, pr_origin) values (%s, %s, %s, %s)"
            insert_value = (product.name, product.price, product.category, product.origin)
            self.cur.execute(f"select * from products where pr_name like %s", (product.name,))

            if (len(self.cur.fetchall()) > 0):
                pass
            else:
                self.cur.execute(insert_script, insert_value)
                self.conn.commit()
        except Exception as error:
            print(error)
            # self.cur.close()
            # self.conn.close()


# HEADERS = Headers(
#         browser="chrome",
#         os="win",
#         headers=True
#     ).generate()
URL = 'https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony'
DOMAIN = 'https://kz.e-katalog.com'
ALL_DATA = dict()
QUEUE_URL = set()


# def add_to_csv_from_file(product_dict):
#
db = DataBase()
db.getConnection()

def get_data(product_link):
    product = dict()
    page = urlopen(product_link)
    html_bytes = page.read()
    file = BeautifulSoup(html_bytes, "lxml")
    all_names = file.find_all("p",
                              class_="Typography ProductCardV__Title --loading Typography__Body Typography__Body_Bold")
    all_prices = file.find_all("p",
                               class_="Typography ProductCardV__Price ProductCardV__Price_WithOld Typography__Subtitle")

    for i in range(len(all_names)):
        try:
            words = all_names[i].text.split()[1:]
            s = 0;
            for item in words:
                if item.__contains__('GB'):
                    s = words.index(item)
            name = ' '.join(words[:s])
            a = all_prices[i].text.replace('₸', '')
            b = int(''.join(a.split()))
            product = Product(name, Decimal(b), "Smartphones", "Technodom")
            db.insertRecord(product)
        except:
            pass
    # return product

def get_gadgets(product_link):
    page = urlopen(product_link)
    html_bytes = page.read()
    file = BeautifulSoup(html_bytes, "lxml")
    all_names = file.find_all("p",
                              class_="Typography ProductCardV__Title --loading Typography__Body Typography__Body_Bold")
    all_prices = file.find_all("p",
                               class_="Typography ProductCardV__Price ProductCardV__Price_WithOld Typography__Subtitle")

    for i in range(len(all_names)):
        words = all_names[i].text.split()[2:]
        name = ' '.join(words)
        print(name)
        try:
            a = all_prices[i].text.replace('₸', '')
            b = int(''.join(a.split()))
            product = Product(name, Decimal(b), "Gadgets", "Technodom")
            db.insertRecord(product)
        except:
            pass


def get_links(page_url):
    request = requests.get(page_url)
    tree = html.fromstring(request.content)
    pages_count = tree.xpath('//div[@class="Paginator__List"]//p[last()]/text()')
    print('Pages: ', pages_count)

    get_data(URL)
    for url in range(2, len(pages_count)):
        full_url = f"{URL}?page={url}"
        print(full_url)
        get_data(full_url)
    #     pagination_pages.add(full_url)
    #
    # while len(pagination_pages) != 0:
    #     current_url = pagination_pages.pop()
    #     get_data(current_url)


def main():

    get_links(URL)

    # while len(QUEUE_URL) != 0:
    #     current_url = QUEUE_URL.pop()
    #     get_data(current_url)


if __name__ == "__main__":
    main()