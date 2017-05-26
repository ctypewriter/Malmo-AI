---
layout: default
title: Status
---

Video link goes HERE


## Project Summary
  The goal of our AI is to create a self-learning, pathfinding AI that uses continuous movement to make its way to a target location. It should be able to jump up hills and climb mountains to it's goal if neccessary, but also find quick and efficient paths towards the goal on flat land. The AI uses reinforment learning (q-learning) to gradually learn an optimal policy.

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
