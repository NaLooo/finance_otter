from .ticker_index import Ticker_Index
from .ticker_stock import Ticker_Stock
from .models import GRU, LSTM, AR, ARMA
from .utils import *

__version__ = '0.1.0'
__author__ = "Ming Yu"

benchmark:Benchmark = Benchmark()
_CACHE = {}

def get_ticker(ticker: str):
    ticker = ticker.upper()
    if _CACHE.get(ticker):
        return _CACHE[ticker]
    result = None
    if ticker[0] == '^':
        result = Ticker_Index(ticker)
    else:
        result = Ticker_Stock(ticker)
    if not result:
        list = get_similar_ticker(ticker)
        if list is not None:
            print(f'Returning {list[0]} instead')
            return get_ticker(list[0])
    _CACHE[ticker] = result
    return result

def set_benchmark(ticker:str = '^GSPC'):
    benchmark.benchmark = get_ticker(ticker)




