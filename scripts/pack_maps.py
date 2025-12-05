#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_root, run_cmd

# === Pack maps from mapsrc/ into .wad files ===
# Supports optional --no-source (to exclude the map sources).

def create_temp_file(path: Path) -> bool:
    if path.exists():
        return False
    path.write_bytes(b"")
    return True

def safe_delete(path: Path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass

def pack_single_map(tool: Path, map_path: Path, out_wad: Path,
                    map_name: str, include_scripts: bool):
    #logging.info(f"  Packing {map_name} -> {out_wad}...")

    # Temporary ENDMAP + MAP_NAME lumps
    tmp_endmap = create_temp_file(map_path / "ENDMAP")
    tmp_level = create_temp_file(map_path / map_name)

    args = [
        str(tool),
        f"file:{map_path / map_name}",
        f"file:{map_path / 'TEXTMAP'}",
        f"file:{map_path / 'BEHAVIOR'}",
        f"file:{map_path / 'ZNODES'}"
    ]

    if include_scripts:
        args.append(f"file:{map_path / 'SCRIPTS'}")

    args.append(f"file:{map_path / 'ENDMAP'}")
    args += ["-o", str(out_wad)]

    try:
        run_cmd(args)
    except SystemExit:
        logging.error(f"  [FAIL] Failed to pack {map_name}")
    else:
        logging.info(f"  [OK] Packed {map_name}")
    finally:
        if tmp_endmap:
            safe_delete(map_path / "ENDMAP")
        if tmp_level:
            safe_delete(map_path / map_name)


def main():
    setup_logging()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-source", action="store_true")
    args = parser.parse_args()

    include_scripts = not args.no_source

    root = get_root()
    tool = root / "tools" / "Gdcc_x64" / "gdcc-ar-wad.exe"
    mapsrc = root / "mapsrc"
    outroot = root / "src"

    if not tool.exists():
        raise SystemExit(f'[ERROR] gdcc-ar-wad.exe not found at "{tool}"')

    if not mapsrc.exists():
        raise SystemExit(f'[ERROR] Source directory "{mapsrc}" does not exist.')

    # Compile maps first
    logging.info("Compiling maps...\n")
    run_cmd(["python", str(root / "scripts" / "compile_maps.py")])
    logging.info("")

    logging.info(f'Packing projects from "{mapsrc}"...')

    # Iterate project folders
    for project_path in sorted(p for p in mapsrc.iterdir() if p.is_dir()):
        project_name = project_path.name
        outdir = outroot / project_name / "maps"
        outdir.mkdir(parents=True, exist_ok=True)

        logging.info(f"[PROJECT] {project_name}")

        # Iterate maps inside project
        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            map_name = map_path.name
            out_wad = outdir / f"{map_name}.wad"

            pack_single_map(tool, map_path, out_wad, map_name, include_scripts)

        logging.info("")

    # Cleanup BEHAVIOR lumps
    logging.info("Deleting map behaviors...\n")
    run_cmd(["python", str(root / "scripts" / "delete_map_behaviors.py")])
    logging.info("")

    logging.info("[DONE] All projects packed successfully.")


if __name__ == "__main__":
    main()
