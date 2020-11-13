"""MC2-P1: Market simulator.

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

import pandas as pd
import numpy as np
from datetime import datetime as dt
from util import get_data, plot_data


def author():
    return 'jtan301'


# compute the price
def compute_prices_df(sd, ed, symbols):
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices.index.name = 'Date'
    df_prices = df_prices.drop(['SPY'], axis=1)
    df_prices["Cash"] = 1.0
    return df_prices


# compute the trades
def compute_trades_df(df_trades, df_prices, symbol_list, commission, impact):
    symbol = symbol_list[0]
    df_trades['Cash'] = 0.0
    neg_num = -1
    old_val = -0.0
    new_val = 0
    for i in range(len(df_trades)):
        curr_trade = df_trades.loc[df_trades.index[i]][symbol]
        curr_stock_val = df_prices.loc[df_prices.index[i]][symbol]
        transaction_cost = (impact * curr_stock_val) - commission
        if curr_trade > 0:
            df_trades.ix[i, "Cash"] = (curr_trade * curr_stock_val + transaction_cost) * neg_num
        elif curr_trade < 0:
            df_trades.ix[i, "Cash"] = (curr_trade * curr_stock_val - transaction_cost) * neg_num
    df_trades["Cash"] = df_trades["Cash"].replace(old_val, new_val)
    return df_trades


# compute the holdings
def compute_holdings_df(df_trades, start_val):
    df_holdings = pd.DataFrame(np.zeros(df_trades.shape), index=df_trades.index, columns=df_trades.columns)
    df_holdings.ix[0, :] = df_trades.ix[0, :].copy()
    df_holdings["Cash"][0] = df_holdings["Cash"][0] + start_val

    for i in range(1, len(df_holdings)):
        df_holdings.ix[i, :] = df_holdings.ix[i - 1, :] + df_trades.ix[i, :]
    return df_holdings


def compute_portvals(df_trades, sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), start_val=1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    symbol_list = (list(df_trades)[:])

    # get the prices
    prices_df = compute_prices_df(sd, ed, symbol_list)

    # get the trades
    trades_df = compute_trades_df(df_trades, prices_df, symbol_list, commission, impact)

    # get the holdings
    holdings_df = compute_holdings_df(trades_df, start_val)

    # compute the values
    df_values = pd.DataFrame(index=prices_df.index, columns=prices_df.columns)
    df_values = df_values.fillna(0)
    df_values["Cash"] = 1.0
    df_values = holdings_df * prices_df

    # compute the portfolio values in dataFrame
    portvals = df_values.sum(axis=1)

    return portvals


def portfolio_vals_benchmark(sd, ed, symbols=['JPM']):
    zero_dec_const = 0.0
    one_thousand_const = 1000
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices = df_prices.drop(['SPY'], axis=1)
    df_prices.index.name = 'Date'
    df_trades = df_prices.copy()
    stock = symbols[0]
    for symbol in symbols:
        stock = symbol
    df_trades[symbol] = zero_dec_const
    df_trades.ix[0, stock] = one_thousand_const
    return df_trades


def compute_portfolio_stats(portfolio_val):
    start_date = min(portfolio_val.index)
    end_date = max(portfolio_val.index)
    portvals = portfolio_val / portfolio_val.ix[0, :]

    daily_return = (portfolio_val / portfolio_val.shift(1)) - 1
    cr = (portfolio_val[-1] / portfolio_val[0]) - 1
    adjusted_daily_return = daily_return[1:]
    adr = daily_return.mean()
    sddr = adjusted_daily_return.std()
    sr = np.sqrt(252.0) * ((adjusted_daily_return).mean() / sddr)

    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sr)
    print
    print "Cumulative Return of Fund: {}".format(cr)
    print
    print "Standard Deviation of Fund: {}".format(sddr)
    print
    print "Average Daily Return of Fund: {}".format(adr)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    return cr, adr, sddr, sr
