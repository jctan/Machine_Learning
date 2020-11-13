"""
Name: John Tan
GT ID: jtan301
"""

import numpy as np
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lr


class BagLearner(object):

    def __init__(self, learner={}, kwargs={}, bags=20, boost=False, verbose=False):
        self.learners = []
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.kwargs = kwargs
        for i in range(0, bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return 'jtan301'

    def addEvidence(self, Xtrain, Ytrain):
        for i in xrange(len(self.learners)):
            num_dataX = Xtrain.shape[0]
            randomChoice = np.random.choice(num_dataX, num_dataX)
            randomBagX = Xtrain[randomChoice]
            randomBagY = Ytrain[randomChoice]
            self.learners[i].addEvidence(randomBagX, randomBagY)

    def query(self, trainX):
        results = []
        for i in self.learners:
            results.append(i.query(trainX))
        return np.mean(results, axis=0)
