#!/usr/bin/env python3
import logging
import subprocess
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Compile ACS SCRIPTS into BEHAVIOR lumps ===
# Compiles the SCRIPTS file in each map into a BEHAVIOR lump.

def main():
    setup_logging()

    root = get_root()
    bcc = root / "tools" / "Zt-bcc_x86" / "zt-bcc.exe"
    mapfolder = root / "pk3" / "maps"

    if not bcc.exists():
        raise SystemExit(f'BCC compiler not found at "{bcc}"')

    if not mapfolder.exists():
        raise SystemExit(f'Source directory "{mapfolder}" does not exist.')

    logging.info(f'Compiling ACS scripts from "{mapfolder}"...\n')

    include_args = [
        "-i", str(root / "pk3" / "libraries" / "ZombieHorde2Lib"),
        "-i", str(root / "pk3" / "ZombieHorde2")
    ]

    # Iterate project folders
    for project_path in sorted(p for p in mapfolder.iterdir() if p.is_dir()):
        project_name = project_path.name
        logging.info(f"Project: {project_name}")

        # Iterate maps inside this project
        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            map_name = map_path.name

            src_acs = map_path / "SCRIPTS"
            dst_behavior = map_path / "BEHAVIOR"

            if not src_acs.exists():
                logging.info(f"Skipped: {map_name} contains no script")
                continue

            #logging.info(f"  Compiling {map_name}...")

            cmd = [str(bcc)] + include_args + [str(src_acs), str(dst_behavior)]
            #logging.info("    " + " ".join(cmd))

            result = subprocess.run(cmd)

            if result.returncode == 0:
                logging.info(f"Compiled {map_name}")
            else:
                logging.error(f"Failed to compile {map_name}")

        logging.info("")

    logging.info("All map scripts compiled.")


if __name__ == "__main__":
    main()
