import math
import numpy as np
import random
import operator

class C_UCB():
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.B = [5.] * n_arms
        self.pulls = np.zeros(n_arms)
        self.empReward = np.zeros(n_arms)
        self.sumReward = np.zeros(n_arms)
        self.Index=dict(zip(range(n_arms), [np.inf]*n_arms))
        self.empReward[:] = np.inf
        self.empPseudoReward = np.zeros((n_arms, n_arms))
        self.sumPseudoReward = np.zeros((n_arms, n_arms))
        self.empPseudoReward[:,:] = np.inf
        self.t=0

    def reset(self):
        self.n_arms = [0] * self.n_arms
        self.B = [5.] * self.n_arms
        self.pulls = np.zeros(self.n_arms)
        self.empReward = np.zeros(self.n_arms)
        self.sumReward = np.zeros(self.n_arms)
        self.Index=dict(zip(range(self.n_arms), [np.inf]*self.n_arms))
        self.empReward[:] = np.inf
        self.empPseudoReward = np.zeros((self.n_arms, self.n_arms))
        self.sumPseudoReward = np.zeros((self.n_arms, self.n_arms))
        self.empPseudoReward[:,:] = np.inf
        self.t=0

    def select_arm(self):
        #add to set \ell for arms with pulls >t/K
        bool_ell = self.pulls >= (float(self.t - 1)/self.n_arms)

        max_mu_hat = np.max(self.empReward[bool_ell])

        if self.empReward[bool_ell].shape[0] == 1:
            secmax_mu_hat = max_mu_hat
        else:
            temp = self.empReward[bool_ell]
            temp[::-1].sort()
            secmax_mu_hat = temp[1]
        argmax_mu_hat = np.where(self.empReward == max_mu_hat)[0][0]

        #Set of competitive arms - update through the run
        min_phi = np.min(self.empPseudoReward[:, bool_ell], axis=1)

        comp_set = set()
        #Adding back the argmax arm
        comp_set.add(argmax_mu_hat)

        for arm in range(self.n_arms):
            if arm != argmax_mu_hat and min_phi[arm] >= max_mu_hat:
                comp_set.add(arm)
            elif arm == argmax_mu_hat and min_phi[arm] >= secmax_mu_hat:
                comp_set.add(arm)

        if self.t < self.n_arms:
            k_t = self.t %self.n_arms
        elif len(comp_set)==0:
            #UCB for empty comp set
            k_t = max(self.Index.items(), key=operator.itemgetter(1))[0]
        else:
            comp_Index = {ind: self.Index[ind] for ind in comp_set}
            k_t = max(comp_Index.items(), key=operator.itemgetter(1))[0]

        self.pulls[k_t] = self.pulls[k_t] + 1

        return k_t

    def update(self, chosen_arm, reward):
        k_t = chosen_arm
        self.pulls[k_t] = self.pulls[k_t] + 1

        #Update \mu_{k_t}
        self.sumReward[k_t] = self.sumReward[k_t] + reward
        self.empReward[k_t] = self.sumReward[k_t]/float(self.pulls[k_t])

        #Pseudo-reward updates!!!!
        # pseudoRewards = tables[k_t][reward-1, :] #(zero-indexed)
        pseudoRewards = np.ones(self.n_arms)

        self.sumPseudoReward[:, k_t] = self.sumPseudoReward[:, k_t] + pseudoRewards
        self.empPseudoReward[:, k_t] = np.divide(self.sumPseudoReward[:, k_t], float(self.pulls[k_t]))

        #Diagonal elements of pseudorewards
        self.empPseudoReward[np.arange(self.n_arms), np.arange(self.n_arms)] = self.empReward

        #Update UCB+LCB indices: Using pseduorewards
        for k in range(self.n_arms):
            if(self.pulls[k] > 0):
                #UCB index
                self.Index[k] = self.empReward[k] + self.B[k]*np.sqrt(2. * np.log(self.t+1)/self.pulls[k]) 

        self.t = self.t + 1    


