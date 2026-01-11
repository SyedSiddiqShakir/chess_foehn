import os

file_path = os.path.join(
    os.getcwd(),
    "searchless_chess", "src", "training_utils.py"
)
print(f"patch file {file_path}")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_text = "jax.sharding.PositionalSharding"
    new_text = "jax.sharding.Sharding"

    if old_text in content:
        new_content = content.replace(old_text, new_text)

        with open(file_path, "w", encoding="utf-8") as f2:
            f2.write(new_content)
    else:
        print("check manually")
        
except FileNotFoundError:
    print("file not found")
