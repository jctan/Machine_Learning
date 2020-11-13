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
from matplotlib import lines as lns
import numpy as np
from datetime import datetime as dt
import indicators as ind
from util import get_data, plot_data
import marketsimcode as ms


def author():
    return 'jtan301'


def compute_prices_df(sd, ed, symbols=['JPM']):
    dates = pd.date_range(sd, ed)
    df_prices = get_data(symbols, dates, addSPY=True)
    df_prices = df_prices.drop(['SPY'], axis=1)
    return df_prices


def compute_trades_df(df_prices, df_trades, stock, master='in_sample'):
    df_trades[stock] = 0
    total_holdings = 0
    num_action = 0
    final_action = 0
    zero = 0
    one_thousand = 1000
    neg_one_thousand = -1000
    two_thousand = 2000

    ninty_five = 0.95
    twenty = 0.2
    eighty = 0.8
    one_hundred = 1.0
    one_const = 1
    two_const = 2
    buy_const = "BUY"
    hold_const = "HOLD"
    sell_const = "SELL"

    if master == 'in_sample':
        master_frame = ind.in_sample_manual_df()
    elif master == 'out_sample':
        master_frame = ind.out_sample_comparative_df(master=master)

    for i in xrange(len(df_prices)):
        if total_holdings == zero:
            trade_shares = one_thousand
        elif total_holdings == neg_one_thousand or trade_shares == one_thousand:
            trade_shares = two_thousand

        master_frame_index = master_frame.index[i]
        master_frame_index_loc = master_frame.loc[master_frame.index[i]]
        mom = master_frame_index_loc['MOM']
        sma = master_frame_index_loc['SMA']
        bbp = master_frame_index_loc['BBP']

        if mom < zero and sma < ninty_five and bbp <= twenty:
            num_action = one_const
        elif mom > zero and sma > one_hundred and bbp >= eighty:
            num_action = two_const

        if num_action == final_action:
            num_action = zero

        if num_action == one_const:
            total_holdings += trade_shares
            order_status = buy_const
            final_shares = trade_shares
        elif num_action == two_const:
            order_status = sell_const
            total_holdings -= trade_shares
            final_shares = -trade_shares
        else:
            order_status = hold_const

        if num_action != zero:
            final_action = num_action
        if order_status == hold_const:
            df_trades.ix[i, stock] = zero
        else:
            df_trades.ix[i, stock] = final_shares

    return df_trades


def testPolicy(symbols=['JPM'], sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), sv=100000, master='in_sample'):
    df_prices = compute_prices_df(sd, ed, symbols)
    df_trades = df_prices.copy()
    stock = symbols[0]

    df_trades = compute_trades_df(df_prices, df_trades, stock)

    return df_trades


def plot_in_out_sample_comparative_benchmark(symbols, adjusted_portvals, adjusted_portvals_benchmark, df_trades, master='in_sample'):
    zero_const = 0
    symbol = symbols[0]
    plt.clf()
    plt.figure(figsize=(10, 8))
    plt.plot(adjusted_portvals, color='r')
    plt.plot(adjusted_portvals_benchmark, color='g')
    if master == 'in_sample':
        title_name = 'Manual Rule-Based vs. Benchmark ({}): 1/1/2008 - 12/31/2009'.format(symbol)
    elif master == 'out_sample':
        title_name = 'Manual Rule-Based vs. Benchmark ({}): 1/1/2010 - 12/31/2011'.format(symbol)
    plt.title(title_name)
    plt.ylabel('Portfolio Value')
    plt.xlabel('Date')
    for i, row in df_trades.iterrows():
        if row[zero_const] > zero_const:
            plt.axvline(i, color='b')
        elif row[zero_const] < zero_const:
            plt.axvline(i, color='k')
    long_line = lns.Line2D([], [], color='b', label='LONG')
    short_line = lns.Line2D([], [], color='k', label='SHORT')
    in_sample_line = lns.Line2D([], [], color='r', label='In Sample: Manual Rule-Based')
    out_sample_line = lns.Line2D([], [], color='g', label='Out of Sample: Benchmark')
    list_of_handles = [long_line, short_line, in_sample_line, out_sample_line]
    plt.legend(handles=list_of_handles)
    if master == 'in_sample':
        pic = 'in_sample_manual_benchmark'
    elif master == 'out_sample':
        pic = 'out_sample_comparative_benchmark'
    plt.savefig(pic + '.png')
    plt.close()


def manual_strategy(sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), symbols=['JPM'], master='in_sample'):
    df_trades = testPolicy(symbols=symbols, master=master, sd=sd, ed=ed)

    portvals = ms.compute_portvals(df_trades, sd=sd, ed=ed)
    portvals_benchmark = ms.portfolio_vals_benchmark(sd=sd, ed=ed, symbols=symbols)
    final_portvals_benchmark = ms.compute_portvals(portvals_benchmark, sd=sd, ed=ed)

    ms.compute_portfolio_stats(portvals)
    ms.compute_portfolio_stats(final_portvals_benchmark)

    adjusted_portvals = portvals / portvals.ix[0, :]
    adjusted_portvals_benchmark = final_portvals_benchmark / final_portvals_benchmark.ix[0, :]

    plot_in_out_sample_comparative_benchmark(symbols, adjusted_portvals, adjusted_portvals_benchmark, df_trades, master=master)


if __name__ == '__main__':
    in_sample_sd = dt(2008, 1, 1)
    in_sample_ed = dt(2009, 12, 31)
    out_sample_sd = dt(2010, 1, 1)
    out_sample_ed = dt(2011, 12, 31)
    manual_strategy(sd=in_sample_sd, ed=in_sample_ed, master='in_sample')
    manual_strategy(sd=out_sample_sd, ed=out_sample_ed, master='out_sample')
