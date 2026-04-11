#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Remove map editor files ===
# Deletes Doombuilder map artifacts:
# - *.dbs
# - *.backup<NUMBER>   (e.g. .backup1, .backup12)
# - *.autosave<NUMBER> (e.g. .autosave1, .autosave42)
# Note this script DOES ensure that the extension has a number suffix after it in case of renames.

def _has_numeric_suffix_extension(path: Path, prefix: str) -> bool:
    suffix = path.suffix
    if not suffix.startswith(f".{prefix}"):
        return False

    remainder = suffix[len(f".{prefix}"):]
    return remainder.isdigit()


def main():
    setup_logging()

    root = get_root()
    pk3root = root / "pk3"

    if not pk3root.exists():
        raise SystemExit(f'[ERROR] Source directory "{pk3root}" does not exist.')

    logging.info(f'Cleaning map editor files in "{pk3root}"...')

    # Loop all projects in the source.
    for project_path in sorted(p for p in pk3root.iterdir() if p.is_dir()):
        project_name = project_path.name
        mapdir = project_path / "maps"

        if not mapdir.exists():
            logging.info(f'Skipping "{project_name}". No "maps/" directory found.\n')
            continue

        logging.info(f"Project: {project_name}")

        # Remove *.dbs
        for dbs_file in mapdir.glob("*.dbs"):
            logging.info(f'Deleting "{dbs_file.name}"...')
            try:
                dbs_file.unlink()
            except Exception:
                logging.error(f'Could not delete "{dbs_file.name}"')

        # Remove *.backup<NUMBER> and *.autosave<NUMBER>
        for candidate in mapdir.iterdir():
            if not candidate.is_file():
                continue

            if _has_numeric_suffix_extension(candidate, "backup") or _has_numeric_suffix_extension(candidate, "autosave"):
                logging.info(f'Deleting "{candidate.name}"...')
                try:
                    candidate.unlink()
                except Exception:
                    logging.error(f'Could not delete "{candidate.name}"')

        logging.info("")

    logging.info("All map editor files cleaned.")


if __name__ == "__main__":
    main()