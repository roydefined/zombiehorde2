#!/usr/bin/env python3
import logging
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Find duplicate sprite frames in the projects that are merged into one pk3. ===

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

    # Contains the (sprite, frame, rotation) and their file paths.
    # A sprite lump is named TNT1A0 or TNT1A0A0: a 4 character name, then a frame letter and a rotation.
    # The optional second frame and rotation is the mirrored version of the same graphic.
    # Rotation 0 is for all rotations, then rotations 1 to 8 are stored so it gets caught too as a duplicate.
    frame_map: dict[tuple[str, str, str], list[Path]] = {}

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

            # Test lump length being either 6 or 8.
            # Unlike textures Zandronum doesn't cut them off, so just warn.
            lump_name = file_path.name.split(".", 1)[0].upper()
            if len(lump_name) not in (6, 8):
                logging.warning(f"Invalid sprite name: {file_path}")
                continue

            sprite = lump_name[:4]
            for frame, rotation in zip(lump_name[4::2], lump_name[5::2]):
                if rotation not in "012345678":
                    logging.warning(f"Invalid sprite rotation: {file_path}")
                    continue

                rotations = "12345678" if rotation == "0" else rotation
                for r in rotations:
                    paths = frame_map.setdefault((sprite, frame, r), [])
                    if file_path not in paths:
                        paths.append(file_path)

        logging.info("")

    # Group the clashes per sprite and frame, so each file is listed once.
    duplicates: dict[tuple[str, str], list[Path]] = {}
    for (sprite, frame, _), paths in frame_map.items():
        if len(paths) > 1:
            listed = duplicates.setdefault((sprite, frame), [])
            listed.extend(p for p in paths if p not in listed)

    # Report duplicates
    logging.info("=== Duplicate sprite frames ===")

    for (sprite, frame), paths in sorted(duplicates.items()):
        logging.info(f"Duplicate sprite frame: {sprite} {frame}")
        for p in paths:
            logging.info(f"  {p}")

    if not duplicates:
        logging.info("No duplicates found.")

    logging.info("Finished analysing.")


if __name__ == "__main__":
    main()
