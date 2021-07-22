import random

class EpsilonGreedy():
    def __init__(self, epsilon, n_arms):
        self.epsilon = epsilon
        self.n_arms = n_arms
        self.values = [0] * n_arms              # Amount of reward for each arm
        self.counts = [0] * n_arms              # Number of times each arm has been chosen
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
        # self.update(chosen_arm)
        self.counts[chosen_arm] += 1
        print(self.values)
        return chosen_arm

    def update(self, chosen_arm, reward):
        self.values[chosen_arm] += reward
        # arr = [0] * self.n_arms
        # for i in range(self.n_arms):
        #     if chosen_arm == i:
        #         self.values[chosen_arm] += arr[chosen_arm]
        self.trialnumber += 1

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
            print(self.maxIndexCounter( maxIndex ))
            x = self.maxIndexCounter(maxIndex)[5] * 5 + self.maxIndexCounter(maxIndex)[2]
            if x > optimality:
                optimality = x
                optimalEpsilon = self.epsilon
            self.epsilon += 0.01
        return optimalEpsilon

f = EpsilonGreedy(0.1, 9)
# print(f.optimizeEpsilon())

counts = []
rewards = []
maxIndex = []

#for i in range(10000):
#    counts.append((f.run_experiment(20)))
#    rewards.append(f.values)
#    maxIndex.append(f.maxIndex())
#    f.reset()
#print(maxIndex)
#print(f.maxIndexCounter(maxIndex))


# for i in range(20):
#     counts.append((f.select_arm()))
# print(counts)
