from .version import version
from .ticker_index import Ticker_Index
from .ticker_stock import Ticker_Stock

__version__ = version
__author__ = "Ming Yu"

def get_ticker(ticker: str):
    if ticker[0] == '^':
        return Ticker_Index(ticker)
    else:
        return Ticker_Stock(ticker)
