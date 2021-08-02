import random

class EpsilonGreedy():
    def __init__(self, epsilon, n_arms):
        self.epsilon = epsilon
        self.n_arms = n_arms
        self.values = [0] * n_arms              # Amount of reward for each arm
        self.counts = [0] * n_arms              # Number of times each arm has been chosen
        self.dependents = [[]] * n_arms
        self.trialnumber = 0                    # Number of rounds completed

    def reset(self):
        self.values = [0] * self.n_arms
        self.counts = [0] * self.n_arms
        self.trialnumber = 0

    def run_experiment(self, rounds):
        for i in range(rounds):
            self.select_arm()
        return self.counts

    def select_arm(self):
        if self.trialnumber < self.n_arms:
            chosen_arm = self.trialnumber
        elif random.random() > self.epsilon:
            chosen_arm = random.choice([i for i, val in enumerate(self.values) if val == max(self.values)])
        else:
            chosen_arm = random.randrange(self.n_arms)
        self.counts[chosen_arm] += 1
        return chosen_arm

    def update(self, chosen_arm, reward):
        self.values[chosen_arm] += reward
        self.trialnumber += 1
        for i in self.dependents[chosen_arm]:
            self.values[i] += 0.5 * reward

    def makeArmsDependent(self, *dependentArms):
        for x in dependentArms:
            self.dependents[x].append(2)
        # for x in dependentArms:
        #     for y in dependentArms:
        #         if x != y:
        #             self.dependents[x].append(y)

    def maxIndexCounter(self, maxIndex):
        indices = [0] * self.n_arms
        for i in range(self.n_arms):
            indices[i] = maxIndex.count(i)
        return indices

    def maxIndex(self):
        max_value = max(self.counts)
        return self.counts.index(max_value)

    def optimizeEpsilon(self):
        self.epsilon = 0.0
        optimalEpsilon = 0.2
        optimality = 0
        while self.epsilon < 1.0:
            maxIndex = []
            for i in range(10000):
                self.run_experiment(20)
                maxIndex.append(self.maxIndex())
                self.reset()
            x = self.maxIndexCounter(maxIndex)[5] * 5 + self.maxIndexCounter(maxIndex)[2]
            if x > optimality:
                optimality = x
                optimalEpsilon = self.epsilon
            self.epsilon += 0.01
        return optimalEpsilon

# f = EpsilonGreedy(0.1, 9)
# print(f.dependents)
# f.dependents[0].append(2)
# #f.makeArmsDependent(1,2,3)
# print(f.dependents)
# for i in range(20):
#     chosen = f.select_arm()
#     f.update(chosen, 1)
#
# counts = []
# rewards = []
# maxIndex = []