#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Find texture files with an invalid lump name in all projects. ===

def main():
    setup_logging()

    root = get_root()
    srcroot = root / "pk3"

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    # The folders inside each project we want to scan.
    texture_folders = ["Flats", "Patches", "Textures"]

    # The engine names a lump after the file name up to the first dot and only uses the first 8 characters.
    # A valid name is at most 8 characters of printable ASCII (no spaces).
    found_any = False

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

                lump_name = file_path.name.split(".", 1)[0]
                if not all("!" <= c <= "~" for c in lump_name):
                    found_any = True
                    logging.warning(f"Not printable ASCII: {file_path}")
                elif len(lump_name) > 8:
                    found_any = True
                    logging.warning(f"Longer than 8 characters, used as {lump_name[:8].upper()}: {file_path}")

        logging.info("")

    if not found_any:
        logging.info("No invalid names found.")

    logging.info("Finished analysing.")

    if found_any:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
