#!/usr/bin/env python3
import logging
import os
from pathlib import Path
from utils import setup_logging, get_paths, copy_file, run_cmd

# === ACSUtils packing script ===
# This script prepares ACSUtils by copying files and running preprocessing steps.
# The ACSUtils compilation itself is handled elsewhere (e.g. build-project.py).

def main():
    setup_logging()
    paths = get_paths()

    acsutils_dir = paths["acsutils_dist"].parent
    dist_dir = paths["acsutils_dist"]
    misc_dir = acsutils_dir / "misc"

    logging.info("Pack ACSUtils")

    # Recreate dist/ directory
    if dist_dir.exists():
        logging.info(f"Removing {dist_dir}")
        import shutil
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    # Copy misc files
    copy_file(misc_dir / "cvarinfo.acsutils", dist_dir / "cvarinfo.acsutils")
    copy_file(misc_dir / "decorate.acsutils", dist_dir / "decorate.acsutils")

    # ACSUtils' Python scripts require their working directory to be inside the actual module.
    os.chdir(acsutils_dir)

    # Run preprocess.py
    logging.info("[preprocess]")
    run_cmd(["py", "tools/preprocess.py"])

    # Run changeflaggen.py
    logging.info("[changeflaggen]")
    run_cmd(["py", "tools/changeflaggen.py"])

    logging.info("SUCCESS")


if __name__ == "__main__":
    main()
