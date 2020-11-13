"""
Student Name: John Tan
GT User ID: jtan301
GT ID: 903366741
"""

from datetime import datetime as dt
import StrategyLearner as st
from ManualStrategy import *
from marketsimcode import *
import matplotlib.pyplot as plt


def author():
    return 'jtan301'


# impact = 0.0005
def compute_strategy_learner_0005(sd, ed, syms, impact):
    st_learner_0005 = st.StrategyLearner(verbose=False, impact=impact)
    st_learner_0005.addEvidence(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_trades_0005 = st_learner_0005.testPolicy(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_port_val_0005 = compute_portvals(df_trades=st_trades_0005, start_val=100000, commission=0, impact=impact)
    return st_port_val_0005


# impact = 0.005
def compute_strategy_learner_005(sd, ed, syms, impact):
    st_learner_005 = st.StrategyLearner(verbose=False, impact=impact)
    st_learner_005.addEvidence(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_trades_005 = st_learner_005.testPolicy(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_port_val_005 = compute_portvals(df_trades=st_trades_005, start_val=100000, commission=0, impact=impact)
    return st_port_val_005


# impact = 0.05
def compute_strategy_learner_05(sd, ed, syms, impact):
    st_learner_05 = st.StrategyLearner(verbose=False, impact=impact)
    st_learner_05.addEvidence(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_trades_05 = st_learner_05.testPolicy(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_port_val_05 = compute_portvals(df_trades=st_trades_05, start_val=100000, commission=0, impact=impact)
    return st_port_val_05


# impact = 0
def compute_strategy_learner_0(sd, ed, syms, impact):
    st_learner_0 = st.StrategyLearner(verbose=False, impact=impact)
    st_learner_0.addEvidence(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_trades_0 = st_learner_0.testPolicy(symbol=syms, sd=sd, ed=ed, sv=100000)
    st_port_val_0 = compute_portvals(df_trades=st_trades_0, start_val=100000, commission=0, impact=impact)
    return st_port_val_0


# print stats
def print_stats(sd, ed, st_port_val_0, st_port_val_0005, st_port_val_005, st_port_val_05):
    cum_ret_0, avg_daily_ret_0, std_daily_ret_0, sharpe_ratio_0 = compute_portfolio_stats(st_port_val_0)
    cum_ret_0005, avg_daily_ret_0005, std_daily_ret_0005, sharpe_ratio_0005 = compute_portfolio_stats(st_port_val_0005)
    cum_ret_005, avg_daily_ret_005, std_daily_ret_005, sharpe_ratio_005 = compute_portfolio_stats(st_port_val_005)
    cum_ret_05, avg_daily_ret_05, std_daily_ret_05, sharpe_ratio_05 = compute_portfolio_stats(st_port_val_05)

    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Cumulative Return with impact 0: {}".format(cum_ret_0)
    print "Cumulative Return with impact 0.0005: {}".format(cum_ret_0005)
    print "Cumulative Return with impact 0.005: {}".format(cum_ret_005)
    print "Cumulative Return with impact 0.05: {}".format(cum_ret_05)
    print
    print "Average Daily Return with impact 0: {}".format(avg_daily_ret_0)
    print "Average Daily Return with impact 0.0005: {}".format(avg_daily_ret_0005)
    print "Average Daily Return with impact 0.005: {}".format(avg_daily_ret_005)
    print "Average Daily Return with impact 0.05: {}".format(avg_daily_ret_05)
    print
    print "Standard Deviation with impact 0: {}".format(std_daily_ret_0)
    print "Standard Deviation with impact 0.0005: {}".format(std_daily_ret_0005)
    print "Standard Deviation with impact 0.005: {}".format(std_daily_ret_005)
    print "Standard Deviation with impact 0.05: {}".format(std_daily_ret_05)
    print
    print "Sharp Ration with impact 0: {}".format(sharpe_ratio_0)
    print "Sharp Ration with impact 0.0005: {}".format(sharpe_ratio_0005)
    print "Sharp Ration with impact 0.005: {}".format(sharpe_ratio_005)
    print "Sharp Ration with impact 0.05: {}".format(sharpe_ratio_05)


# plot stats
def plot_stats(st_port_val_0, st_port_val_0005, st_port_val_005, st_port_val_05):
    st_port_val_0_normed = st_port_val_0 / st_port_val_0[0]
    st_port_val_0005_normed = st_port_val_0005 / st_port_val_0005[0]
    st_port_val_005_normed = st_port_val_005 / st_port_val_005[0]
    st_port_val_05_normed = st_port_val_05 / st_port_val_05[0]

    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.title("Experiment 2: 0 vs. 0.0005 vs. 0.005 vs. 0.05 (Impact)")
    ax = st_port_val_0_normed.plot(fontsize=12, color="black", label='impact = 0')
    st_port_val_0005_normed.plot(ax=ax, color="red", label="impact = 0.0005")
    st_port_val_005_normed.plot(ax=ax, color="green", label='impact = 0.005')
    st_port_val_05_normed.plot(ax=ax, color="blue", label='impact = 0.05')
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    plt.legend()
    plt.savefig('experiment2.png')
    plt.close()


if __name__ == "__main__":

    np.random.seed(1992)
    sd = dt(2008, 1, 1)
    ed = dt(2009, 12, 31)
    syms = "JPM"
    impact_0005 = 0.0005
    impact_005 = 0.005
    impact_05 = 0.05
    impact_0 = 0

    # compute impact 0.0005
    st_port_val_0005 = compute_strategy_learner_0005(sd, ed, syms, impact_0005)

    # compute impact 0.005
    st_port_val_005 = compute_strategy_learner_005(sd, ed, syms, impact_005)

    # compute impact 0.05
    st_port_val_05 = compute_strategy_learner_05(sd, ed, syms, impact_05)

    # compute impact 0
    st_port_val_0 = compute_strategy_learner_0(sd, ed, syms, impact_0)

    # print stats
    print_stats(sd, ed, st_port_val_0, st_port_val_0005, st_port_val_005, st_port_val_05)

    # plot stats
    plot_stats(st_port_val_0, st_port_val_0005, st_port_val_005, st_port_val_05)
