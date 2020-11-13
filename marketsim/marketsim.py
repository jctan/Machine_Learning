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
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'jtan301'


# compute the price
def compute_prices_df(orders_df):
    start_date = orders_df.index.values[0]
    end_date = orders_df.index.values[-1]
    stock_list = list(set(orders_df["Symbol"]))
    dates = pd.date_range(start_date, end_date)
    prices_df = get_data(stock_list, dates)
    # fill in NA for empty data
    prices_df.fillna(method='ffill', inplace=True)
    prices_df.fillna(method='bfill', inplace=True)
    prices_df["Cash"] = 1.0
    return prices_df


# compute the trades
def compute_trades_df(orders_df, prices_df, commission, impact):
    trades_df = pd.DataFrame(np.zeros(prices_df.shape), prices_df.index, prices_df.columns)
    mask_check = (orders_df['Order'] == "SELL")
    orders_df['Shares'] = orders_df['Shares'].mask(mask_check, -1 * orders_df["Shares"])

    for i, row in orders_df.iterrows():
        try:
            trade_val = row["Shares"] * prices_df.loc[i, row["Symbol"]]
            # compute transaction cost
            transaction_cost = abs(row["Shares"]) * prices_df.loc[i, row["Symbol"]] * impact
            trades_df.loc[i, row["Symbol"]] = trades_df.loc[i, row["Symbol"]] + row["Shares"]
            trades_df.loc[i, "Cash"] = trades_df.loc[i, "Cash"] - trade_val - commission - transaction_cost
        except:
            pass

    return trades_df


# compute the holdings
def compute_holdings_df(trades_df, prices_df, start_val):
    holdings_df = pd.DataFrame(np.zeros(prices_df.shape), prices_df.index, prices_df.columns)
    holdings_df.iloc[0, :-1] = trades_df.iloc[0, :-1].copy()
    holdings_df.iloc[0, -1] = trades_df.iloc[0, -1] + start_val

    for i in range(1, len(trades_df.index.values)):
        holdings_df.iloc[i] = holdings_df.iloc[i - 1] + trades_df.iloc[i]
    return holdings_df


def compute_portvals(orders_file="./orders/orders-01.csv", start_val=1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # read csv from orders_file as dataframe
    orders_df = pd.read_csv(orders_file, header=0, index_col='Date', parse_dates=True, na_values=['nan'])

    # sort the orders
    orders_df = orders_df.sort_index()

    # get the prices
    prices_df = compute_prices_df(orders_df)

    # get the trades
    trades_df = compute_trades_df(orders_df, prices_df, commission, impact)

    # get the holdings
    holdings_df = compute_holdings_df(trades_df, prices_df, start_val)

    # compute the values
    values_df = holdings_df * prices_df

    # compute the portfolio values in dataFrame
    portvals = pd.DataFrame(values_df.sum(axis=1), values_df.index, ["port_val"])

    return portvals


# compute the portfolio value
def compute_portfolio(allocs, prices_df, sv=1):
    prices_normalized = prices_df / prices_df.iloc[0]
    alloced = prices_normalized * allocs
    pos_vals = alloced * sv
    portfolio_val = np.sum(pos_vals, axis=1)
    return portfolio_val


# compute the portoflio stats of cr, adr, sddr, sr
def compute_portfolio_stats(portfolio_val):
    daily_return = (portfolio_val / portfolio_val.shift(1)) - 1
    cr = (portfolio_val[-1] / portfolio_val[0]) - 1
    adr = daily_return.mean()
    sddr = daily_return.std()
    adjusted_daily_retrun = daily_return - 0.0
    sr = np.sqrt(252.0) * ((adjusted_daily_retrun).mean() / sddr)
    return cr, adr, sddr, sr


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders.csv"
    #of = "./orders/orders-short.csv"
    #of = "./orders/orders-short.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    df = pd.read_csv(of, header=0, index_col='Date', parse_dates=True, na_values=['nan'])

    # get start date and end date
    start_date = min(df.index)
    end_date = max(df.index)

    # get the data for SPX
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]
    # compute the portfolio value for SPX
    portfolio_vals_SPX = compute_portfolio([1.0], prices_SPX)

    # get the portfolio stats for cr, adr, sddr, sr
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = compute_portfolio_stats(portfolio_vals_SPX)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX : {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX : {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX : {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
