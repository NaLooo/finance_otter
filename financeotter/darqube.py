import requests as re
import pandas as pd

from io import StringIO
from datetime import datetime, timedelta
from time import mktime

URL_HISTORY = 'https://api.darqube.com/data-api/market_data/historical/{}?token={}&start_date={}&end_date={}&interval=1d'


def cursor(token):
    return Cursor(token)

class Cursor():
    def __init__(self, token):
        self.token = token
    
    def history(self, ticker, period='max', start=None, end=None):
        start_time, end_time = self._process_date(period, start, end)
        json = re.get(URL_HISTORY.format(ticker.upper(), self.token, start_time, end_time)).text
        df = pd.read_json(StringIO(json))
        df['date'] = pd.DataFrame([datetime.fromtimestamp(t).date() for t in df['time']])
        df = df.set_index('date').astype('float32')

        return df.dropna().drop('time', axis=1)
    
    def _process_date(self, period, start, end):
        span = None
        start_date = None
        end_date = datetime.now().date()
        if start is not None:
            start_date = datetime.strptime(start, format='%Y%m%d')
            if end is not None:
                end_date = datetime.strptime(end, format='%Y%m%d')
        else:
            match period:
                case '1d':
                    span = timedelta(days=1)
                case '5d':
                    span = timedelta(days=5)
                case '1m':
                    span = timedelta(days=30)
                case '3m':
                    span = timedelta(days=90)
                case '6m':
                    span = timedelta(days=180)
                case '1y':
                    span = timedelta(days=365)
                case '5y':
                    span = timedelta(days=365*5)
                case 'ytd':
                    span = end_date - datetime.now().date().replace(month=1, day=1)
                case 'max':
                    span = end_date - datetime.fromtimestamp(0)
                case _:
                    span = end_date - datetime.fromtimestamp(0)
                    print('illegal period, max historical data is returned instead')
            start_date = end_date - span
        end_date += timedelta(days=1)
        print(end_date)
        return int(mktime(start_date.timetuple())), int(mktime(end_date.timetuple()))
