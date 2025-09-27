# chess_foehn
This is me trying my way with machine learning using my hobby, chess.  

## Idea
Instead of using images of boards or hard-coded engines like Stockfish, I’m feeding in raw **PGN files** (yep, those game logs with all the move information). The idea is simple:  
- Train a model that understands chess moves directly from PGNs.  
- It should never make illegal moves (coz rules are built-in, [Python-Chess](https://python-chess.readthedocs.io/en/latest/) helps).  
- Try some pretraining tricks and forcing the model to guess them.  
- Later: see if it can play fast games (like blitz/bullet) where intuition matters more than brute-force search.  

This isn’t about beating Stockfish-like engines (they are far too powerful).  
It’s more about exploring:  
- Can ML learn patterns & style from millions of human games better than traditional chess engines without any methodical bias?  
- Can it make creative, human-like moves?
- Can it move more like a human?, in contrast to the chess engines that make very illogical but accurate moves  

## Plans
- Pretrain on large PGN dataset.  
- Build a simple interface to play against the model.