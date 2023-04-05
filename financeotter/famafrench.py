import requests, zipfile
import pandas as pd

from io import StringIO, BytesIO
from bs4 import BeautifulSoup


URL = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html'

r = requests.get(URL)
soup = BeautifulSoup(r.text, "lxml")
table = soup.find_all('table')[3].find_all('tr')

ff3 = table[2].find_all('td')
ff5 = table[3].find_all('td')

ff3_latest_month = [float(i) for i in ff3[1].div.font.text.split()]
ff3_last_3_month = [float(i) for i in ff3[2].div.font.text.split()]
ff3_last_12_month = [float(i) for i in ff3[3].div.font.text.split()]

ff5_latest_month = [float(i) for i in ff5[1].div.font.text.split()]
ff5_last_3_month = [float(i) for i in ff5[2].div.font.text.split()]
ff5_last_12_month = [float(i) for i in ff5[3].div.font.text.split()]


# return rm-rf, smb, hml
def get_ff3_latest_month():
    return ff3_latest_month

def get_ff3_last_3_month():
    return ff3_last_3_month

def get_ff3_last_12_month():
    return ff3_last_12_month

# return rm-rf, smb, hml, rmw, cma
def get_ff5_latest_month():
    return ff5_latest_month

def get_ff5_last_3_month():
    return ff5_last_3_month

def get_ff5_last_12_month():
    return ff5_last_12_month

