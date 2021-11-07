import random
import numpy as np
import operator

class C_ThompsonSampling():
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.B = [5.] * n_arms
        self.beta = 4.
        self.pulls = np.zeros(n_arms)
        self.empReward = np.zeros(n_arms)
        self.sumReward = np.zeros(n_arms)
        self.empReward[:] = np.inf
        self.empPseudoReward = np.zeros((n_arms, n_arms))
        self.sumPseudoReward = np.zeros((n_arms, n_arms))
        self.empPseudoReward[:,:] = np.inf
        self.t=0

    def reset(self):
        self.n_arms = [0] * self.n_arms
        self.B = [5.] * self.n_arms
        self.beta = 4.
        self.pulls = np.zeros(self.n_arms)
        self.empReward = np.zeros(self.n_arms)
        self.sumReward = np.zeros(self.n_arms)
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
            k_t = self.t #%numArms
        else:
            # Thompson Sampling
            thompson = self.ThompsonSample(self.empReward, self.pulls, self.beta)
            comp_values = {ind: thompson[ind] for ind in comp_set}
            k_t = max(comp_values.items(), key=operator.itemgetter(1))[0]

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

        self.t = self.t + 1    

    def ThompsonSample(self, empiricalMean, numPulls, beta):
        numArms = self.n_arms
        sampleArm = np.zeros(numArms)

        var_ = beta/(numPulls + 1.)
        std_ = np.sqrt(var_)

        mean_ = empiricalMean

        sampleArm = np.random.normal(mean_, std_)

        return sampleArm