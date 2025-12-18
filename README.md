# Chess_foehn

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Status](https://img.shields.io/badge/status-active%20development-orange)

## Project Overview

`chess_foehn` represents an experimental step in chess Transformers. Unlike traditional engines (Stockfish) that rely on Minimax/AlphaBeta search, or some RL approaches that view chess as isolated board states (FEN), this project treats chess as a **sequence modeling problem**. The goal is not to beat Stockfish at calculation depth, but to build an engine that plays with similar **human heuristics** or can conclude on some unfinded heuristics, making it ideal for speed time controls (Blitz/Bullet) where "intuition" of the position matters more than deepth.

## Architecture

### Sequence-Based Input (PGN over FEN)
Existing chess transformers evaluate a board state (FEN) as one input, which inherently makes them non-markovian. `chess_foehn` uses the power of Transformers to process **PGN** data.
* **Hypothesis:** A game of chess swings a lot between different states. By feeding the model the history of moves, it can understand the *flow* and *intent* behind a position, somewhat similar to how LLMs understand context in different texts. This also removes the complexity of additional curating of certain specific chess positions which is impossible to capture in FEN notations

### Architectural Upgrades
I am iterating on the architecture proposed by Ruoss et al. (2024) to better suit game positions, by small-scale architectural and data-notation changes  

## Features

* **Rule Integrity:** Built-in validation using `python-chess` ensures the model never hallucinates illegal moves. By employing PGN notations, the possibility of ignoring special game rules which depend on the history of the game is removed 
* **Searchless Play:** The model aims to output high-quality moves via direct inference rather than tree search
* **Human Heuristics:** By training on human games (possibiliy creative), the model learns to mimic human creativity and error patterns, avoiding the mate-in-23 like moves be the traditional engines
* **Exploring Fine-Tuning:** Exploration on the possibility of finetuning a specific style of chess a grandmaster plays based on their professional games

## Acknowledgments
This project is continuously getting inspired by the work of Ruoss et al. and their paper:

> Ruoss, A., Delétang, G., Medapati, S., Grau-Moya, J., Wenliang, L. K., Catt, E., ... & Genewein, T. (2024). *Amortized Planning with Large-Scale Transformers: A Case Study on Chess*. 38th Conference on Neural Information Processing Systems (NeurIPS 2024). arXiv preprint arXiv:2402.04494.

## 🛠️ Installation

```bash
# Clone the repository
git clone [https://github.com/SyedSiddiqShakir/chess_foehn.git](https://github.com/SyedSiddiqShakir/chess_foehn.git)
cd chess_foehn

# Install dependencies
pip install -r requirements.txt 