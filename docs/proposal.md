---
layout: default
title: Proposal
---

## Summary
  This project aims to create an AI whose purpose is to get from one point to another as quickly as possible while also avoiding any possible dangers including monsters, terrain, and other sources of damage. As input, it shall take destination coordinates and information on its immediate surroundings such as the surrounding tile information and possible threats. Ideally, the learned AI will obtain high performance not only in the test enviorment, but also any other normal situations that a regular player may experience.

## Algorithms
  The current plan is to explore genetic algorithms, possibly with the help of neural networks. If that becomes impractical, reinforcement is also a possibility. 
  
## Evaluation Plan
  The AI's performance or fitness will be determined based on it's ability to reach the target coordinates, the time it takes to arrive, and any damage it may have taken in the process. At the very minimum, it must be able to traverse multiple elevations and terrain obstacles (lava, pitfalls), but ideally it will be able to avoid (and possibly remove) a large number of monsters on its way to the target. Genetic algorithms are expected to perform quite well with enough generations, but the limits are not yet known.
  The plan is to record the distinct different generations of the algorithm to show that the algorithm is indeed inheriting positive traits from the population while remove negative traits. The beginning generations are expected to be abyssmal, and as "natural" selection occurs, the future generations will perforce considerably better. 
  
  
