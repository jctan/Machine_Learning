"""                                                                                         
Template for implementing StrategyLearner (c) 2016 Tucker Balch                                                                                        
                                                                                        
Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332 
All Rights Reserved                                                                                        
                                                                                        
Template code for CS 4646/7646                                                                                      
                                                                                        
Georgia Tech asserts copyright ownership of this template and all derivative                                                                                        
works, including solutions to the projects assigned in this course. Students                                                                                        
and other users of this template code are advised not to share it with others                                                                                       
or to make it available on publicly viewable websites including repositories                                                                                        
such as github and gitlab.  This copyright statement should not be removed                                                                                      
or edited.                                                                                      
                                                                                        
We do grant permission to share solutions privately with non-students such                                                                                      
as potential employers. However, sharing with other current or future                                                                                       
students of CS 7646 is prohibited and subject to being investigated as a                                                                                        
GT honor code violation.                                                                                        
                                                                                        
-----do not edit anything above this line---                                                                                        
                                                                                        
Student Name: John Tan (replace with your name)                                                                                         
GT User ID: jtan301 (replace with your User ID)                                                                                         
GT ID: 903366741 (replace with your GT ID)                                                                                      
"""

from datetime import datetime as dt
import pandas as pd
import util as ut
import random


import RTLearner as rt
import BagLearner as bl
from indicators import *


class StrategyLearner(object):

    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=20, boost=False, verbose=False)

    def author(self):
        return 'jtan301'

    def get_prices(self, symbol, sd, ed):
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        return prices, syms

    def get_indicators(self, prices, syms):
        # get SMA
        sma = get_SMA(prices, syms)
        # get bollinger
        bollinger = get_bollinger_bands(prices, syms)
        # get momentum
        momentum = get_momentum(prices)
        # get rsi
        rsi = get_rsi(prices, syms)
        return sma, bollinger, momentum, rsi

    # Constructing trainX
    def compute_trainX(self, prices, syms, symbol):
        # get indicators
        sma, bbp, mom, rsi = self.get_indicators(prices, syms)

        df_sma = sma.rename(columns={symbol: 'SMA'})
        df_bollinger = bbp.rename(columns={symbol: 'BBA'})
        df_momentum = mom.rename(columns={symbol: 'VOL'})
        df_rsi = rsi.rename(columns={symbol: 'RSI'})

        df_indicators = pd.concat((df_sma, df_bollinger, df_momentum, df_rsi), axis=1)
        df_indicators.fillna(0, inplace=True)
        df_indicators = df_indicators[:-10]
        trainX = df_indicators.values
        return trainX

    # Constructing trainY
    def compute_trainY(self, prices, symbol):
        trainY = []
        last_ten_days = prices.shape[0] - 10
        for i in range(last_ten_days):
            last_ten_days_price = (prices.ix[i + 10, symbol] - prices.ix[i, symbol])
            ratio = last_ten_days_price / prices.ix[i, symbol]
            pos_two_impact = (0.02 + self.impact)
            neg_two_impact = (-0.02 - self.impact)
            if ratio > pos_two_impact:
                trainY.append(1)
            elif ratio < neg_two_impact:
                trainY.append(-1)
            else:
                trainY.append(0)
        trainY = np.array(trainY)
        return trainY

    def compute_testX(self, prices, syms, symbol):

        # get indicators
        sma, bbp, mom, rsi = self.get_indicators(prices, syms)

        # Constructing testX
        df_sma = sma.rename(columns={symbol: 'SMA'})
        df_bollinger = bbp.rename(columns={symbol: 'BBA'})
        df_momentum = mom.rename(columns={symbol: 'VOL'})
        df_rsi = rsi.rename(columns={symbol: 'RSI'})

        df_indicators = pd.concat((df_sma, df_bollinger, df_momentum, df_rsi), axis=1)
        df_indicators.fillna(0, inplace=True)
        testX = df_indicators.values
        return testX

    def compute_trades(self, prices, syms, testY):
        # construct trades df
        df_trades = prices.copy()
        df_trades.loc[:] = 0

        pos = 0
        short_position = -1
        zero_out_position = 0
        long_position = 1
        pos_one_thousand = 1000
        neg_one_thousand = -1000
        pos_two_thousand = 2000
        neg_two_thousand = -2000

        last_pos_price = prices.shape[0] - 1

        for i in range(last_pos_price):
            if pos == zero_out_position:
                if testY[i] > 0:
                    df_trades.values[i, :] = pos_one_thousand
                    pos = long_position
                elif testY[i] < 0:
                    df_trades.values[i, :] = neg_one_thousand
                    pos = short_position
            elif pos == long_position:
                if testY[i] < 0:
                    df_trades.values[i, :] = neg_two_thousand
                    pos = short_position
                elif testY[i] == 0:
                    df_trades.values[i, :] = neg_one_thousand
                    pos = zero_out_position
            else:
                if testY[i] > 0:
                    df_trades.values[i, :] = pos_two_thousand
                    pos = long_position
                elif testY[i] == 0:
                    df_trades.values[i, :] = pos_one_thousand
                    pos = zero_out_position

        if pos == -1:
            df_trades.values[prices.shape[0] - 1, :] = 1000
        elif pos == 1:
            df_trades.values[prices.shape[0] - 1, :] = -1000
        return df_trades

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol="IBM",
                    sd=dt(2008, 1, 1),
                    ed=dt(2009, 1, 1),
                    sv=10000):

        # add your code to do learning here

        # get prices and syms
        prices, syms = self.get_prices(symbol, sd, ed)

        # compute trainX and trainY
        trainX = self.compute_trainX(prices, syms, symbol)
        trainY = self.compute_trainY(prices, symbol)

        # learn the training data
        self.learner.addEvidence(trainX, trainY)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol="IBM",
                   sd=dt(2009, 1, 1),
                   ed=dt(2010, 1, 1),
                   sv=10000):

        # get prices and syms
        prices, syms = self.get_prices(symbol, sd, ed)

        # Constructing testX
        testX = self.compute_testX(prices, syms, symbol)

        # query testY
        testY = self.learner.query(testX)

        # construct trades df
        df_trades = self.compute_trades(prices, syms, testY)
        return df_trades


if __name__ == "__main__":
    print "One does not simply think up a strategy"
    aapl_sym = "AAPL"
    start_date = dt(2008, 1, 1)
    end_date = dt(2009, 12, 31)
    st = StrategyLearner()
    st.addEvidence(symbol=aapl_sym, sd=start_date, ed=end_date, sv=100000)
    st.testPolicy(symbol=aapl_sym, sd=start_date, ed=end_date, sv=100000)
