# Finance Otter
Download data from [Yahoo!Ⓡ finance](https://finance.yahoo.com) or [Darqube](https://darqube.com/) open API.

Analysis data using FamaFrench, ARMA, LSTM models.

## Quick Start
``` python
import financeotter as fo

aapl = fo.get_ticker('aapl')
history = aapl.history(period='max')

aapl.summary
aapl.income_statement
aapl.balance_sheet
aapl.cash_flow
```

## Module famafrench
```python
import financeotter as fo
import financeotter.famafrench as ff

aapl = fo.get_ticker('aapl')
result = ff.OLS_ff3_daily(aapl, period='1y')
# also OLS_ff3_monthly OLS_ff5_daily OLS_ff5_monthly
print(result.summary())
```

## Module models
Other built in regression models
```python
from financeotter.models import ARMA, LSTM
import financeotter as fo

aapl = fo.get_ticker('aapl')
lstm = LSTM(aapl)
lstm.train()
lstm.predict()

arma = ARMA(aapl)
arma.fit()
arma.predict()
```

## Module darqube
Download Data using [Darqube](https://darqube.com/) API
``` python
import financeotter.darqube as dq

token = 'your token'
cursor = dq.cursor(token)
history = cursor.history('aapl', 'max')
```

## Requirements

-   Python >= 3.0
-   requests >= 2.28.1
-   beautifulsoup4 >= 4.11.1
-   statsmodels >= 0.13.5
-   pandas >= 1.4.4
-   sklearn >= 1.2.1
-   numpy >= 1.23.2