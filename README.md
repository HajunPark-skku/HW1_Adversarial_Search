# AI HW1 - Adversarial Search

## Project Description

This project implements a simple adversarial board game environment and several agents for playing the game.

The implemented agents are:

* RandomAgent
* NoisyHeuristicAgent
* AlphaBetaAgent

The AlphaBetaAgent uses depth-limited alpha-beta pruning with an evaluation function.

---

## Files

### game.py

Contains the Game class and all game-related logic.

Implemented functions include:

* board initialization
* move validation
* legal move generation
* making moves
* checking winner
* checking terminal state
* copying game states
* board printing
* switching current player

### agents.py

Contains the implementations of:

* RandomAgent
* NoisyHeuristicAgent
* AlphaBetaAgent

### main.py

Runs one game or multiple experiments between different agents.

---

## Requirements

* Python 3.x
* No external packages are required

---

## Run

Run the program with:

```bash
python3 main.py
```

---

## Experiments

The following experiments are included in main.py:

1. AlphaBetaAgent vs RandomAgent
2. AlphaBetaAgent vs NoisyHeuristicAgent

For each experiment, the program reports:

* number of wins
* number of losses
* number of draws
* average computation time
* average expanded nodes
* average game length

---

## Agent Descriptions

### RandomAgent

Chooses a move randomly from all legal moves.

### NoisyHeuristicAgent

Uses simple heuristics:

* immediate winning move
* blocking opponent winning move
* center preference
* random action with probability epsilon

### AlphaBetaAgent

Uses:

* alpha-beta pruning
* depth-limited minimax search
* heuristic evaluation function
* terminal state evaluation
* time limit handling

The evaluation function considers:

* center control
* possible 4-cell lines
* offensive opportunities
* defensive blocking
