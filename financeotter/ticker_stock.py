from tkinter import N
from tkinter.messagebox import NO
from .utils import *
from .constant import *
from .ticker import Ticker


class Ticker_Stock(Ticker):

    def __init__(self, ticker: str) -> None:
        super().__init__(ticker)
        self._summary = None
        self._market_cap = None
        self._beta = None
        self._pe_ratio = None
        self._eps = None
        self._valuation_measures = None
        self._trading_information = None
        self._financial_highlights = None
        self._key_executives = None
        self._income_statement = None
        self._balance_sheet = None
        self._cash_flow = None
        self._isin = None

    @property
    def summary(self):
        if self._summary is None:
            self._summary = get_summary(self.ticker)
        return self._summary

    @property
    def market_cap(self):
        if self._market_cap is None:
            self._market_cap = self.summary.loc[CAP][0]
        return self._market_cap

    @property
    def beta(self):
        if self._beta is None:
            self._beta = self.summary.loc[BETA][0]
        return self._beta

    @property
    def pe_ratio(self):
        if self._pe_ratio is None:
            self._pe_ratio = self.summary.loc[PE][0]
        return self._pe_ratio

    @property
    def eps(self):
        if self._eps is None:
            self._eps = self.summary.loc[EPS][0]
        return self._eps

    @property
    def valuation_measures(self):
        if self._valuation_measures is None:
            self._valuation_measures, self._trading_information, self._financial_highlights = get_key_statistics(
                self.ticker)
        return self._valuation_measures

    @property
    def trading_information(self):
        if self._trading_information is None:
            self._valuation_measures, self._trading_information, self._financial_highlights = get_key_statistics(
                self.ticker)
        return self._trading_information

    @property
    def financial_highlights(self):
        if self._financial_highlights is None:
            self._valuation_measures, self._trading_information, self._financial_highlights = get_key_statistics(
                self.ticker)
        return self._financial_highlights

    @property
    def key_executives(self):
        if self._key_executives is None:
            self._key_executives = get_key_executives(self.ticker)
        return self._key_executives

    @property
    def income_statement(self):
        if self._income_statement is None:
            self._income_statement = get_income_statement(self.ticker)
        return self._income_statement

    @property
    def balance_sheet(self):
        if self._balance_sheet is None:
            self._balance_sheet = get_balance_sheet(self.ticker)
        return self._balance_sheet

    @property
    def cash_flow(self):
        if self._cash_flow is None:
            self._cash_flow = get_cash_flow(self.ticker)
        return self._cash_flow

    @property
    def isin(self):
        if self._isin is None:
            self._isin = get_isin(self.ticker)
        return self._isin
