"""Generate a transparent SHA-256 manifest of the actual repository files."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "build", "dist", "__pycache__", ".pytest_cache",
             ".ruff_cache", ".mypy_cache", ".ipynb_checkpoints", "site", "outputs"}

def main():
    entries = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative == "REPOSITORY_MANIFEST.json" or relative.endswith(".pyc") or relative.endswith(".egg-info/PKG-INFO"):
            continue
        content = path.read_bytes()
        entries.append({"path": relative, "bytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest()})
    document = {"project": "Neural State Space Lab",
                "version": "0.9.0",
                "note": "Computed from files available during manifest generation; excludes this manifest itself.",
                "files": entries}
    (ROOT / "REPOSITORY_MANIFEST.json").write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {len(entries)} repository files")

if __name__ == "__main__":
    main()
