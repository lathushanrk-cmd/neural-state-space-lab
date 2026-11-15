"""Reproduce four synthetic figures, including regression-to-the-mean trap."""
from nssl.demo import generate
if __name__ == "__main__":
    print(*generate("assets"), sep="\n")
