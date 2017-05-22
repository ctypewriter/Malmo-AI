




class Poro(object):
    def __init__(self, alpha = .3, gamma = 1, n = 1):
        """Constructing an RL agent.

                Args
                    alpha:  <float>  learning rate      (default = 0.3)
                    gamma:  <float>  value decay rate   (default = 1)
                    n:      <int>    number of back steps to update (default = 1)
                """
        self.epsilon = 0.1  # chance of taking a random action instead of the best
        self.q_table = {}
        self.n, self.gamma, self.alpha = n, alpha, gamma



    def run(self, agent):

        # TODO: Roll random number given the traits, picking an algorithm to run

        agent.sendCommand("move 1")


    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0



        # TODO add episilon agorithm

        return
