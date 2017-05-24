

import sys
import time
from collections import deque
import random

class Poro(object):
    def __init__(self, destx, desty, destz, alpha=.3, gamma=1, n=1 ):
        """Constructing an RL agent.

                Args
                    alpha:  <float>  learning rate      (default = 0.3)
                    gamma:  <float>  value decay rate   (default = 1)
                    n:      <int>    number of back steps to update (default = 1)
                """
        self.epsilon = 0.1  # chance of taking a random action instead of the best
        self.q_table = {}
        self.n, self.gamma, self.alpha = n, alpha, gamma
        self.x, self.y, self.z = destx, desty, destz
    '''
    def init_dict(self):
        result = dict()
        result["Wall"] = None
        result["Jump"] = None
        result["Drop"] = None
        result["None"] = None
        result["Direction"] = None
        return result

    def direction_default(self):
        result = dict()
        result["N"] = False
        result["NE"] = False
        result["E"] = False
        result["SE"] = False
        result["S"] = False
        result["SW"] = False
        result["W"] = False
        result["NW"] = False
        return result
    
    def get_possible_actions(self, agent_host):


        return ["move 1", "move 0"] # TODO add more actions
    
    def direction_to_goal(self, curx, cury, curz):
        if curx == self.x:
            if curz > self.z:
                return "S"
            else:
                return "N"
        elif curz == self.z:
            if curx > self.x:
                return "W"
            else:
                return "E"
        else:
            if curx > self.x and curz > self.z:
                return "SE"
            elif curx > self.x and curz < self.z:
                return "NE"
            elif curx < self.x and curz > self.z:
                return "SW"
            else:
                return "NW"
            
    def is_wall(self, curx, curz):
        wall = self.direction_default()
        if curx == -29:
            if curz == -29:
                wall["NE"] = True
                wall["E"] = True
                wall["S"] = True
                wall["SE"] = True
                wall["SW"] = True
            elif curz == 29:
                wall["N"] = True
                wall["E"] = True
                wall["NE"] = True
                wall["NW"] = True
                wall["SE"] = True
            else:
                wall["E"] = True
                wall["NE"] = True
                wall["SE"] = True
                
        elif curx == 29:
            if curz == -29:
                wall["NW"] = True
                wall["W"] = True
                wall["S"] = True
                wall["SW"] = True
                wall["SE"] = True
            elif curz == 29:
                wall["W"] = True
                wall["N"] = True
                wall["NW"] = True
                wall["NE"] = True
                wall["SW"] = True
            else:
                wall["NW"] = True
                wall["W"] = True
                wall["SW"] = True

        elif curz == 29:
            wall["NW"] = True
            wall["N"] = True
            wall["NE"] = True

        elif curz == -29:
            wall["SW"] = True
            wall["S"] = True
            wall["SE"] = True
        return wall
    
    def get_curr_state(self, grid, curx, cury, curz): #TODO might have to pass agent_host or world state to get user location
        state = self.init_dict()
        state["Wall"] = self.is_wall(curx, curz)
        state["Direction"] = self.direction_to_goal(curx, cury, curz)
        return state
    '''
    
    def feature(self, blockA, blockB, blockC):
        if blockA == u'air' and blockB == u'air' and blockC == u'air':
            return 'drop'
        elif blockA != u'air' and blockB == u'air' and blockC == u'air':
            return 'flat'
        elif (blockA != u'air' and blockB != u'air' and blockC != u'air') or \
             (blockB == u'air' and blockC != u'air'):
            return 'wall'
        elif blockA != u'air' and blockB != u'air' and blockC == u'air':
            return 'hill'
        
    def get_curr_state(self, grid): #TODO might have to pass agent_host or world state to get user location
        # [N, E, W]
        state = [None for i in range(3)]
        state[0] = self.feature(grid[-1][7], grid[0][7], grid[1][7])
        state[1] = self.feature(grid[-1][4], grid[0][3], grid[1][3])
        state[2] = self.feature(grid[-1][5], grid[0][5], grid[1][5])
        print(state)

        return state
    
    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.

        Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
        """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def run(self, agent_host):

        # Learning process
        S, A, R = deque(), deque(), deque()
        done_update = False
        while not done_update:
            s0 = self.get_curr_state()
            possible_actions = self.get_possible_actions(agent_host)

            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)

            # Running the below code results in an infinite loop (or one too long to be useful) TODO inplement terminal State
            T = sys.maxint
            for t in xrange(sys.maxint):
                time.sleep(0.1) # TODO increase so actions are only chosen at a slower rate.
                if t < T:

                    # TODO, change below lines, act should not return reward, if terminal state, reward = 5000, else -1.
                    current_r = self.act(agent_host, A[-1])
                    R.append(current_r)

                    # TODO if in terminal state.
                        # T = t + 1
                        # S.append('Term State') #Append terminal state
                        # present_reward = current_r # Total reward
                        # print "Reward:", present_reward
                    #else: TODO
                    s = self.get_curr_state()
                    S.append(s)
                    possible_actions = self.get_possible_actions(agent_host)
                    next_a = self.choose_action(s, possible_actions, self.epsilon)
                    A.append(next_a)

                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break



        #agent_host.sendCommand("move 1")
        # time.sleep(1)
        # agent_host.sendCommand("move -1")
        # time.sleep(1)


    def choose_action(self, curr_state, possible_actions, eps):
        """Chooses an action according to eps-greedy policy. """

        # initialize state in q_table if needed
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0


        # Checks whether to do a random strategy or the optimal strategy currently found
        rnd = random.random()

        # With probablitiy 1-eps, populate the list of actions with only the highest q value actions
        if (rnd > self.epsilon):
            # sorts list of actions by highest q value
            action_q_value = sorted(self.q_table[curr_state].items(), key=lambda x: x[1], reverse=True)

            # Records highest q value
            highest_q = action_q_value[0][1]

            possible_actions = []

            # Populates list with highest q value actions
            for action in action_q_value:
                if action[1] == highest_q:
                    possible_actions.append(action[0])
                else:
                    break

        a = random.randint(0, len(possible_actions) - 1)

        return possible_actions[a]
