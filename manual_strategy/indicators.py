'''
P6: Manual Strategy

Student Name: John Tan (replace with your name)
GT User ID: jtan301 (replace with your User ID)
GT ID: 903366741 (replace with your GT ID)
'''

import pandas as pd
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime as dt
from util import get_data, plot_data


def author():
    return 'jtan301'


def plot_bollinger_bands(df_prices, symbol, upper_band, lower_band, bb_mean, bbp):
    plt.clf()
    plt.figure(figsize=(10, 11))
    plt.rc('font', size=12)
    plt.subplot(211)
    plt.title('JPM Stock Price vs. Bollinger Bands (1/1/2008 - 12/31/2009)')
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.plot(df_prices, label="{}".format(symbol))
    plt.plot(upper_band, label="Upper Band")
    plt.plot(lower_band, label="Lower Band")
    plt.plot(bb_mean, label="BBP Mean")
    plt.legend(loc="lower left")

    plt.subplot(212)
    plt.plot(bbp, label="BBP", color='b')
    plt.title("% of JPM Bolinger Bands")
    plt.ylabel("BBP")
    plt.xlabel("Date")
    plt.legend(loc="lower right")
    plt.savefig("BollingerBands.png")
    plt.close()

def compute_bollinger_bands(df_prices, sd, ed, symbols=['JPM'], master='in_sample'):
    dates = pd.date_range(sd, ed)
    df_bb = get_data(symbols, dates, addSPY=True)
    symbol = symbols[0]
    df_bb = df_bb / df_bb.ix[0, :]
    num_windows = 10
    two_const = 2
    bb_std = pd.Series(df_bb[symbol]).rolling(window=num_windows).std()
    bb_mean = pd.Series(df_bb[symbol]).rolling(window=num_windows).mean()
    upper_band = bb_mean + bb_std * two_const
    upper_band = upper_band.dropna()
    lower_band = bb_mean - bb_std * two_const
    lower_band = lower_band.dropna()
    bbp = df_prices.copy()
    bbp_row = bbp.shape[0]
    for i in xrange(bbp_row):
        bbp_lower_band = (df_prices.ix[i, :] - lower_band.ix[i, :])
        bbp_upper_lower_band = (upper_band.ix[i, :] - lower_band.ix[i, :])
        bbp.ix[i, :] = bbp_lower_band / bbp_upper_lower_band
    if master == 'in_sample':
        plot_bollinger_bands(df_prices, symbol, upper_band, lower_band, bb_mean, bbp)
    bbp = bbp.dropna()
    return bbp
    


def plot_momentum(df_prices, symbols, momentum):
    symbol = symbols[0]
    zero_const = 0
    plt.clf()
    plt.figure(figsize=(10, 11))
    plt.subplot(211)
    plt.title('{} Stock Price vs Momentum (1/1/2008 - 12/31/2009)'.format(symbol))
    plt.plot(df_prices, label='{}'.format(symbol))
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.legend(loc="lower left")
    plt.subplot(212)
    plt.title('{} Stock Price vs Momentum (1/1/2008 - 12/31/2009)'.format(symbol))
    plt.plot(momentum, label="Momentum")
    plt.axhline(zero_const, color='g')
    plt.ylabel("Momentum")
    plt.xlabel("Date")
    plt.legend(loc="lower left")
    plt.savefig("Momentum.png")
    plt.close()


def compute_momentum(df_prices, sd, ed, symbols=['JPM'], master='in_sample'):
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices = df_prices / df_prices.ix[0, :]
    df_prices = df_prices.drop(['SPY'], axis=1)
    adjusted_price = df_prices.copy()
    adjusted_price = adjusted_price[10:]
    df_prices = df_prices.shift(10).dropna()
    momentum = (adjusted_price / df_prices) - 1
    if master == 'in_sample':
        plot_momentum(df_prices, symbols, momentum)
    return momentum


def plot_sma(df_prices, symbols, df_sma_prices_mean, df_price_per_sma):
    symbol = symbols[0]
    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.title('{} Stock Price vs. SMA (1/1/2008 - 12/31/2009)'.format(symbol))
    plt.plot(df_prices, label="{}".format(symbol))
    plt.plot(df_sma_prices_mean, label="SMA")
    plt.plot(df_price_per_sma, label="Price/SMA")
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.legend(loc="lower left")
    plt.savefig("SMA.png")
    plt.close()


def compute_sma(df_prices, sd, ed, symbols=['JPM'], master='in_sample'):
    dates = pd.date_range(sd, ed)
    df_sma_prices = get_data(symbols, dates, addSPY=True)
    df_sma_prices = df_sma_prices / df_sma_prices.ix[0, :]
    df_sma_prices = df_sma_prices.rolling(window=10, min_periods=10)
    df_sma_prices_mean = df_sma_prices.mean()
    df_sma_prices_mean = df_sma_prices_mean.dropna()
    df_sma_prices_mean = df_sma_prices_mean.drop(['SPY'], axis=1)
    df_sma_prices_mean = df_sma_prices_mean[1:]
    df_price_per_sma = df_prices / df_sma_prices_mean
    if master == 'in_sample':
        plot_sma(df_prices, symbols, df_sma_prices_mean, df_price_per_sma)
    return df_sma_prices_mean


