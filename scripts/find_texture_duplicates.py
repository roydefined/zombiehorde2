#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Find duplicate texture names in all projects. ===

def main():
    setup_logging()

    root = get_root()
    srcroot = root / "pk3"

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    # The folders inside each project we want to scan.
    texture_folders = ["Flats", "Patches", "Textures"]

    # Contains the texture names without extension and their file paths.
    name_map: dict[str, list[Path]] = {}

    logging.info(f"Scanning projects in {srcroot}...")

    # Iterate each project folder.
    for project_path in sorted(p for p in srcroot.iterdir() if p.is_dir()):
        logging.info(f"Project: {project_path.name}")

        # Iterate the defined folders to scan.
        for folder_name in texture_folders:
            folder = project_path / folder_name
            if not folder.exists():
                continue

            # Include subfolders as well
            for file_path in folder.rglob("*"):
                if not file_path.is_file():
                    continue

                name_no_ext = file_path.stem.lower()
                name_map.setdefault(name_no_ext, []).append(file_path)

        logging.info("")

    # Report duplicates
    logging.info("=== Duplicate texture names ===")

    found_any = False
    for name, paths in sorted(name_map.items()):
        if len(paths) > 1:
            found_any = True
            logging.info(f"Duplicate name: {name}")
            for p in paths:
                logging.info(f"  {p}")

    if not found_any:
        logging.info("No duplicates found.")

    logging.info("Finished analysing.")


if __name__ == "__main__":
    main()
