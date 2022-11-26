from bs4 import BeautifulSoup
import lxml
import psycopg2
import psql_config
from urllib.request import urlopen
from decimal import Decimal

class Product:
    def __init__(self, name, color, price, storage, category, origin):
        self.name = name
        self.color = color
        self.price = price
        self.storage = storage
        self.category = category
        self.origin = origin
class Laptop:
    def __init__(self, name, pro, storage, price, type, category, origin):
        self.name = name
        self.pro = pro
        self.type = type
        self.price = price
        self.storage = storage
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
            insert_script = "insert into product(pr_name, pr_price, pr_color, pr_category, pr_origin, pr_storage) values (%s, %s, %s, %s, %s, %s)"
            insert_value = (product.name, product.price, product.color, product.category, product.origin, product.storage)
            self.cur.execute(insert_script, insert_value)
            self.conn.commit()
        except Exception as error:
            print(error)


url = "https://www.technodom.kz/catalog/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

file = BeautifulSoup(html_bytes, "lxml")

all_names = file.find_all("p", class_="Typography ProductCardV__Title --loading Typography__Body Typography__Body_Bold")
all_prices = file.find_all("p", class_="Typography ProductCardV__Price ProductCardV__Price_WithOld Typography__Subtitle")

db = DataBase()
db.getConnection()

# for i in range(len(all_names)):
#     words = all_names[i].text.split()[1:]
#     s = 0;
#     for item in words:
#         if item.__contains__('GB'):
#             storage = item
#             s = words.index(item)
#     name = ' '.join(words[:s])
#     color = ' '.join(words[s+1:])
#     a = all_prices[i].text.replace('₸', '')
#     b = int(''.join(a.split()))
#     storage = storage.replace("GB", '')
#     ker = int(storage)
#     product = Product(name, color, Decimal(b), ker, "Smartphones", "Technodom")
#     db.insertRecord(product)

#laptop
for i in all_names:
    words = i.text.split()
    if words[0] == 'Ноутбук':
        s = 1
        type = "Laptop"
    else:
        s = 2
        type = "Gaming laptop"
    for item in words:
        if item.__contains__('ГБ'):
            e = words.index(item)-2
            pro = item
        elif item.__contains__('SSD'):
            storage = item
        else:
            continue
        name = words[s:e]
    print(' '.join(name), pro, storage)



