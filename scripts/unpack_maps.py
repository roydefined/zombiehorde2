#!/usr/bin/env python3
import logging
import sys
from pathlib import Path
from logger import setup_logging, get_log_level
from utils import get_root, run_cmd, mod_to_map_folder

# === Unpack maps from WAD files back into pk3/maps/ ===

def safe_delete(path: Path):
    try:
        path.unlink()
    except Exception:
        pass

def main():
    setup_logging(get_log_level())

    root = get_root()
    tool = root / "tools" / "Gdcc_x64" / "gdcc-ar-wad.exe"
    pk3root = root / "pk3"
    outroot = root / "pk3" / "maps"

    if not tool.exists():
        raise SystemExit(f'gdcc-ar-wad.exe not found at "{tool}"')

    if not pk3root.exists():
        raise SystemExit(f'Source directory "{pk3root}" does not exist.')

    logging.info(f'Searching for projects in "{pk3root}"...\n')

    # Projects inside src/
    for project_path in sorted(p for p in pk3root.iterdir() if p.is_dir()):
        project_name = project_path.name
        mapdir = project_path / "maps"

        if not mapdir.exists():
            logging.debug(f'Skipping "{project_name}". No "maps/" directory found.\n')
            continue

        logging.debug(f"[PROJECT] {project_name}")

        outdir = outroot / mod_to_map_folder(project_name)
        outdir.mkdir(parents=True, exist_ok=True)

        had_wads = False

        # Locate all .wad files
        for wad_file in mapdir.glob("*.wad"):
            if not wad_file.exists():
                continue

            had_wads = True
            #logging.info(f"Extracting {wad_file.name} -> {outdir}...")

            # Run extractor
            try:
                run_cmd([
                    str(tool),
                    f"wad:{wad_file}",
                    "--extract",
                    "-o", str(outdir)
                ])
            except SystemExit:
                logging.error(f"Failed to extract {wad_file.name}")
                continue
            else:
                logging.debug(f"Extracted {wad_file.name}")

            # Folder name inside maps is based on wad name
            mapfolder = outdir / wad_file.stem

            # Remove ENDMAP
            endmap = mapfolder / "ENDMAP"
            if endmap.exists():
                #logging.info(f"Removing ENDMAP from {mapfolder}...")
                safe_delete(endmap)

            # Remove level lump
            level_file = mapfolder / wad_file.stem
            if level_file.exists():
                #logging.info(f"Removing {wad_file.stem} from {mapfolder}...")
                safe_delete(level_file)

        if not had_wads:
            logging.warning(f'No .wad files found in "{mapdir}"')

        logging.debug("")

    # Cleanup BEHAVIOR lumps, passing on --verbose.
    logging.info("Deleting map behaviors...\n")
    run_cmd(["python", str(root / "scripts" / "delete_map_behaviors.py"), *sys.argv[1:]])
    logging.debug("")

    logging.info("All projects processed.")

if __name__ == "__main__":
    main()