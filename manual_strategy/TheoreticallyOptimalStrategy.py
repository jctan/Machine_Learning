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
import indicators as ind
from util import get_data, plot_data
import marketsimcode as ms


def compute_prices_df(sd, ed, symbols = ['JPM']):
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices = df_prices.drop(['SPY'], axis=1)
    return df_prices

def compute_trades_df(df_prices, df_trades, symbols):
    stock = symbols[0]
    df_trades[stock] = 0
    total_holdings = 0
    zero = 0
    one_thousand = 1000
    neg_one_thousand = -1000
    two_thousand = 2000

    for i in xrange(len(df_prices)):
        if total_holdings == zero:
            trade_shares = one_thousand
        elif total_holdings == neg_one_thousand or trade_shares == one_thousand:
            trade_shares = two_thousand
        curr_stock_price = df_prices.loc[df_prices.index[i]][stock]
        last_stock_price = len(df_prices) - 1

        if i != last_stock_price:
            nxt_stock_price = df_prices.index[i + 1]
            nxt_day_stock_price = df_prices.loc[nxt_stock_price][stock]

            if curr_stock_price < nxt_day_stock_price and total_holdings <= zero:
                total_holdings += trade_shares
                df_trades.ix[i, stock] = trade_shares
            elif curr_stock_price > nxt_day_stock_price and total_holdings >= zero:
                total_holdings -= trade_shares
                df_trades.ix[i, stock] = -trade_shares
    return df_trades


def testPolicy(symbols = ['JPM'], sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), sv = 100000):
    df_prices = compute_prices_df(sd, ed, symbols)
    df_prices.index.name = 'Date'
    df_trades = df_prices.copy()
    df_trades = compute_trades_df(df_prices, df_trades, symbols)

    return df_trades



def plot_theoretically_optimal_strategy(symbols, adjusted_portvals, adjusted_portvals_benchmark):
    symbol = symbols[0]
    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.plot(adjusted_portvals, label='Optimal Portfolio', color='r')
    plt.plot(adjusted_portvals_benchmark, label='Benchmark', color='g')
    plt.ylabel('Portfolio Value')
    plt.xlabel('Date')
    plt.title("Optimal Portfolio vs Benchmark ({}): 1/1/2008 - 12/31/2009".format(symbol))
    plt.legend(loc="upper left")
    plt.savefig('theoretically_optimal_strategy.png')
    plt.close()

def theoretically_optimal_strategy(sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), symbols=['JPM'], commission=0.00, impact=0.00):
    df_trades = testPolicy(symbols=symbols, sd=sd, ed=ed)

    portvals = ms.compute_portvals(df_trades, sd=sd, ed=ed, commission=commission, impact=impact)
    portvals_benchmark = ms.portfolio_vals_benchmark(sd=sd, ed=ed, symbols=symbols)
    final_portvals_benchmark = ms.compute_portvals(portvals_benchmark, sd=sd, ed=ed, commission=commission, impact=impact)

    ms.compute_portfolio_stats(portvals)
    ms.compute_portfolio_stats(final_portvals_benchmark)

    adjusted_portvals = portvals / portvals.ix[0, :]
    adjusted_portvals_benchmark = final_portvals_benchmark / final_portvals_benchmark.ix[0, :]

    plot_theoretically_optimal_strategy(symbols, adjusted_portvals, adjusted_portvals_benchmark)


if __name__ == "__main__":
    in_sample_sd = dt(2008, 1, 1)
    in_sample_ed = dt(2009, 12, 31)
    theoretically_optimal_strategy(sd=in_sample_sd, ed=in_sample_ed)