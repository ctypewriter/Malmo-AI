---
layout: default
title: Status
---

Video link goes HERE


## Project Summary
  The goal of our AI is to create a self-learning, pathfinding AI that uses continuous movement to make its way to a target location. It should be able to jump up hills and climb mountains to it's goal if neccessary, but also find quick and efficient paths towards the goal on flat land. The AI uses reinforment learning (q-learning) to gradually learn an optimal policy.
  
  The AI is to have reasonable performance, but not to the same level as A* or even dijkstra's algorithm. However, this AI will outperform the mentioned Algorithms in memory constraints and scalability. It only requires it's immediate surroundings, cordinates of itself, and it's goal, as opposed to the entire world. As a result, in huge, endless worlds where regular pathfinding algorithms would fail, this AI will still perform adequately.

## Approach
  The AI uses q-learning, specifically, it creates a q-table which for each state, lists the expected reward for each action that can be done in that state. The rewards are initially 0 and the q-table is learned through randomly selecting actions in the beginning. As some q values change, the AI selects the highest q-value action in the current state a majority of the time (1-epsilon probabilty) and randomly chooses a random action with epsilon probablity. The q table is updated using the following formula in the case where future actions do not propagate down and affect the currect q value.
  
    Q(s,a) = Q(s,a) + alpha( gamma( previous reward + q value of next action) - Q(s,a) )
  
  where gamma and alpha are user specified variables. Alpha affects how quickly Q values change and Gamma affects the weight of the current reward and expected reward.
  
  Our AI also uses a variable n which specifies how many actions in the future a q-value is affected by. (if n = 100, q(s,a) will be affected by the rewards of a(t+1), a(t+2), ..., a(t+100), and Q(s(t+100), a(t+100)). The equation is therefore:
  
    Q(s,a) = Q(s,a) + alpha( rewards + gamma^n(q value of nth action from current action) - Q(s,a) )
  
  where rewards is the sum from i =0, to i = n of gamma^i * reward(a(t+i)).


States:

  The states of this AI can be split into 2 distinct parts. The first is the features of the 4 adjacent blocks. Each of these blocks can have a value of (drop, flat, hill, wall). This is mainly to help the AI figure out how to move up and down elevations. As the demo current does not contain any hills or mountains, this part mainly serves as a placeholder.
  
  The second and most important part of the state definition is a variable (N,E,S,W) that determines the general direction the goal is from the AI.
  
![State Figure](https://raw.githubusercontent.com/ctypewriter/Malmo-AI/master/docs/StateDemo.PNG)
The above figure shows the approximation the AI uses to determine the general direction to the goal, depending on which quadrant the AI current resides in. This approximation is core to the AI because it limits the state space, giving the AI just enough information to make its way to the goal, but not encumbering it with an excess number of states. By limiting the number of states, the AI is able to learn, and then recognize a few, specific situations, as opposed to learning optimal actions in every single tile of the world or some other unreasonable metric.
