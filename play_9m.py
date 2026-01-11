import sys
import os

sys.path.append(os.getcwd())

import jax
import jax.numpy as jnp
import orbax.checkpoint
from src import transformer
from src import tokenizer

current_dir = os.getcwd()
print(current_dir)