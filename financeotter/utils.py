import requests
import re
import numpy as np

from pandas import DataFrame
from bs4 import BeautifulSoup
from .constant import *

def get_isin(ticker: str):
    pattern = re.compile(ticker.upper()+'\|(US.*?)\|')
    request = requests.get(URL_ISIN.format(ticker), headers = HEADERS)
    if request.status_code !=  200:
        print('Network Error: ', request.status_code)
        return
    result = re.search(pattern, request.text)
    return result.group(1)

def get_similar_ticker(ticker: str):
    soup = get_soup(URL_SIMILAR.format(ticker))
    if not soup:
        return
    list = []
    for e in soup.find_all(name = TR):
        s = e.find_all(name = TD)
        for x in s:
            list.append(x.string)
            break
    if len(list) > 0:
        print('Similar Ticker: ', list)
    else:
        print('No Similar Ticker Found')

def get_key_statistics(ticker: str):
    soup = get_soup(URL_INFO.format(ticker, INFO_STATISTICS))
    if not soup:
        return
    blocks = soup.find_all(name = H2)
    return get_valuation_measures(blocks[0].parent), get_trading_information(blocks[1].parent), get_financial_highlights(blocks[2].parent)

def get_key_executives(ticker: str):
    soup = get_soup(URL_INFO.format(ticker, INFO_PROFILE))
    if not soup:
        return
    rows = soup.find(name = 'table').find_all(name = 'tr')
    cols = ['Name', 'Title', 'Pay', 'Exercised', 'Year Born']
    data = []

    for row in rows:
        cells = row.find_all(name = 'td')
        for e in cells:
            if e.span.string:
                data.append(e.span.string.strip())
            else:
                data.append('N/A')
    
    arr = np.array(data)
    arr = np.resize(arr, (len(data)//5, 5))
    return DataFrame(arr, columns = cols)

def get_income_statement(ticker: str):
    return get_financials_table(ticker, INFO_INCOME_STATEMENT)

def get_balance_sheet(ticker: str):
    return get_financials_table(ticker, INFO_BALANCE_SHEET)

def get_cash_flow(ticker: str):
    return get_financials_table(ticker, INFO_CASH_FLOW)

def get_financials_table(ticker, info):
    soup = get_soup(URL_INFO.format(ticker, info))
    if not soup:
        return
    cols = []
    data = []
    for e in soup.find(name = 'div', class_ = 'D(tbhg)').find_all(name = 'span'):
        cols.append(e.string.strip())

    for row in soup.find(name = 'div', class_ = 'D(tbrg)').children:
        for cell in row.find(name = 'div').children:
            span = cell.find(name = 'span')
            if span:
                data.append(span.string.strip())
            else:
                data.append('-')
    
    arr = np.array(data)
    arr = np.resize(arr, (len(data)//len(cols), len(cols)))
    return DataFrame(arr, columns = cols).set_index(['Breakdown'])

def get_soup(url: str):
    request = requests.get(url, headers = HEADERS)
    if request.status_code != 200:
        print('Fetch failed, code: ', request.status_code)
        return None
    return BeautifulSoup(request.text, 'lxml')

def get_valuation_measures(soup):
    time_tile = soup.find_all(name = TH)
    content = soup.find(name = TBODY).find_all(name = TR)
    cols = ['Current']
    headers = []
    data = []

    for e in time_tile:
        if e.span and e.span.string:
            cols.append(e.span.string.strip())

    for e in content:
        cells = e.find_all(name = TD)
        headers.append(cells[0].span.string.strip())
        for i in range(1, len(cells)):
            if cells[i].span  and cells[i].span.string:
                data.append(cells[i].span.string.strip())
            else:
                data.append(cells[i].string.strip())

    l1 = len(headers)
    l2 = len(data)
    arr = np.array(data)
    arr = np.resize(arr, (l1, l2//l1))
    return DataFrame(arr, index=headers, columns=cols)

def get_trading_information(soup):
    return TradingInformation(get_table_dict(soup))

def get_financial_highlights(soup):
    return FinancialHighlights(get_table_dict(soup))

def get_table_dict(soup):
    blocks = soup.find_all(name = H3)
    table_dict = {}

    for block in blocks:
        title = block.span.string.strip()
        index = []
        data = []
        for e in block.next_sibling.find_all(name = TR):
            children = e.find_all(name = TD)
            index.append(children[0].span.string.strip())
            if children[1].span:
                data.append(children[1].span.string.strip())
            else:
                data.append(children[1].string.strip())
        table_dict[title] = DataFrame(data, index=index, columns=['data'])
    return table_dict

class TradingInformation():
    def __init__(self, table_dict):
        self.stock_price_history: DataFrame = table_dict['Stock Price History']
        self.share_statistics: DataFrame = table_dict['Share Statistics']
        self.dividends_and_splits: DataFrame = table_dict['Dividends & Splits']

    def __str__(self) -> str:
        return 'Stock Price History\n' \
            + str(self.stock_price_history) \
            + '\n\n' \
            + 'Share Statistics\n' \
            + str(self.share_statistics) \
            + '\n\n' \
            + 'Dividends & Splits\n' \
            + str(self.dividends_and_splits)

class FinancialHighlights():
    def __init__(self, table_dict):
        self.fiscal_year: DataFrame = table_dict['Fiscal Year']
        self.profitability: DataFrame = table_dict['Profitability']
        self.management_effectiveness: DataFrame = table_dict['Management Effectiveness']
        self.income_statement: DataFrame = table_dict['Income Statement']
        self.balance_sheet: DataFrame = table_dict['Balance Sheet']
        self.cash_flow_statement: DataFrame = table_dict['Cash Flow Statement']
        pass

    def __str__(self) -> str:
        return 'Fiscal Year\n' \
            + str(self.fiscal_year) \
            + '\n\n' \
            + 'Profitability\n' \
            + str(self.profitability) \
            + '\n\n' \
            + 'Management Effectiveness\n' \
            + str(self.management_effectiveness) \
            + '\n\n' \
            + 'Income Statement\n' \
            + str(self.income_statement) \
            + '\n\n' \
            + 'Balance Sheet\n' \
            + str(self.balance_sheet) \
            + '\n\n' \
            + 'Cash Flow Statement\n' \
            + str(self.cash_flow_statement)

