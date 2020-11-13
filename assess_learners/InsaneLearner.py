"""
Name: John Tan
GT ID: jtan301
"""

import numpy as np
import BagLearner as bl
import LinRegLearner as lrl


class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.learners = []
        for i in range(0, 20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))

    def author(self):
        print 'jtan301'

    def addEvidence(self, Xtrain, Ytrain):
        for i in xrange(len(self.learners)):
            self.learners[i].addEvidence(Xtrain, Ytrain)

    def query(self, trainX):
        results = np.array([i.query(trainX) for i in self.learners])
        return np.mean(results, axis=0)
