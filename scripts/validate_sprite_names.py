#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Find sprite files with an invalid lump name in the projects that are merged into one pk3. ===

# Frame letters A to Z, and `[`, `\` and `]` which is also valid.
VALID_FRAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]"

# Rotation 0 is for all rotations, otherwise 1 to 8.
VALID_ROTATIONS = "012345678"

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

    # A sprite lump is named TNT1A0 or TNT1A0A0: a 4 character name, then a frame letter and a rotation.
    # The optional second frame and rotation is the mirrored version of the same graphic.
    # Unlike textures Zandronum doesn't cut the name off, so it has to be exactly 6 or 8 characters of printable ASCII.
    found_any = False

    logging.info(f"Scanning projects in {srcroot}...")

    for project_name in projects:
        logging.info(f"Project: {project_name}")

        folder = srcroot / project_name / "sprites"
        if not folder.exists():
            continue

        # Include subfolders as well
        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue

            lump_name = file_path.name.split(".", 1)[0].upper()
            if not all("!" <= c <= "~" for c in lump_name):
                found_any = True
                logging.warning(f"Not printable ASCII: {file_path}")
            elif len(lump_name) not in (6, 8):
                found_any = True
                logging.warning(f"Not 6 or 8 characters: {file_path}")
            elif any(f not in VALID_FRAMES for f in lump_name[4::2]):
                found_any = True
                logging.warning(f"Invalid frame letter: {file_path}")
            elif any(r not in VALID_ROTATIONS for r in lump_name[5::2]):
                found_any = True
                logging.warning(f"Invalid rotation: {file_path}")

        logging.info("")

    if not found_any:
        logging.info("No invalid names found.")

    logging.info("Finished analysing.")


if __name__ == "__main__":
    main()
