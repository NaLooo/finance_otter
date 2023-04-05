import matplotlib.pyplot as plt
import numpy as np

from tensorflow.python.keras import Sequential, layers
from sklearn import  model_selection
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from abc import ABC, abstractmethod


def add_lags(data, features, lags=5):
    df = data[features].copy()
    cols = []
    
    for f in features:
        for i in range(1, lags+1):
            col = f'{f}_lag_{i}'
            df[col] = df[f].shift(i)
            cols.append(col)

    df.dropna(inplace=True)
    return df, cols


def add_features(data, tag='Adj Close', window=50):
    df = data[[tag]].copy()

    df.dropna(inplace=True)
    df['log_r'] = np.log(df / df.shift())
    df['sma'] = df[tag].rolling(window).mean()
    df['min'] = df[tag].rolling(window).min()
    df['max'] = df[tag].rolling(window).max()
    df['mom'] = df['log_r'].rolling(window).mean()
    df['vol'] = df['log_r'].rolling(window).std()
    df.dropna(inplace=True)
    df['d'] = np.where(df['log_r'] > 0, 1, 0)
    features = [tag, 'log_r', 'd', 'sma', 'min', 'max', 'mom', 'vol']
    
    return df, features

class ARMA():
    def __init__(self, ticker):
        self.ticker = ticker

    def fit(self, period='1y', split=0.2):
        self.base_model = MLPClassifier(
            hidden_layer_sizes=[512],
            random_state=100,
            max_iter=1000,
            early_stopping=True,
            validation_fraction=0.2,
            shuffle=False
        )
        self.train(self.base_model, period, split)

    def fit_bagging(self, n=50, period='1y', split=0.2):
        self.base_model = MLPClassifier(
            hidden_layer_sizes=[512],
            random_state=100,
            max_iter=1000,
            early_stopping=True,
            validation_fraction=0.2,
            shuffle=False
        )
        self.bag_model = BaggingClassifier(
            estimator=self.base_model,
            n_estimators=n,
            max_samples=0.25,
            max_features=0.5,
            bootstrap=False,
            bootstrap_features=True,
            n_jobs=8,
            random_state=100
        )
        self.train(self.bag_model, period, split)

    def train(self, model, period, split):
        df, features = add_features(self.ticker.history(period))
        df, cols = add_lags(df, features)
        df[cols] = (df[cols] - df[cols].mean()) / df[cols].std()

        left = int(len(df)*(1-split))
        train = df[:left].copy()
        test = df[left:].copy()

        model.fit(train[cols], train['d'])

        predict = model.predict(train[cols])
        acc = accuracy_score(train['d'], predict)
        print(f'In Sample  | {self.ticker.ticker:5s} | acc={acc:.4f}')

        predict = model.predict(test[cols])
        acc = accuracy_score(test['d'], predict)
        print(f'Out Sample | {self.ticker.ticker:5s} | acc={acc:.4f}')

class AR():
    def __init__(self, ticker):
        self.ticker = ticker
    
    def fit(self, period='1y', lags=1, split=0.2):
        self.model = LinearRegression()

        df = self.ticker.history(period)[['Adj Close']].dropna()
        df['Lag_1'] = df['Adj Close'].shift(1)
        df['r'] = df['Adj Close'] - df['Lag_1']
        df['r%'] = df['r'] / df['Adj Close']

        for i in range(1, lags+1):
            df[f'r%_lag_{i}'] = df['r%'].shift(i)

        x = np.array(df.drop(['Adj Close', 'Lag_1', 'r', 'r%'], axis=1)[lags+1:])
        y = np.array(df['r%'][lags+1:])

        x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=split, shuffle=False)

        self.model.fit(x_train, y_train)
        accuracy = self.model.score(x_test, y_test)
        predict = self.model.predict(x_test)

        print(f'Accuracy: {accuracy}')
        print(f'Intercept: {self.model.intercept_}')
        print(f'Coefficient: {self.model.coef_}')

        plt.plot(y_test, color='red', label='Stock Return')
        plt.plot(predict, color='blue', label='Predicted Stock Return')
        plt.legend()
        plt.show()

class Model(ABC):
    def __init__(self, ticker):
        self.ticker = ticker
        self.model = self.get_model()
        

    def train(self, price='Adj Close', memory=60, period=600, split=0.2, epochs=50, batch_size=32):
        self.memory = memory
        self.raw_data = self.ticker.history().loc[:,price].copy().to_numpy()
        period = min(period, len(self.raw_data))
        data = self.raw_data[-period:]

        self.sc = MinMaxScaler(feature_range=(0, 1))
        data = self.sc.fit_transform(data.reshape(-1, 1)).reshape((-1))

        x_train, y_train, x_test, y_test = self.process_data(data, memory, int((1-split)*period))
        history = self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True, validation_data=(x_test, y_test))
        predict = self.sc.inverse_transform(self.model.predict(x_test))
        target = self.sc.inverse_transform(y_test.reshape(-1, 1))

        plt.plot(target, color='red', label=f'{self.ticker.ticker} Stock Price')
        plt.plot(predict, color='blue', label=f'Predicted {self.ticker.ticker} Stock Price')
        plt.title(f'{self.ticker.ticker} Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel(f'{self.ticker.ticker} Stock Price')
        plt.legend()
        plt.show()
        plt.clf()

    def predict(self):
        arr = self.raw_data[-self.memory:]
        data = self.sc.transform(arr.reshape(-1, 1))
        result = self.sc.inverse_transform(self.model.predict(data.reshape(1,-1,1)))

        print(result)
        # plt.plot(result, color='blue', label=f'Predicted {self.ticker.ticker} Stock Price')
        # plt.title(f'{self.ticker.ticker} Stock Price Prediction')
        # plt.xlabel('Time')
        # plt.ylabel(f'{self.ticker.ticker} Stock Price')
        # plt.show()
        # plt.clf()


    def process_data(self, data, memory, split):
        train_data, test_data = data[:split], data[split:]

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        for i in range(memory, len(train_data)):
            x_train.append(train_data[i-60:i])
            y_train.append(train_data[i])
        for i in range(memory, len(test_data)):
            x_test.append(test_data[i-60:i])
            y_test.append(test_data[i])

        x_train, y_train, x_test, y_test = np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)
        x_train = x_train.reshape(-1, memory, 1)
        x_test = x_test.reshape(-1, memory, 1)
        
        return x_train, y_train, x_test, y_test

    @abstractmethod
    def get_model(self):
        pass

class LSTM(Model):
    def get_model(self):
        model = Sequential([
            layers.LSTM(80, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(100),
            layers.Dropout(0.2),
            layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

class GRU(Model):
    def get_model(self):
        model = Sequential([
            layers.GRU(80, return_sequences=True),
            # layers.Dropout(0.5),
            layers.GRU(100),
            # layers.Dropout(0.5),
            # layers.Dense(25, activation='relu'),
            layers.Dense(1),
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model


