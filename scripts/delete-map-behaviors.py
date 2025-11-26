#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_root

# === Remove BEHAVIOR lumps ===
# This script removes all compiled BEHAVIOR lumps from every map under `mapsrc/`.

def main():
    setup_logging()

    root = get_root()
    mapsrc = root / "mapsrc"

    if not mapsrc.exists():
        raise SystemExit(f'[ERROR] Source directory "{mapsrc}" does not exist.')

    logging.info(f'Cleaning BEHAVIOR lumps from "{mapsrc}"...')
    logging.info("")

    # Iterate project folders
    for project_path in sorted(p for p in mapsrc.iterdir() if p.is_dir()):
        project_name = project_path.name
        logging.info(f"[PROJECT] {project_name}")

        # Iterate maps inside project
        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            map_name = map_path.name
            behavior_file = map_path / "BEHAVIOR"

            if behavior_file.exists():
                #logging.info(f"  Deleting BEHAVIOR for {map_name}...")
                try:
                    behavior_file.unlink()
                except Exception:
                    logging.error(f"  [FAIL] Failed to delete BEHAVIOR for {map_name}")
                else:
                    if behavior_file.exists():
                        logging.error(f"  [FAIL] Failed to delete BEHAVIOR for {map_name}")
                    else:
                        logging.info(f"  [OK] Deleted BEHAVIOR for {map_name}")
            else:
                logging.info(f"  [SKIP] {map_name} has no BEHAVIOR lump")

        logging.info("")

    logging.info("[DONE] All BEHAVIOR lumps removed.")


if __name__ == "__main__":
    main()
