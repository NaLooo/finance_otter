URL_BASE = 'https://finance.yahoo.com/quote/{}'
URL_SIMILAR = 'https://finance.yahoo.com/lookup?s={}'
URL_INFO = 'https://finance.yahoo.com/quote/{}/{}'
URL_QUERY = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true'
URL_ISIN = 'https://markets.businessinsider.com/ajax/SearchController_Suggest?max_results=25&query={}'

URL_FF3_MONTHLY = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'
URL_FF3_DAILY = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip'
URL_FF5_MONTHLY = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip'
URL_FF5_DAILY = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip'


INFO_STATISTICS = 'key-statistics'
INFO_PROFILE = 'profile'
INFO_INCOME_STATEMENT = 'financials'
INFO_BALANCE_SHEET = 'balance-sheet'
INFO_CASH_FLOW = 'cash-flow'

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

TR = 'tr'
TD = 'td'
TH = 'th'
H2 = 'h2'
H3 = 'h3'
DIV = 'div'
TABLE = 'table'
TBODY = 'tbody'

BETA = 'Beta (5Y Monthly)'
PE = 'PE Ratio (TTM)'
EPS = 'EPS (TTM)'
CAP = 'Market Cap'

DATE_FORMAT = '%Y-%m-%d'
