---
layout: default
title: Final Report
---


EMBED VIDEO GOES HERE




## Project Summary
  The goal of our AI is to create a self-learning, pathfinding AI that uses continuous movement to make its way to a target location indicated by the diamond block. It is able to jump up hills and climb mountains to it's goal if neccessary, but also find quick and efficient paths towards the goal on flat land. The AI uses reinforcement learning (q-learning) to gradually learn an optimal policy/path to a goal.
  
  ![State Figure](https://raw.githubusercontent.com/ctypewriter/Poro-Pathfinder/master/docs/Goalpic.PNG)
  
  Reinforcement learning is used to reach the goal when LIMITED information is known about the enviorment due to hardware constraints, lack of knowledge, or saving on resources. While other known algorithms such as A* or Dijkstra's will have better perforcemance than the AI when the entire enviorment is known, this AI will outperform the mentioned algorithms in resource usage and scalability. The AI requires information about it's immediate surroundings, coordinates of itself, and its goal, as opposed to the entire world. As a result, in enormous worlds where regular pathfinding algorithms would fail, this AI will still perform adequately.


