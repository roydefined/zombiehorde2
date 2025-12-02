#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_root

# === Find duplicate texture names in all projects. ===

def main():
    setup_logging()

    root = get_root()
    srcroot = root / "src"

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    # The folders inside each project we want to scan.
    texture_folders = ["Flats", "Patches", "Textures"]

    # Contains the texture names without extension and their file paths.
    name_map: dict[str, list[Path]] = {}

    logging.info(f"Scanning projects in {srcroot}...")

    # Iterate each project folder.
    for project_path in sorted(p for p in srcroot.iterdir() if p.is_dir()):
        logging.info(f"[PROJECT] {project_path.name}")

        # Iterate the defined folders to scan.
        for folder_name in texture_folders:
            folder = project_path / folder_name
            if not folder.exists():
                continue

            # Include subfolders as well
            for file_path in folder.rglob("*.*"):
                if not file_path.is_file():
                    continue

                name_no_ext = file_path.stem

                if name_no_ext not in name_map:
                    name_map[name_no_ext] = []

                name_map[name_no_ext].append(file_path)

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

    logging.info("[DONE]")


if __name__ == "__main__":
    main()
