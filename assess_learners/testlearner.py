"""
Test a learner.  (c) 2015 Tucker Balch

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
"""

"""
Name: John Tan
GT ID: jtan301
"""

import util
import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as it
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time


def question_one(trainX, trainY, testX, testY):
    print "Running Question 1... "
    in_sample_rmse_result = []
    in_sample_corr_result = []
    out_sample_rmse_result = []
    out_sample_corr_result = []
    in_sample_result = []
    out_sample_result = []
    num_runs = 10
    for i in xrange(1, 51):
        learner = dtl.DTLearner(leaf_size=i, verbose=False)
        learner.addEvidence(trainX, trainY)

        rmse_in_total = 0
        rmse_out_total = 0
        corr_in_total = 0
        corr_out_total = 0

        #get in samples (train)
        predY_in = learner.query(trainX)
        rmse_in = math.sqrt(((trainY - predY_in) ** 2).sum() / trainY.shape[0])
        corr_in = np.corrcoef(predY_in, y=trainY)
        rmse_in_total += rmse_in
        corr_in_total += corr_in[0, 1]

        # get out samples (test)
        predY_out = learner.query(testX)
        rmse_out = math.sqrt(((testY - predY_out) ** 2).sum() / testY.shape[0])
        corr_out = np.corrcoef(predY_out, y=testY)
        rmse_out_total += rmse_out
        corr_out_total += corr_out[0, 1]

        # in samples RMSE
        avg_RMSE_in = rmse_in_total / num_runs
        avg_RMSE_out = rmse_out_total / num_runs
        in_sample_rmse_result.append(avg_RMSE_in)
        out_sample_rmse_result.append(avg_RMSE_out)

        # in samples Correlation
        avg_corr_in = corr_in_total / num_runs
        avg_corr_out = corr_out_total / num_runs
        in_sample_corr_result.append(avg_corr_in)
        out_sample_corr_result.append(avg_corr_out)

    print "In sample results"
    print "RMSE: ", in_sample_rmse_result
    print "corr: ", in_sample_corr_result

    print "Out of sample results"
    print "RMSE: ", out_sample_rmse_result
    print "corr: ", out_sample_corr_result

    return in_sample_rmse_result, out_sample_rmse_result, in_sample_corr_result, out_sample_corr_result


def question_two(trainX, trainY, testX, testY, bag_size):
    print "Running Question 2... "
    in_sample_rmse_result = []
    in_sample_corr_result = []
    out_sample_rmse_result = []
    out_sample_corr_result = []
    in_sample_result = []
    out_sample_result = []
    num_runs = 1
    for i in xrange(1, 51):
        learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={"leaf_size": i}, bags=bag_size, boost=False, verbose=False)
        learner.addEvidence(trainX, trainY)

        rmse_in_total = 0
        rmse_out_total = 0
        corr_in_total = 0
        corr_out_total = 0

        #get in samples (train)
        predY_in = learner.query(trainX)
        rmse_in = math.sqrt(((trainY - predY_in) ** 2).sum() / trainY.shape[0])
        corr_in = np.corrcoef(predY_in, y=trainY)
        rmse_in_total += rmse_in
        corr_in_total += corr_in[0, 1]

        # get out samples (test)
        predY_out = learner.query(testX)
        rmse_out = math.sqrt(((testY - predY_out) ** 2).sum() / testY.shape[0])
        corr_out = np.corrcoef(predY_out, y=testY)
        rmse_out_total += rmse_out
        corr_out_total += corr_out[0, 1]

        # in samples RMSE
        avg_RMSE_in = rmse_in_total / num_runs
        avg_RMSE_out = rmse_out_total / num_runs
        in_sample_rmse_result.append(avg_RMSE_in)
        out_sample_rmse_result.append(avg_RMSE_out)

        # in samples Correlation
        avg_corr_in = corr_in_total / num_runs
        avg_corr_out = corr_out_total / num_runs
        in_sample_corr_result.append(avg_corr_in)
        out_sample_corr_result.append(avg_corr_out)

    print "In sample results"
    print "RMSE: ", in_sample_rmse_result
    print "corr: ", in_sample_corr_result

    print "Out of sample results"
    print "RMSE: ", out_sample_rmse_result
    print "corr: ", out_sample_corr_result

    return in_sample_rmse_result, out_sample_rmse_result, in_sample_corr_result, out_sample_corr_result


