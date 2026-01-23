import os

def load_config(filename="config.txt"):
    config = {}
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found. Using defaults.")
        return config
        
    with open(filename, "r") as f:
        for line in f:
            # Skip empty lines or comments
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config