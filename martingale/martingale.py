"""Assess a betting strategy.

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

import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt


def author():
    return 'jtan301'  # replace tb34 with your Georgia Tech username.


def gtid():
    return 903366741  # replace with your GT ID number


def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def test_code():
    win_prob = 0.60  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    print get_spin_result(win_prob)  # test the roulette spin

    # add your code here to implement the experiments

    # running simulator from 10 to 1000 to track the wins
    original_winnings = np.zeros(1001)

    # start running simulator at 1000 times to track the wins
    winnings_bets = np.zeros((1000, 1001))

    # bank roll = 0 for assignment 1
    experiment1(win_prob, original_winnings, winnings_bets, 0)

    # rankroll = 256 for assignment 2
    experiment2(win_prob, original_winnings, winnings_bets, 256)


# Figure 1 - 3: Explore the strategy and make more charts
def experiment1(win_prob, original_winnings, winnings_bets, bRoll):

    # figure 1
    plot_multiple_runs(win_prob, original_winnings, bRoll)
    # figure 2
    plot_mean(win_prob, original_winnings, winnings_bets, bRoll, 'Figure 2: Mean and Mean $\pm$ STD', 'Figure2.png')
    # figure 3
    plot_median(win_prob, original_winnings, winnings_bets, bRoll, 'Figure 3: Median and Median $\pm$ STD', 'Figure3.png')


# Figure 4 & 5: A more realistic gambling simulator
def experiment2(win_prob, original_winnings, winnings_bets, bRoll):

    # figure 4
    plot_mean(win_prob, original_winnings, winnings_bets, bRoll, 'Figure 4: Mean and Mean $\pm$ STD and $\$256$ Bank Roll', 'Figure4.png')
    # figure 5
    plot_median(win_prob, original_winnings, winnings_bets, bRoll, 'Figure 5: Median and Median $\pm$ STD and $\$256$ Bank Roll', 'Figure5.png')


# The different plt methods are from the matplotlib: https://matplotlib.org/users/pyplot_tutorial.html
def plot_multiple_runs(win_prob, original_winnings, bRoll):
    plt.clf()
    for i in xrange(10):
        num_test = str(i + 1)
        num_winnings = gambling_simulator(win_prob, original_winnings, bRoll)
        plt.plot(num_winnings, label='Test' + num_test)
    plt.legend(loc='lower right')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Num of Spins')
    plt.ylabel('Num of Winnings')
    plt.title('Figure 1: 10 Diff Runs')
    plt.savefig('Figure1.png')
    plt.close()


# The different plt methods are from the matplotlib: https://matplotlib.org/users/pyplot_tutorial.html
def plot_mean(win_prob, original_winnings, winnings_bets, bRoll, titleName, fileName):

    for i in xrange(1000):
        winnings_bets[i] = gambling_simulator(win_prob, original_winnings, bRoll)
    mean_wins = np.mean(winnings_bets, axis=0)
    standardDev = np.std(winnings_bets, axis=0)
    mean_Label = 'Mean'
    mean_STD_Plus = mean_wins + standardDev
    mean_STD_Plus_Label = 'Mean + STD'
    mean_STD_Minus = mean_wins - standardDev
    mean_STD_Minus_Label = 'Mean - STD'
    plt.clf()
    plt.plot(mean_STD_Plus, label=mean_STD_Plus_Label)
    plt.plot(mean_STD_Minus, label=mean_STD_Minus_Label)
    plt.plot(mean_wins, label=mean_Label)
    plt.legend(loc='lower right')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Num of Spins')
    plt.ylabel('Num of Winnings')
    plt.title(titleName)
    plt.savefig(fileName)
    plt.close()


# The different plt methods are from the matplotlib: https://matplotlib.org/users/pyplot_tutorial.html
def plot_median(win_prob, original_winnings, winnings_bets, bRoll, titleName, fileName):

    for i in xrange(1000):
        winnings_bets[i] = gambling_simulator(win_prob, original_winnings, bRoll)
    median_wins = np.median(winnings_bets, axis=0)
    standardDev = np.std(winnings_bets, axis=0)
    median_Label = 'Median'
    median_STD_Plus = median_wins + standardDev
    median_STD_Plus_Label = 'Median + STD'
    median_STD_Minus = median_wins - standardDev
    median_STD_Minus_Label = 'Median - STD'
    plt.clf()
    plt.plot(median_STD_Plus, label=median_STD_Plus_Label)
    plt.plot(median_STD_Minus, label=median_STD_Minus_Label)
    plt.plot(median_wins, label=median_Label)
    plt.legend(loc='lower right')
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Num of Spins')
    plt.ylabel('Num of Winnings')
    plt.title(titleName)
    plt.savefig(fileName)
    plt.close()

###
# code from overview:
# http://quantsoftware.gatech.edu/Summer_2019_Project_1:_Martingale
###
def gambling_simulator(win_prob, original_winnings, bRoll):
    episode_winnings = 0
    winning_amount = 80  # the number to stop betting
    time_limit = 1000  # setting time limit
    k = 0
    kIndex = k + 1
    maxIndex = 1000 + 1

    while episode_winnings < winning_amount:
        won = False
        bet_amount = 1

        while not won:
            k += 1
            won = get_spin_result(win_prob)
            if won is True:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2

            # when it reaches its time limit, just return the winning episode
            if k == time_limit:
                return episode_winnings

            ##
            # bank roll strategies from: https://github.com/wdm0006/keeks/tree/master/keeks/strategies
            ##
            # if bet_amount has reached over bankroll
            bet_amount = check_bet_amount(bRoll, episode_winnings, bet_amount)

            # when it reaches its bank roll and there's no more bet amounts
            original_winnings[k] = episode_winnings
            kIndex = k + 1
            if bet_amount == 0:
                original_winnings[kIndex:maxIndex] = original_winnings[k]
                return original_winnings

    original_winnings[kIndex:maxIndex] = original_winnings[k]
    return original_winnings


def check_bet_amount(bRoll, episode_winnings, bet_amount):
    if 0 < bRoll:
        total_bet_amount = episode_winnings + bRoll
        bet_amount = min(bet_amount, total_bet_amount)
    return bet_amount


if __name__ == "__main__":
    test_code()
