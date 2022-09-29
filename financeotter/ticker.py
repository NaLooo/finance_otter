from tkinter.messagebox import NO
import pandas as pd
import requests

from io import StringIO
from datetime import datetime, timedelta

from .utils import get_similar_ticker
from .constant import *

class Ticker():

    def __new__(cls, ticker:str):
        instance = super().__new__(cls)
        instance.ticker = ticker.upper()
        instance.start_time_stamp = -1356980400
        instance.end_time_stamp = int(datetime.timestamp(datetime.now()))
        instance.request_historical_data = requests.get(URL_QUERY.format(instance.ticker, instance.start_time_stamp, instance.end_time_stamp), headers = HEADERS)
        if(instance.request_historical_data.status_code != 200):
            print('Invalid Ticker: ' + ticker)
            get_similar_ticker(ticker)
            return None
        else:
            return instance

    def __init__(self, ticker:str) -> None:
        df = pd.read_csv(StringIO(self.request_historical_data.text))
        df['Date'] = pd.to_datetime(df['Date'])
        self._historical_data = df.set_index('Date')

    # get historical data from start to end, time format: YYYY-MM-DD
    def get_historical_data(self, 
                            period = 'max',
                            start = None, 
                            end = None):
        span = None
        start_date  = None
        end_date = datetime.now().date()
        if start is not None:
            start_date = start
            if end is not None:
                end_date = end
        else:
            match period:
                case '1d':
                    return self._historical_data.iloc[-1:]
                case '5d':
                    return self._historical_data.iloc[-5:]
                case '3m':
                    span = timedelta(days = 90)
                case '6m':
                    span = timedelta(days = 180)
                case '1y':
                    span = timedelta(days = 365)
                case '5y':
                    span = timedelta(days = 365*5)
                case 'ytd':
                    span = end_date - datetime.now().date().replace(month = 1, day = 1)
                case 'max':
                    return self._historical_data
            start_date = end_date - span

        return self._historical_data.loc[str(start_date):str(end_date)]