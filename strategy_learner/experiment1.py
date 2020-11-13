"""
Student Name: John Tan
GT User ID: jtan301
GT ID: 903366741
"""

from datetime import datetime as dt
import pandas as pd
import numpy as np
import StrategyLearner as st
from ManualStrategy import *
from marketsimcode import *
import matplotlib.pyplot as plt


def author():
    return 'jtan301'


# Benchmark
def compute_benchmark(sd, ed):
    st_learner = st.StrategyLearner(verbose=False, impact=0.00)
    st_learner.addEvidence(symbol="JPM", sd=sd, ed=ed, sv=100000)
    st_learner_test = st_learner.testPolicy("JPM", sd, ed)
    benchmark = pd.DataFrame(index=st_learner_test.index)
    benchmark['JPM'] = 0
    benchmark.iloc[0, 0] = 1000
    benchmark_port_val = compute_portvals(df_trades=benchmark, start_val=100000, commission=0, impact=0)
    return benchmark_port_val


# Manual Strategy
def compute_manual_strategy(sd, ed):
    trades = testPolicy(['JPM'], sd, ed, 100000)
    manual_strategy_port_val = compute_portvals(df_trades=trades, start_val=100000, commission=0, impact=0)
    return manual_strategy_port_val


# Strategy Learner
def compute_strategy_learner(sd, ed):
    strategy_learner = st.StrategyLearner(verbose=False, impact=0.00)
    strategy_learner.addEvidence(symbol="JPM", sd=sd, ed=ed, sv=100000)
    strategy_learner_test = strategy_learner.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=100000)
    strategy_learner_port_val = compute_portvals(df_trades=strategy_learner_test, start_val=100000, commission=0, impact=0)
    return strategy_learner_port_val


# print stats
def print_stats(sd, ed, benchmark_port_val, manual_strategy_port_val, strategy_learner_port_val):
    benchmark_cum_ret, benchmark_avg_daily_ret, benchmark_std_daily_ret, benchmark_sharpe_ratio = compute_portfolio_stats(benchmark_port_val)
    manual_strategy_cum_ret, manual_strategy_avg_daily_ret, manual_strategy_std_daily_ret, manual_strategy_sharpe_ratio = compute_portfolio_stats(manual_strategy_port_val)
    strategy_learner_cum_ret, strategy_learner_avg_daily_ret, strategy_learner_std_daily_ret, strategy_learner_sharpe_ratio = compute_portfolio_stats(strategy_learner_port_val)

    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Cumulative Return Benchmark: {}".format(benchmark_cum_ret)
    print "Cumulative Return Manual Strategy: {}".format(manual_strategy_cum_ret)
    print "Cumulative Return Strategy Learner: {}".format(strategy_learner_cum_ret)
    print
    print "Average Daily Return Benchmark: {}".format(benchmark_avg_daily_ret)
    print "Average Daily Return Manual Strategy: {}".format(manual_strategy_avg_daily_ret)
    print "Average Daily Return Strategy Learner: {}".format(strategy_learner_avg_daily_ret)
    print
    print "Standard Deviation Benchmark: {}".format(benchmark_std_daily_ret)
    print "Standard Deviation Manual Strategy: {}".format(manual_strategy_std_daily_ret)
    print "Standard Deviation Strategy Learner: {}".format(strategy_learner_std_daily_ret)
    print
    print "Sharp Ration Benchmark: {}".format(benchmark_sharpe_ratio)
    print "Sharp Ration Manual Strategy: {}".format(manual_strategy_sharpe_ratio)
    print "Sharp Ration Strategy Learner: {}".format(strategy_learner_sharpe_ratio)


# plot stats
def plot_stats(benchmark_port_val, manual_strategy_port_val, strategy_learner_port_val):
    benchmark_norm = benchmark_port_val / benchmark_port_val[0]
    manual_strategy_norm = manual_strategy_port_val / manual_strategy_port_val[0]
    strategy_learner_norm = strategy_learner_port_val / strategy_learner_port_val[0]

    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.title("Experiment 1: Strategy Learner vs. Manual Strategy vs. Benchmark")
    axis = manual_strategy_norm.plot(color="red", label="Manual Strategy")
    benchmark_norm.plot(ax=axis, color="green", label='Benchmark')
    strategy_learner_norm.plot(ax=axis, color="blue", label='Strategy Learner')
    axis.set_xlabel("Date")
    axis.set_ylabel("Portfolio Value")
    plt.legend()
    plt.savefig('experiment1.png')
    plt.close()


if __name__ == "__main__":
    np.random.seed(1992)
    sd = dt(2008, 1, 1)
    ed = dt(2009, 12, 31)

    # Benchmark
    benchmark_port_val = compute_benchmark(sd, ed)

    # ManualStrategy
    manual_strategy_port_val = compute_manual_strategy(sd, ed)

    # Strategy Learner
    strategy_learner_port_val = compute_strategy_learner(sd, ed)

    # Print Stats
    print_stats(sd, ed, benchmark_port_val, manual_strategy_port_val, strategy_learner_port_val)

    # Plot Stats
    plot_stats(benchmark_port_val, manual_strategy_port_val, strategy_learner_port_val)
