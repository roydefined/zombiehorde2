#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_root, run_cmd

# === Unpack maps from WAD files back into mapsrc/ ===

def safe_delete(path: Path):
    try:
        path.unlink()
    except Exception:
        pass

def main():
    setup_logging()

    root = get_root()
    tool = root / "tools" / "Gdcc_x64" / "gdcc-ar-wad.exe"
    srcroot = root / "src"
    outroot = root / "mapsrc"

    if not tool.exists():
        raise SystemExit(f'[ERROR] gdcc-ar-wad.exe not found at "{tool}"')

    if not srcroot.exists():
        raise SystemExit(f'[ERROR] Source directory "{srcroot}" does not exist.')

    logging.info(f'Searching for projects in "{srcroot}"...\n')

    # Projects inside src/
    for project_path in sorted(p for p in srcroot.iterdir() if p.is_dir()):
        project_name = project_path.name
        mapdir = project_path / "maps"

        if not mapdir.exists():
            logging.info(f'[INFO] Skipping "{project_name}". No "maps/" directory found.\n')
            continue

        logging.info(f"[PROJECT] {project_name}")

        outdir = outroot / project_name
        outdir.mkdir(parents=True, exist_ok=True)

        had_wads = False

        # Locate all .wad files
        for wad_file in mapdir.glob("*.wad"):
            if not wad_file.exists():
                continue

            had_wads = True
            #logging.info(f"  Extracting {wad_file.name} -> {outdir}...")

            # Run extractor
            try:
                run_cmd([
                    str(tool),
                    f"wad:{wad_file}",
                    "--extract",
                    "-o", str(outdir)
                ])
            except SystemExit:
                logging.error(f"  [FAIL] Failed to extract {wad_file.name}")
                continue
            else:
                logging.info(f"  [OK] Extracted {wad_file.name}")

            # Folder name inside mapsrc is based on wad name
            mapfolder = outdir / wad_file.stem

            # Remove ENDMAP
            endmap = mapfolder / "ENDMAP"
            if endmap.exists():
                #logging.info(f"    Removing ENDMAP from {mapfolder}...")
                safe_delete(endmap)

            # Remove level lump
            level_file = mapfolder / wad_file.stem
            if level_file.exists():
                #logging.info(f"    Removing {wad_file.stem} from {mapfolder}...")
                safe_delete(level_file)

        if not had_wads:
            logging.info(f"  [WARN] No .wad files found in {mapdir}")

        logging.info("")

    logging.info("[DONE] All projects processed.")


if __name__ == "__main__":
    main()
