import sys
import time
from collections import deque
import math
import json
import random

actions = ["move 1", "move -1", "jump 1", "strafe 1", "strafe -1"]


class Poro(object):
    def __init__(self, destx, desty, destz, alpha=1, gamma=.5, n=5 ):
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
        self.currX, self.currY, self.currZ = 0, 0, 0 # Agent's current position, will be overwritten when program runs
    
    def get_possible_actions(self, agent_host):

        return actions

    # Returns one of 4 directions, choosing direction AI needs to travel the most
    def direction_to_goal(self, curx, curz):

        if math.fabs(curz - self.z) >= math.fabs(curx - self.x):
            if curz > self.z:
                return "S"
            else:
                return "N"
        elif math.fabs(curz - self.z) < math.fabs(curx - self.x):
            if curx > self.x:
                return "E"
            else:
                return "W"

    
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
        
    def get_curr_state(self, agent_host):
        # [N, E, W, Goal_Direction, yaw]

        pos = self.get_position_and_yaw(agent_host, agent_host.getWorldState())
        grid = self.load_grid(agent_host, agent_host.getWorldState())

        state = [None for i in range(5)]
        world_state = agent_host.getWorldState()

        if (world_state.is_mission_running):
            state[0] = self.feature(grid[-1][7], grid[0][7], grid[1][7])
            state[1] = self.feature(grid[-1][4], grid[0][3], grid[1][3])
            state[2] = self.feature(grid[-1][5], grid[0][5], grid[1][5])
            state[3] = self.direction_to_goal(pos[0], pos[2])
            state[4] = pos[3]

        return tuple(state)
    
    def load_grid(self, agent_host, world_state):
        """
        Used the agent observation API to get a 21 X 21 grid box around the agent (the agent is in the middle).

        Args
            world_state:    <object>    current agent world state

        Returns
            grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
        """
        grid = dict()
        while world_state.is_mission_running:
            world_state = agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                grid[-1] = observations.get(u'floor-1', 0)
                grid[0] = observations.get(u'floor0', 0)
                grid[1] = observations.get(u'floor1', 0)
                break
        return grid

    def get_position_and_yaw(self, agent_host, world_state):
        pos = ()
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            world_state = agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')

            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                observations = json.loads(msg)
                #grid = observations.get(u'floorAround', 0)
                break
        try:
            pos = tuple((math.floor(observations.get(u'XPos', 0)), \
                         math.floor(observations.get(u'YPos', 0)), \
                         math.floor(observations.get(u'ZPos', 0)), \
                         observations.get(u'Yaw', 0)))
            self.currX = observations.get(u'XPos', 0)
            self.currY = observations.get(u'YPos', 0)
            self.currZ = observations.get(u'ZPos', 0)

        except:
            pass
        return pos
    
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

        # Prevent mission end mid get_state call from being added to q_table
        if None in curr_s:
            return

        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def run(self, agent_host):
        # Learning process
        # Initialize Queues
        S, A, R = deque(), deque(), deque()
        reward = 0
        done_update = False
        while not done_update:
            # Get beginning state/action
            s0 = self.get_curr_state(agent_host)
            possible_actions = self.get_possible_actions(agent_host)

            a0 = self.choose_action(s0, possible_actions, self.epsilon)
            S.append(s0)
            A.append(a0)
            R.append(0)

            # Running the below code results in an infinite loop (or one too long to be useful) TODO inplement terminal State
            T = sys.maxint
            for t in xrange(sys.maxint):
                if t < T:

                    # Act
                    current_r = self.act(agent_host, A[-1])


                    # Terminal State check
                    world_state = agent_host.getWorldState()
                    if (math.fabs(self.currX - self.x) < 2 and math.fabs(self.currY - self.y) < 2 and math.fabs(self.currZ - self.z) < 2):
                        T = t + 1
                        S.append('Term State')

                        R.append(1000)
                        reward = reward + 1000

                        # present_reward = current_r # Total reward
                        # print "Reward:", present_reward
                    # Mission failed state
                    elif not world_state.is_mission_running:
                        T = t + 1
                        S.append('Fail State')

                        R.append(-math.fabs(self.currX - self.x) - math.fabs(self.currY - self.y) - math.fabs(self.currZ - self.z))
                        reward = reward - math.fabs(self.currX - self.x) - math.fabs(self.currY - self.y) - math.fabs(self.currZ - self.z)
                    # Continue taking actions
                    else:
                        # Reward is the x + y + z distance from the goal
                        R.append(-math.fabs(self.currX - self.x) - math.fabs(self.currY - self.y) - math.fabs(self.currZ - self.z))
                        reward += -math.fabs(self.currX - self.x) - math.fabs(self.currY - self.y) - math.fabs(self.currZ - self.z)
                        s = self.get_curr_state(agent_host)

                        S.append(s)
                        possible_actions = self.get_possible_actions(agent_host)
                        next_a = self.choose_action(s, possible_actions, self.epsilon)
                        A.append(next_a)


                # Update value tau = current t, n steps back, in the q table (ie if t = 10, n = 3, update the 7th action based on rewards from 8th 9th 10th actions)
                tau = t - self.n + 1
                if tau >= 0:
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break

        print "Reward is : ", reward
        print "Q-table is : ", self.q_table


    def act(self, agent_host, action):

        # If moving forward/backward, stop strafing, if strafing, stop moving back/forward
        if action == "move 1" or action == "move -1":
            agent_host.sendCommand("strafe 0")
        elif action == "strafe 1" or action == "strafe -1":
            agent_host.sendCommand("move 0")

        agent_host.sendCommand(action)
        time.sleep(.1)

        # Prevent ai from being jump happy
        agent_host.sendCommand("jump 0")
        time.sleep(.5) # Let action resolve/ AI land

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