def plot_data(in_sample_data, out_sample_data, yLabel, xLabel, in_label, out_label, legend_location, title, fileName):
    rangeX = np.arange(1, 51)
    plt.clf()
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.plot(rangeX, in_sample_data, label=in_label)
    plt.plot(rangeX, out_sample_data, label=out_label)
    plt.title(title)
    plt.legend(loc=legend_location)
    plt.savefig(fileName)
    plt.close()


# question 3
def DT_Time(trainX, trainY):
    print "Running Question 3 (DT Time)... "
    result = []
    for i in xrange(1, 51):
        startTime = time.time()
        DT_Learner = dtl.DTLearner(leaf_size=i, verbose=False)
        DT_Learner.addEvidence(trainX, trainY)
        endTime = time.time()
        finalResult = endTime - startTime
        result.append(finalResult)
    return result


def RT_Time(trainX, trainY):
    print "Running Question 3 (RT Time)... "
    result = []
    for i in xrange(1, 51):
        startTime = time.time()
        RT_Learner = rtl.RTLearner(leaf_size=i, verbose=False)
        RT_Learner.addEvidence(trainX, trainY)
        endTime = time.time()
        finalResult = endTime - startTime
        result.append(finalResult)
    return result


def DT_MAPE(trainX, trainY, testX, testY):
    print "Running Question 3 (DT MAPE)... "
    DT_MAPE_IN_Sample = []
    DT_MAPE_OUT_Sample = []

    for i in xrange(1, 51):
        DT_Learner = dtl.DTLearner(leaf_size=i, verbose=False)
        DT_Learner.addEvidence(trainX, trainY)
        predY_in = DT_Learner.query(trainX)
        DT_MAPE_IN_Sample.append(abs(trainY - predY_in).sum() / trainY.shape[0])
        predY_out = DT_Learner.query(testX)
        DT_MAPE_OUT_Sample.append(abs(testY - predY_out).sum() / trainY.shape[0])
    return DT_MAPE_IN_Sample, DT_MAPE_OUT_Sample


def RT_MAPE(trainX, trainY, testX, testY):
    print "Running Question 3 (RT MAPE)... "
    RT_MAPE_IN_Sample = []
    RT_MAPE_OUT_Sample = []

    for i in xrange(1, 51):
        RT_Learner = rtl.RTLearner(leaf_size=i, verbose=False)
        RT_Learner.addEvidence(trainX, trainY)
        predY_in = RT_Learner.query(trainX)
        RT_MAPE_IN_Sample.append(abs(trainY - predY_in).sum() / trainY.shape[0])
        predY_out = RT_Learner.query(testX)
        RT_MAPE_OUT_Sample.append(abs(testY - predY_out).sum() / trainY.shape[0])
    return RT_MAPE_IN_Sample, RT_MAPE_OUT_Sample


def MAPE_Plot(DT_MAPE_IN_Sample, DT_MAPE_OUT_Sample, RT_MAPE_IN_Sample, RT_MAPE_OUT_Sample):
    rangeX = np.arange(1, 51)
    plt.clf()
    plt.ylabel('Mean Absolute Percentage Error')
    plt.xlabel('Leaf Size')
    plt.plot(rangeX, DT_MAPE_IN_Sample, label='DTLearner Train: MAPE')
    plt.plot(rangeX, RT_MAPE_IN_Sample, label='RTLearner Train: MAPE')
    plt.plot(rangeX, DT_MAPE_OUT_Sample, label='DTLearner Test: MAPE')
    plt.plot(rangeX, RT_MAPE_OUT_Sample, label='RTLearner Test: MAPE')
    plt.title('Mean Absolute Percentage Error: DTLearner vs RTLeaner')
    plt.legend(loc='lower right')
    plt.savefig('Q3B.png')
    plt.close()


