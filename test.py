from time import process_time_ns
import financeotter as otter
import requests
import re
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
from enum import Enum
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
from financeotter.utils import *

# date_string = '2010-01-02'
# delta = timedelta(days = 50)
# dt = datetime.fromisoformat(date_string) + delta
# print(dt)
# print(str(dt))

# ticker = fo.Ticker('AAPL')
# if(ticker):
#     ticker.display_historical_data()
# else:
#     print('none')

# def Encode(content):
#     return bytes(str(content), encoding = 'utf-8')

# headers = {
#     'User-Agent' : User_Agent
# }
# pattern = re.compile('<ol class="grid_view">(.*)</ol>', re.S)
# nameOnly = re.compile('<span class="title">(.*?)</span>')
# r = requests.get('https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL', headers = headers)
# soup = bf(r.text, 'lxml')
# item = soup.find_all(name = 'span')
# print(item)

# df = pd.read_csv(StringIO(r.text))
# print(df)

# content = re.search(pattern, r.content.decode('utf-8'))
# titles = re.findall(nameOnly, r.text)

# file = open('AAPL.txt', 'wb')
# file.write(Encode(soup.prettify()))
# file.close()




# pattern = re.compile('<h3.*?</table>', re.S)

# file = open('AAPL.txt', 'rb')
# content = file.read().decode('utf-8')
# soup = BeautifulSoup(content, 'lxml')
# file.close()

# result = re.findall(pattern, content)
# soup = BeautifulSoup(result[0], 'lxml')

# s = soup.find_all(name = 'td')

# title = soup.find_all(name = 'th')
# for e in title:
#     if(e.span and e.span.string):
#         print(e.span.string.strip())

# headers = []
# data = []

# for e in s:
#     if(e.span and e.span.string):
#         headers.append(e.span.string.strip())
#     elif e.string:
#         data.append(e.string.strip())

# print(headers)
# print(data)

# l1 = len(headers)
# l2 = len(data)

# print(l1, l2)

# arr = np.array(data)
# arr = np.resize(arr,(l1, l2//l1))
# print(arr)

# df = pd.DataFrame(arr, index = headers)
# print(df)

# col = ['a','b','c','d','e','f']
# df.columns = col
# print(df)


aapl = otter.get_ticker('aapl')
print(aapl.get_historical_data())


# for info like isin
# https://markets.businessinsider.com/ajax/SearchController_Suggest?max_results=25&query=amzn


