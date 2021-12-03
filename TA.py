'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Student Name  : 

@Date          : Nov 2021

Technical Indicators

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np

from datetime import date
from scipy.stats import norm

from math import log, exp, sqrt

from stock import *

class SimpleMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._sma = {}

    def _calc(self, period, price_source):
        '''
        for a given period, calc the SMA as a pandas series from the price_source
        which can be  open, high, low or close
        '''
        result = None
        #TODO
        self.period = period
        self.price_source = price_source
        result = self.ohlcv_df[price_source].rolling(period).mean()
        #end TODO
        
        return(result)
        
    def run(self, price_source = 'close'):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._sma[period] = self._calc(period, price_source)
    
    def get_series(self, period):
        return(self._sma[period])

    
class ExponentialMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._ema = {}

    def _calc(self, period):
        '''
        for a given period, calc the SMA as a pandas series
        '''
        result = None
        #TODO: implement details here
        result = self.ohlcv_df['close'].ewm(span=period, adjust=False).mean()
        #end TODO
        
        return(result)
        
    def run(self):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._ema[period] = self._calc(period)

    def get_series(self, period):
        return(self._ema[period])


class RSI(object):

    def __init__(self, ohlcv_df, period = 14):
        self.ohlcv_df = ohlcv_df
        self.period = period
        self.rsi = None

    def get_series(self):
        return(self.rsi)

    def run(self):
        '''
        calculate RSI
        '''
        #TODO: implement details here
        # self.rsi = ...
        #lower & higher closes
        up = df['close'].diff().clip(lower=0)
        down = -1 * df['close'].diff().clip(upper=0)
        
        ma_up = up.ewm(com = period - 1, adjust = True, min_period = period).mean()
        ma_down = down.ewm(com = period - 1, adjust = True, min_period = period).mean()
        self.rsi = ma_up/ ma_down
        rsi = 100 - (100/(1+rsi))
        
        #end TODO

class VWAP(object):

    def __init__(self, ohlcv_df):
        self.ohlcv_df = ohlcv_df
        self.vwap = None

    def get_series(self):
        return(self.vwap)

    def run(self):
        '''
        calculate VWAP
        '''
        #TODO: implement details here
        v = df['volume'].values
        tp = (df['low']+df['close']+df['high']).div(3).values
        #end TODO
        
        return df.assign(vwap = (tp * v).cumsum()/v.cumsum())
        #price = (self.ohlcv_df['high'] + self.ohlcv_df['low'] + self.ohlcv_df['close']) / 3
        #self.vwap = ((self.ohlcv_df['volume'] * price).cumsum()) / self.ohlcv_df['volume'].cumsum()


def _test():
    # simple test cases
    symbol = 'AAPL'
    stock = Stock(symbol)
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    stock.get_daily_hist_price(start_date, end_date)

    periods = [9, 20, 50, 100, 200]
    smas = SimpleMovingAverages(stock.ohlcv_df, periods)
    smas.run()
    s1 = smas.get_series(9)
    print(s1.index)
    print(s1)

    rsi_indicator = RSI(stock.ohlcv_df)
    rsi_indicator.run()

    print(f"RSI for {symbol} is {rsi_indicator.rsi}")
    

if __name__ == "__main__":
    _test()

