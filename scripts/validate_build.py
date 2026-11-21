#!/usr/bin/env python3
import logging
import subprocess
import sys
from pathlib import Path
from logger import setup_logging

# === Run all validation tools and report which ones failed. ===

# Tools run in order for validation.
TOOLS = [
    "find_lump_path_duplicates.py",
    "find_texture_duplicates.py",
    "find_sprite_duplicates.py",
    "validate_texture_names.py",
    "validate_sprite_names.py",
]

def main():
    setup_logging()

    scripts_dir = Path(__file__).resolve().parent

    failed = []
    for tool in TOOLS:
        logging.info(f"=== Running {tool} ===")
        result = subprocess.run([sys.executable, str(scripts_dir / tool)], cwd=scripts_dir)
        if result.returncode != 0:
            failed.append(tool)
        logging.info("")

    logging.info("=== Validation summary ===")
    for tool in TOOLS:
        logging.info(f"{'FAILED' if tool in failed else 'OK'}: {tool}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