def remove_header_col(data):
    header = data[0]
    col = data[:, 0]

    # remove the header from the data
    if np.isnan(header).all():
        removedHeader = data[1:]
        data = removedHeader

    # remove non-numerical (e.g. date) on the first column
    if np.isnan(col).all():
        removedFirstCol = data[:, 1:]
        data = removedFirstCol
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)

    fileParam = sys.argv[1]
    data = np.genfromtxt(util.get_learner_data_file(fileParam), delimiter=',')

    data = remove_header_col(data)

    # compute how much of the data is training and testing
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    # Question 1
    in_rmse_result_Q1, out_rmse_result_Q1, in_corr_result_Q1, out_corr_result_Q1 = question_one(trainX, trainY, testX, testY)
    # Plot DTLearner RMSE
    plot_data(in_rmse_result_Q1, out_rmse_result_Q1, 'RMSE', 'Leaf Size', 'Train (In Sample): RMSE', 'Test (Out of Sample): RMSE', 'lower right', 'DTLearner: Leaf Size vs RMSE', 'Q1A.png')

    # Plot DTLearner Correlation
    plot_data(in_corr_result_Q1, out_corr_result_Q1, 'Correlation', 'Leaf Size', 'Train (In Sample): Correlation', 'Test (Out of Sample): Correlation', 'upper right', 'DTLearner: Leaf Size vs Correlation', 'Q1B.png')

    # Question 2 (Bag 10)
    in_rmse_result_Q2_10, out_rmse_result_Q2_10, in_corr_result_Q2_10, out_corr_result_Q2_10 = question_two(trainX, trainY, testX, testY, 10)
    # Plot DTLearner with Bagging RMSE
    plot_data(in_rmse_result_Q2_10, out_rmse_result_Q2_10, 'RMSE', 'Leaf Size', 'Train (In Sample): RMSE', 'Test (Out of Sample): RMSE', 'lower right', 'DTLearner with Bagging (Bag Size: 10): Leaf Size vs RMSE', 'Q2A_10.png')

    # Plot DTLearner with Bagging Correlation
    plot_data(in_corr_result_Q2_10, out_corr_result_Q2_10, 'Correlation', 'Leaf Size', 'Train (In Sample): Correlation', 'Test (Out of Sample): Correlation', 'upper right', 'DTLearner with Bagging (Bag Size: 10): Leaf Size vs Correlation', 'Q2B_10.png')

    # Question 2 (Bag 20)
    in_rmse_result_Q2_20, out_rmse_result_Q2_20, in_corr_result_Q2_20, out_corr_result_Q2_20 = question_two(trainX, trainY, testX, testY, 20)
    # Plot DTLearner with Bagging RMSE
    plot_data(in_rmse_result_Q2_20, out_rmse_result_Q2_20, 'RMSE', 'Leaf Size', 'Train (In Sample): RMSE', 'Test (Out of Sample): RMSE', 'lower right', 'DTLearner with Bagging (Bag Size: 20): Leaf Size vs RMSE', 'Q2A_20.png')

    # Plot DTLearner with Bagging Correlation
    plot_data(in_corr_result_Q2_20, out_corr_result_Q2_20, 'Correlation', 'Leaf Size', 'Train (In Sample): Correlation', 'Test (Out of Sample): Correlation', 'upper right', 'DTLearner with Bagging (Bag Size: 20): Leaf Size vs Correlation', 'Q2B_20.png')

    # Question 3
    DTTime = DT_Time(trainX, trainY)
    RTTime = RT_Time(trainX, trainY)

    plot_data(DTTime, RTTime, 'Time (s)', 'Leaf Size', 'Time: Decision Tree', 'Time: Random Tree', 'upper right', 'Time Comparison: DTLearner vs RTLearner', 'Q3A.png')

    DT_MAPE_IN_Data, DT_MAPE_OUT_Data = DT_MAPE(trainX, trainY, testX, testY)
    RT_MAPE_IN_Data, RT_MAPE_OUT_Data = RT_MAPE(trainX, trainY, testX, testY)
    MAPE_Plot(DT_MAPE_IN_Data, DT_MAPE_OUT_Data, RT_MAPE_IN_Data, RT_MAPE_OUT_Data)
