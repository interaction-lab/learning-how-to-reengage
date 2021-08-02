import algorithms.epsilon_greedy
import algorithms.epsilon_greedy_annealing
import algorithms.exp3
import algorithms.hedge
import algorithms.softmax
import algorithms.softmax_annealing
import algorithms.thompson_sampling
import algorithms.ucb1
import algorithms.ucb2

class Q_Agent():
    # Intialise
    def __init__(self, environment):
        self.environment = environment
        n_arms = len(self.environment.actions)
        epsilon = 0.1
        gamma = 0
        temperature = 0
        alpha_param = 0
        self.mab = algorithms.epsilon_greedy.EpsilonGreedy(epsilon, n_arms)
        self.mab = algorithms.epsilon_greedy_annealing.EpsilonGreedyAnnealing(n_arms)
        self.mab = algorithms.exp3.EXP3(gamma, n_arms)
        self.mab = algorithms.hedge.Hedge(temperature, n_arms)
        self.mab = algorithms.softmax.Softmax(temperature, n_arms)
        self.mab = algorithms.softmax_annealing.SoftmaxAnnealing(n_arms)
        self.mab = algorithms.thompson_sampling.ThompsonSampling(n_arms)
        self.mab = algorithms.ucb1.UCB1(n_arms)
        self.mab = algorithms.ucb2.UCB2(alpha_param, n_arms)
        # self.mab = EpsilonGreedy.EpsilonGreedy(epsilon, len(self.environment.actions))
        # self.mab = UCB1.UCB1(n_arms)
        # self.mab = ThompsonSampling.ThompsonSampling(n_arms)
        # self.mab = UCB2.UCB2(n_arms)

        # self.makeArmsDependent(3, 4, 5)

    # Returns an index of the availableActions array.
    def choose_action(self):
        return self.mab.select_arm()

    def update(self, arm, reward):
        self.mab.update(arm, reward)

    # def makeArmsDependent(self, *dependents):
    #     self.epsilonGreedy.makeArmsDependent(*dependents)