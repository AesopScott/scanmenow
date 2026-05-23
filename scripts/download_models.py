"""Download required spaCy models for scanmenow.

Run once after installing the package:
    uv run python scripts/download_models.py
"""

import subprocess
import sys


MODELS = [
    "en_core_web_lg",
]


def main() -> None:
    for model in MODELS:
        print(f"Downloading {model}...")
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", model],
            check=False,
        )
        if result.returncode != 0:
            print(f"  ERROR: failed to download {model}", file=sys.stderr)
            sys.exit(1)
        print(f"  OK: {model}")
    print("All models downloaded.")


if __name__ == "__main__":
    main()
