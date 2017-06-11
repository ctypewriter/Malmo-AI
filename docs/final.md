---
layout: default
title: Final Report
---


EMBED VIDEO GOES HERE




## Project Summary
  The goal of our AI is to create a self-learning, pathfinding AI that uses continuous movement to make its way to a target location indicated by the diamond block. It is able to jump up hills and climb mountains to it's goal if neccessary, but also find quick and efficient paths towards the goal on flat land. The AI uses reinforment learning (q-learning) to gradually learn an optimal policy/path to a goal.
  
  ![State Figure](https://raw.githubusercontent.com/ctypewriter/Poro-Pathfinder/master/docs/Goalpic.PNG)
  
  The AI is to have reasonable performance, but not to the same level as A* or even dijkstra's algorithm. However, this AI will outperform the mentioned Algorithms in memory constraints and scalability. It only requires its immediate surroundings, coordinates of itself, and its goal, as opposed to the entire world. As a result, in endless worlds where regular pathfinding algorithms would fail, this AI will still perform adequately.
