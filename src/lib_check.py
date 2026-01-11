import jax
import jax.numpy as jnp
import haiku as hk
import optax
import chex

print(f"JAX Version: {jax.__version__}")
print(f"Haiku Version: {hk.__version__}")
print(f"Optax Version: {optax.__version__}")

# Simple JAX test (Matrix Multiplication)
key = jax.random.PRNGKey(42)
x = jax.random.normal(key, (1000, 1000))

print(f"\nJAX Test: 1000x1000 Matrix Multiply result shape: {jnp.dot(x, x).shape}")
