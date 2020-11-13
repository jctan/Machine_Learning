"""                                                                                         
Template for implementing QLearner  (c) 2015 Tucker Balch                                                                                       
                                                                                        
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
import random as rand


class QLearner(object):

    def __init__(self,
                 num_states=100,
                 num_actions=4,
                 alpha=0.2,
                 gamma=0.9,
                 rar=0.5,
                 radr=0.99,
                 dyna=0,
                 verbose=False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        # keep track of states and actions
        self.s = 0
        self.a = 0

        # initializing Q table for all 0s and records and update for each action
        self.q = np.zeros(shape=(num_states, num_actions))

        # tracking rewards for each action
        self.r = np.zeros(shape=(num_states, num_actions))

        # tracking transitions when action is taken
        self.t = {}

    def author(self):
        return 'jtan301'

    def querysetstate(self, s):
        """                                                                                         
        @summary: Update the state without updating the Q-table                                                                                         
        @param s: The new state                                                                                         
        @returns: The selected action                                                                                       
        """
        self.s = s
        if rand.uniform(0.0, 1.0) < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s, :])

        self.a = action

        if self.verbose:
            print "s =", s, "a =", action
        return action

    def query(self, s_prime, r):
        """                                                                                         
        @summary: Update the Q table and return an action                                                                                       
        @param s_prime: The new state                                                                                       
        @param r: The ne state                                                                                      
        @returns: The selected action                                                                                       
        """

        '''
        This came as described from ML4T udacity lecture
        '''
        # update q table with latest state and action
        self.q[self.s, self.a] = (1 - self.alpha) * self.q[self.s, self.a] + self.alpha * (r + self.gamma * np.max(self.q[s_prime, :]))

        self.t[len(self.t)] = [self.s, self.a, s_prime, r]

        '''
        This came as described from ML4T udacity lecture
        '''
        action = self.querysetstate(s_prime)
        self.rar = self.rar * self.radr

        '''
        resource to implement Dyna-Q: 
        1. https://towardsdatascience.com/reinforcement-learning-model-based-planning-methods-extension-572dfee4cceb
        2. http://intelligentonlinetools.com/blog/rl-dyna-q/
        '''
        # implementation of Dyna-Q
        if self.dyna > 0:
            for i in range(self.dyna):
                s, a, common_sprime, self.r[s, a] = self.t[rand.randint(0, len(self.t) - 1)]
                updated_action = np.argmax(self.q[common_sprime])
                self.q[s, a] = (1 - self.alpha) * self.q[s, a] + self.alpha * (self.r[s, a] + self.gamma * self.q[common_sprime, updated_action])

        if self.verbose:
            print "s =", s_prime, "a =", action, "r =", r
        return action


if __name__ == "__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
