"""Reproduce deterministic synthetic hero and companion figures."""
from nssl.demo import generate
if __name__ == "__main__":
    print(*generate("assets"), sep="\n")
