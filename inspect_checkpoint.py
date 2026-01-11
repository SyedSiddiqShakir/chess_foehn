import sys
import os
import orbax.checkpoint
import jax

my_path = os.path.join(os.getcwd(), 'checkpoints', '9M')

print(f"JAX version{jax.__version__}")
print(f"devices {jax.devices()}")
print(f"Backend{jax.default_backend()}")

def inspect_shapes():
    if not os.path.exists(my_path):
        print("path not exists")
    checkpointer = orbax.checkpoint.PyTreeCheckpointer()
    raw_data = checkpointer.restore(my_path)
    try:
        att_shape = raw_data['params']['MultiHeadDotProductAttention_0']['key']['kernel'].shape
        print(f"{att_shape}")
    
    except:
        print("att kernel not exists")

    #2 check hidden layer
    try:
        dense_shape = raw_data['params']['Dense_0']['kernel'].shape
        print(f"{dense_shape}")

    except:
        print("cant find dense kernel")
if __name__ == '__main__':
    inspect_shapes()