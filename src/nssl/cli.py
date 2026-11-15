"""Command line entry point generating verified synthetic demonstration assets."""
import argparse
from pathlib import Path
from .validation import validate_known_systems

def main():
    parser = argparse.ArgumentParser(description="Run and plot NSSL's explicitly synthetic demo")
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    from .demo import generate
    result = generate(args.output)
    print("Synthetic validation:", validate_known_systems())
    print("Generated files:", *(str(p) for p in result), sep="\n - ")

if __name__ == "__main__":
    main()
