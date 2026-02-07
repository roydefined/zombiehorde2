#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_root

# === Remove map editor files ===
# Deletes Doombuilder map artifacts:
# - *.dbs
# - *.backup1 / *.backup2 / *.backup3

def main():
    setup_logging()

    root = get_root()
    srcroot = root / "src"

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    logging.info(f'Cleaning map editor files in "{srcroot}"...')

    # Loop all projects in the source.
    for project_path in sorted(p for p in srcroot.iterdir() if p.is_dir()):
        project_name = project_path.name
        mapdir = project_path / "maps"

        if not mapdir.exists():
            logging.info(f'[INFO] Skipping "{project_name}". No "maps/" directory found.\n')
            continue

        logging.info(f"[PROJECT] {project_name}")

        # Remove *.dbs
        for dbs_file in mapdir.glob("*.dbs"):
            logging.info(f'  Deleting "{dbs_file.name}"...')
            try:
                dbs_file.unlink()
            except Exception:
                logging.error(f'  [FAIL] Could not delete "{dbs_file.name}"')

        # Remove *.backup1/2/3
        for ext in ("*.backup1", "*.backup2", "*.backup3"):
            for backup_file in mapdir.glob(ext):
                logging.info(f'  Deleting "{backup_file.name}"...')
                try:
                    backup_file.unlink()
                except Exception:
                    logging.error(f'  [FAIL] Could not delete "{backup_file.name}"')

        logging.info("")

    logging.info("[DONE] All map editor files cleaned.")


if __name__ == "__main__":
    main()
