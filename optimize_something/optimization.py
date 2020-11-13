"""MC1-P2: Optimize a portfolio.

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
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as scipyOp

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality


def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),
                       syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    prices_SPY = prices_SPY / prices_SPY.iloc[0]

    # initialize allocs
    len_syms = len(syms)
    allocs = np.ones(len_syms) / len_syms

    # normalized price
    prices_normalized = prices / prices.iloc[0]

    # return sr to minimize
    def get_sr(allocs, prices_normalized):
        sf = 250  # samling frequency
        price_allocated = prices_normalized.values * allocs
        portfolio_price = np.sum(price_allocated, axis=1)
        portfolio_daily_returns = (portfolio_price[1:] / portfolio_price[:-1]) - 1
        adr = portfolio_daily_returns.mean()  # average daily report
        sddr = portfolio_daily_returns.std()  # standard deviation daily return
        sr = -(np.sqrt(sf) * (adr / sddr))
        return sr

    ###
    #'constraints' from the sugguestions on constraints for scipy.optimization - http://quantsoftware.gatech.edu/Summer_2019_Project_2:_Optimize_Something
    ###
    ###
    # scipy.optimization.minimize reference - https://docs.scipy.org/doc/scipy/reference/tutorial/optimize.html
    ###
    # get the optimized result
    def get_optimal_portfolio(syms, allocs, prices_normalized):
        bounds = [(0.0, 1.0) for i in range(len_syms)]
        constraints = ({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})
        result = scipyOp.minimize(get_sr, allocs, args=prices_normalized, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3])  # add code here to find the allocations

    # get the allocated optimize result output
    allocs = get_optimal_portfolio(syms, allocs, prices_normalized)

    # get daily portfolio price
    price_allocated = prices_normalized * allocs
    portfolio_price = np.sum(price_allocated, axis=1)

    # compute output for cr, adr, sddr, sr
    def compute_portfolio_output(portfolio_price):
        rfr = 0.0
        sf = 252
        cr = (portfolio_price.iloc[-1] / portfolio_price.iloc[0]) - 1
        portfolio_daily_returns = (portfolio_price[1:].values / portfolio_price[:-1].values) - 1
        adr = portfolio_daily_returns.mean()  # average daily report
        sddr = portfolio_daily_returns.std()  # standard deviation daily return
        adjusted_portfolio_daily_returns = portfolio_daily_returns - rfr
        adjusted_adr = adjusted_portfolio_daily_returns.mean()
        sr = np.sqrt(sf) * (adjusted_adr / sddr)
        return [cr, adr, sddr, sr]

    cr, adr, sddr, sr = compute_portfolio_output(portfolio_price)
    # cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1]  # add code here to compute stats

    # Get daily portfolio value
    # port_val = prices_SPY  # add code here to compute daily portfolio values
    port_val = portfolio_price

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp.plot(grid=True, title='Daily Portfolio Value and SPY')
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.grid(linestyle='dotted')
        plt.legend(['Portfolio', 'SPY'])
        plt.savefig('plot.png')
        plt.close()

    return allocs, cr, adr, sddr, sr


def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date,
                                                        syms=symbols,
                                                        gen_plot=True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
