""" 			  		 			 	 	 		 		 	  		   	  			  	
A simple wrapper for linear regression.  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
Note, this is NOT a correct DTLearner; Replace with your own implementation. 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
Student Name: Tucker Balch (replace with your name) 			  		 			 	 	 		 		 	  		   	  			  	
GT User ID: tb34 (replace with your User ID) 			  		 			 	 	 		 		 	  		   	  			  	
GT ID: 900897987 (replace with your GT ID) 			  		 			 	 	 		 		 	  		   	  			  	
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import warnings 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = []

    def author(self):
        return 'jtan301'

    # build training data to the decision tree
    def addEvidence(self, Xtrain, Ytrain):
        self.tree = self.build_tree(Xtrain, Ytrain)

    def build_tree(self, Xtrain, Ytrain):
        leaf = [[-1, np.nanmean(Ytrain), -1, -1]]

        if Xtrain.shape[0] <= self.leaf_size:
            return np.array(leaf, dtype=object)
        elif np.unique(Ytrain).size == 1:
            return np.array(leaf, dtype=object)
        else:
            position = self.find_position(Xtrain, Ytrain)

            splitVal = np.median(Xtrain[:, position])

            Xtrain_min = np.min(Xtrain[:, position])
            Xtrain_max = np.max(Xtrain[:, position])

            if(splitVal == Xtrain_min or splitVal == Xtrain_max):
                return np.array(leaf, dtype=object)
            else:
                leftX, leftY, rightX, rightY = self.build_left_right(Xtrain, Ytrain, splitVal, position)

                left_tree = self.build_tree(leftX, leftY)
                right_tree = self.build_tree(rightX, rightY)

                final_tree = self.combine_with_root(left_tree, right_tree, splitVal, position)

                return np.vstack(final_tree)

    def build_left_right(self, Xtrain, Ytrain, splitVal, position):
        left_x = Xtrain[Xtrain[:, position] <= splitVal]
        left_y = Ytrain[Xtrain[:, position] <= splitVal]

        right_x = Xtrain[Xtrain[:, position] > splitVal]
        right_y = Ytrain[Xtrain[:, position] > splitVal]

        return left_x, left_y, right_x, right_y

    def combine_with_root(self, leftTree, rightTree, splitVal, position):
        if len(leftTree.shape) == 1:
            begin_rightTree = 1
        else:
            begin_rightTree = leftTree.shape[0] + 1

        build_root = [[position, splitVal, 1, begin_rightTree]]
        root = np.array(build_root, dtype=object)
        return (root, leftTree, rightTree)

    def find_position(self, Xtrain, Ytrain):
        corr = []
        position = 0
        arrLength = Xtrain.shape[1]
        for i in xrange(arrLength):
            currentCorr = np.corrcoef(Xtrain[:, i], Ytrain)
            absCurrentCorr = abs(currentCorr[0, 1])
            corr.append(absCurrentCorr)
        position = np.nanargmax(corr)
        return position

    # query
    def query(self, points):
        preds = []
        for point in points:
            position = 0
            leaf_found = False
            while not leaf_found:
                node = self.tree[position]
                decision_index = int(node[0])

                if node[0] == -1:
                    result = node[1]
                    leaf_found = True
                elif point[decision_index] <= node[1]:
                    position = int(position + node[2])
                else:
                    position = int(position + node[3])
            preds.append(result)
        return np.array(preds)	  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			 	 	 		 		 	  		   	  			  	
