#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Find files with the same path in the projects that are merged into one pk3. ===

def main():
    setup_logging()

    root = get_root()
    srcroot = root / "pk3"

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    # All merged together in builds.
    projects = [
        "libraries/ZombieHorde2Lib",
        "ZombieHorde2",
        "ZombieHorde2Doom",
        "ZombieHorde2Legacy",
        "ZombieHorde2Modern",
        "ZombieHorde2Resources",
    ]

    # Contains the paths relative to their project and their file paths.
    path_map: dict[str, list[Path]] = {}

    logging.info(f"Scanning projects in {srcroot}...")

    for project_name in projects:
        logging.info(f"Project: {project_name}")

        project_path = srcroot / project_name
        if not project_path.exists():
            continue

        # Include subfolders as well
        for file_path in project_path.rglob("*"):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(project_path).as_posix().lower()
            path_map.setdefault(relative_path, []).append(file_path)

        logging.info("")

    # Report duplicates
    logging.info("=== Duplicate lump paths ===")

    found_any = False
    for relative_path, paths in sorted(path_map.items()):
        if len(paths) > 1:
            found_any = True
            logging.info(f"Duplicate path: {relative_path}")
            for p in paths:
                logging.info(f"  {p}")

    if not found_any:
        logging.info("No duplicates found.")

    logging.info("Finished analysing.")

    if found_any:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
