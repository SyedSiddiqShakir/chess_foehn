# chess_foehn
This is me trying my way with machine learning using my hobby, chess.  

## Idea
Instead of using images of boards or hard-coded engines like Stockfish, I’m feeding in raw **PGN and FEN files** (yep, those game logs with all the move information). The idea is simple:  
- Train a model that understands chess moves directly from PGNs
- It should never make illegal moves (coz rules are built-in, [Python-Chess](https://python-chess.readthedocs.io/en/latest/) helps)
- Try some pretraining tricks and forcing the model to guess them
- Seeing if a hybrid of transformer or Reinforcement learning works 
- Later: see if it can play fast games (like blitz/bullet) where intuition matters more than brute-force search

This isn’t about beating Stockfish-like engines (they are far too powerful).  
It’s more about exploring:  
- Can ML learn patterns & style from millions of human games better than traditional chess engines without any methodical bias?  
- Can it make creative, human-like moves?
- Can it move more like a human?, in contrast to the chess engines that make very illogical but accurate moves  

## Plans
- Explore the Searchless chess architecture
- Identify the bridges to RL
- What is the difference to AlphaZero?  
- Build a simple interface to play against the model

## Acknowledgments
This project is continuously getting inspired by the work of Ruoss et al. and their paper:

> Ruoss, A., Delétang, G., Medapati, S., Grau-Moya, J., Wenliang, L. K., Catt, E., ... & Genewein, T. (2024). *Amortized Planning with Large-Scale Transformers: A Case Study on Chess*. 38th Conference on Neural Information Processing Systems (NeurIPS 2024). arXiv preprint arXiv:2402.04494.