from pathlib import Path

for item in Path("data").glob("**/*"):
    if item.suffix == ".idx":
        item.unlink()