def plot_rsi(df_prices, symbols, rsi, rsi_seventy_percent, rsi_thirty_percent):
    symbol = symbols[0]
    plt.clf()
    plt.figure(figsize=(10, 11))
    plt.subplot(211)
    plt.title('{} Stock Price vs. RSI (1/1/2008 - 12/31/2009)'.format(symbol))
    plt.plot(df_prices, label="JPM")
    plt.ylabel("Price")
    plt.xlabel("Date")
    plt.legend(loc="upper right")
    plt.subplot(212)
    plt.title('{} Stock Price vs. RSI (1/1/2008 - 12/31/2009)'.format(symbol))
    plt.plot(rsi, label="RSI")
    plt.plot(rsi_seventy_percent, label="Upper Bound - 70%")
    plt.plot(rsi_thirty_percent, label="Lower Bound - 30%")
    plt.ylabel("RSI")
    plt.xlabel("Date")
    plt.legend(loc="lower right")
    plt.savefig("RSI.png")
    plt.close()



def compute_rsi(df_prices, sd, ed, symbols=['JPM'], master='in_sample'):
    zero_const = 0
    seventy_percent = 70.0
    thirty_percent = 30.0
    one_hundred_const = 100.0
    one_const = 1.0
    dates = pd.date_range(sd, ed)
    df_rsi = get_data(symbols, dates, addSPY=True)
    df_rsi = df_rsi / df_rsi.ix[0, :]
    delta = df_rsi['JPM'].diff()
    delta_up = delta.copy()
    neg_delta_up = delta_up < zero_const
    delta_up[neg_delta_up] = zero_const
    delta_down = delta.copy()
    pos_delta_down = delta_down > zero_const
    delta_down[pos_delta_down] = zero_const
    rsi_mean_up = pd.Series(delta_up).rolling(window=10).mean()
    rsi_mean_down = pd.Series(delta_down).rolling(window=10).mean()
    rsi_mean_down = rsi_mean_down.abs()
    rsi = one_hundred_const - (one_hundred_const / (one_const + (rsi_mean_up / rsi_mean_down)))
    rsi = rsi.dropna()
    df_prices = df_prices.dropna()
    rsi_seventy_percent = rsi.copy()
    rsi_thirty_percent = rsi.copy()
    rsi_seventy_percent[:] = seventy_percent
    rsi_thirty_percent[:] = thirty_percent
    if master == 'in_sample':
        plot_rsi(df_prices, symbols, rsi, rsi_seventy_percent, rsi_thirty_percent)
    rsi = rsi.to_frame()
    return rsi

def get_df_prices(symbols, sd, ed):
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices = df_prices / df_prices.ix[0, :]
    df_prices = df_prices.drop(['SPY'], axis=1)
    return df_prices

def in_sample_manual_df(symbols=['JPM'], sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), master='in_sample'):
    date_const = 'Date'
    sma_const = 'SMA'
    rsi_const = 'RSI'
    bbp_const = 'BBP'
    mom_const = 'MOM'
    test_const = 'test'
    inner_const = 'inner'
    sd_const = dt(2007, 12, 17)
    df_prices = get_df_prices(symbols, sd, ed)
    mom = compute_momentum(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    sma = compute_sma(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    bbp = compute_bollinger_bands(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    rsi = compute_rsi(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    mom.index.name = date_const
    sma.index.name = date_const
    bbp.index.name = date_const
    rsi.index.name = date_const
    df_in_sample_manual = mom.join(sma, lsuffix=sma_const, rsuffix=rsi_const, how=inner_const)
    df_in_sample_manual = df_in_sample_manual.join(bbp, lsuffix=bbp_const, rsuffix=test_const, how=inner_const)
    df_in_sample_manual.columns = [mom_const, sma_const, bbp_const]
    return df_in_sample_manual



def out_sample_comparative_df(symbols=['JPM'], sd=dt(2010, 1, 1), ed=dt(2011, 12, 31), master='out_sample'):
    date_const = 'Date'
    sma_const = 'SMA'
    rsi_const = 'RSI'
    bbp_const = 'BBP'
    mom_const = 'MOM'
    test_const = 'test'
    inner_const = 'inner'
    sd_const = dt(2009, 12, 17)
    df_prices = get_df_prices(symbols, sd, ed)
    mom = compute_momentum(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    sma = compute_sma(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    bbp = compute_bollinger_bands(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    rsi = compute_rsi(df_prices=df_prices, symbols=symbols, sd=sd_const, ed=ed, master=master)
    mom.index.name = date_const
    sma.index.name = date_const
    bbp.index.name = date_const
    rsi.index.name = date_const
    df_out_sample_manual = mom.join(sma, lsuffix=sma_const, rsuffix=rsi_const, how=inner_const)
    df_out_sample_manual = df_out_sample_manual.join(bbp, lsuffix=bbp_const, rsuffix=test_const, how=inner_const)
    df_out_sample_manual.columns = [mom_const, sma_const, bbp_const]
    return df_out_sample_manual
