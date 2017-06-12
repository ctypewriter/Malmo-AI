---
layout: default
title: Final Report
---


# EMBED VIDEO GOES HERE




## Project Summary
  The goal of our AI is to create a self-learning, pathfinding AI that uses continuous movement to make its way to a target location indicated by the diamond block in a Minecraft enviornment through Project Malmo. It is able to jump up hills and climb mountains to it's goal if neccessary, but also find quick and efficient paths towards the goal on flat land. The AI uses reinforcement learning (q-learning) to gradually learn an optimal policy/path to a goal.
  
  ![State Figure](https://raw.githubusercontent.com/ctypewriter/Poro-Pathfinder/master/docs/Goalpic.PNG)
  
  Reinforcement learning is used to reach the goal when LIMITED information is known about the enviorment due to hardware constraints, lack of knowledge, or saving on resources. While other known algorithms such as A* or Dijkstra's will have better perforcemance than the AI when the entire enviorment is known, this AI will outperform the mentioned algorithms in resource usage and scalability. The AI requires information about its immediate surroundings, coordinates of itself, and its goal, as opposed to the entire world. As a result, in enormous worlds where regular pathfinding algorithms would fail, this AI will still perform adequately.


## Approach
  The AI uses epislon greedy q-learning. Specifically, it creates a q-table in which for each state, lists the expected reward for each action that can be done in that state (Q(s, a) = expected reward). The rewards are initially 0 and the q-table is learned by randomly selecting actions in the beginning. As some q values change, the AI selects the highest q-value action in the current state a majority of the time (with 1-epsilon probabilty) and randomly chooses a random action with epsilon probablity. The q table is updated using the following formula.
  
    Q(s,a) = Q(s,a) + alpha( gamma( reward of a + q value of next action) - Q(s,a) )
  
  where gamma and alpha are user specified variables. Alpha affects how quickly Q values change and Gamma affects the weight of the current reward and expected reward.
  
  Our AI also uses a variable n which specifies how many actions in the future a q-value is affected by. (if n = 100, q(s,a) will be affected by the rewards of a(t+1), a(t+2), ..., a(t+100), and Q(s(t+100), a(t+100)). The equation is therefore:
  
    Q(s,a) = Q(s,a) + alpha( rewards + gamma^n(q value of nth action from current action) - Q(s,a) )
  
  where rewards is the sum from i =0, to i = n of gamma^i * reward(a(t+i)).
  
  Because of this, the AI is quickly able to learn which actions perform well given a current state. Within a few trials, the AI will realize which actions perform well and which do not, enabling it to quickly converage to an optimal policy.
  
  Epsilon greedy q-learning quickly converages to a good policy making it a good algorithm for this AI. However, epsilon greedy algorithms have a problem when a long serials of actions must be correct to reach the goal. For example, if an AI must travel straight 1000 units on a bridge towards a goal, an epsilon greedy algorithm that chooses a random action even 1% of the time will fail to reach the goal countless times, making the algorithm a poor choice for situations where percision is core. However, this is an edge case which the average minecraft player will not encounter frequently. As such, the AI will ignore such situations.
  
  ### States:

  Since q-learning learns optimal actions at each state, it is important to limit the number of states, enabling the AI to quickly converge towards the optimum policy. To do so, the AI uses 2 different pieces of information to determine its current state: The features of its immediate surrounding area, and its distance to the goal.

  The purpose of the AI's surrounding area is to determine the action space for the given state. It consists of the features of the 4 immediate surrounding blocks. Each of these blocks has a value of either drop, flat, hill, or wall. For example, when standing next to a wall, the AI is unable to walk into the wall as that would be pointless and a waste of time.
  
  Additionally, the surrounding area information also helps the AI learn how to interact with drops from cliffs. If the goal is on a mountain, the AI uses the surrounding area to learn that walking off cliffs results in poor returns, discourging the AI from such behavior in the future.
  
  The second and most important part of the state definition is a variable (N,E,S,W) that determines the general direction the goal is from the AI.
  
![State Figure](https://raw.githubusercontent.com/ctypewriter/Malmo-AI/master/docs/StateDemo.PNG)

  The above figure shows the approximation the AI uses to determine the general direction to the goal, depending on which quadrant the AI currently resides in. This means, for example, if the agent was to the south of the goal, the variable would be set as N (for North).  However, for example, if the agent was to the southeast of the goal, the variable would be set as W if the x-coordinate distance to the goal is bigger than the z-coordinate distance to the goal.  If the z-coordinate distance to the goal is bigger than the x-coordinate distance to the goal, the variable would be set as N.  

  This approximation is the core to the AI because it limits the state space, giving the AI just enough information to make its way to the goal, but not encumbering it with an excess number of states. By limiting the number of states, the AI is able to learn, and then recognize a few, specific situations, as opposed to learning optimal actions in every single tile of the world or some other unreasonable metric.

  As a result of these states, the AI is able to gradually take in information as it makes it way to the goal. At any given moment in time, the AI requires very little information, compare to other algorithms that must take the entire enviorment before calcuating a path to the goal. As such, this AI requires comparatively less resources in memory, but may require more calcuations as it must constantly evaluate states and update q values in the q table.
  
  ### Reward:

  The reward acts as both a rating of the AI as well as helping the AI learn ideal actions for each state. The way the reward is determined is by measuring the change in a straight line distance from the AI to the goal between actions. A negative constant (c) is then added on to the reward to teach the AI not to do stagnant actions (such as walking into a wall).

    Reward for an action = oldDistance from goal - newDistance from goal - c

  The AI also receives a reward for reaching its goal (touching its goal).

This reward scheme promotes actions that help the agent progress towards the goal, while punishing actions that distance the agent from the goal. The AI is thus able to quickly learn favorable actions while discrediting disfavorable actions. This also helps the AI learn that walking off cliffs when the goal is above is disfavorable, teaching the AI situational decision making.

### Tying It Together:

  Whenever the AI takes an action, it uses the reward gained or lost to rate the performance of the action, making it more likely to do the action in the future if the reward was positive. Conversely, actions that result in negative rewards are less likely to be done in the future. On top of this, the AI also rates the action based on the expected value of the next state/action pair, which propagates down to previous actions. Because of this, even though an action may have an immediate, negative reward, it may still be chosen in the future if the resulting state generally performs well. The AI learns from each action, which carries over from trial to trial, resulting in relatively consistant performance as trials progress.
  
  
