import requests
import pandas as pd

from statsmodels.api import OLS, add_constant
from io import StringIO, BytesIO
from zipfile import ZipFile
from .constant import *

_CACHE = {}
# Mkt-RF, SMB, HML, RMW, CMA, RF

def OLS_ff3_daily(ticker, period='1y', drop=[]):
    return _OLS(download_ff3_daily(), ticker, period, drop)

def OLS_ff3_monthly(ticker, period='1y', drop=[]):
    return _OLS(download_ff3_monthly(), ticker, period, drop, False)

def OLS_ff5_daily(ticker, period='1y', drop=[]):
    return _OLS(download_ff5_daily(), ticker, period, drop)

def OLS_ff5_monthly(ticker, period='1y', drop=[]):
    return _OLS(download_ff5_monthly(), ticker, period, drop, False)

def _OLS(ff, ticker, period, drop, daily=True):
    r = ticker.history(period)['Adj Close']
    r = r/r.shift() - 1

    if not daily:
        r = r.groupby(pd.Grouper(freq='M')).sum()

    df = pd.merge(r[1:], ff.drop(drop, axis=1), left_index=True, right_index=True)
    y = df['Adj Close'] - df['RF']
    x = add_constant(df.drop(['Adj Close', 'RF'], axis=1))

    return OLS(y.copy(), x.copy()).fit()

def download_ff3_daily():
    return _download_data('ff3d', URL_FF3_DAILY)

def download_ff3_monthly():
    return _download_data('ff3m', URL_FF3_MONTHLY, False)

def download_ff5_daily():
    return _download_data('ff5d', URL_FF5_DAILY)

def download_ff5_monthly():
    return _download_data('ff5m', URL_FF5_MONTHLY, False)

def _download_data(token, url, daily=True):
    if token in _CACHE.keys():
        return _CACHE[token].copy()
    
    end = -2
    format = '%Y%m%d'
    r = requests.get(url)
    zip = ZipFile(BytesIO(r.content))
    result = zip.open(zip.namelist()[0]).read().decode().splitlines()
    
    if not daily:
        format = '%Y%m'
        idx = 0
        for e in result:
            if 'Annual Factors' in e:
                end = idx
                break
            idx += 1

    df = pd.read_csv(StringIO('\r\n'.join(result[3:end])))
    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format=format)
    if not daily:
        df['Date'] = df['Date'] + pd.DateOffset(months=1, days=-1)
    df.set_index('Date', inplace=True)

    _CACHE[token] = df
    return _CACHE[token].copy()
