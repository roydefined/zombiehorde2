#!/usr/bin/env python3
import logging
from pathlib import Path
from utils import setup_logging, get_paths, copy_file, run_cmd

# === Zombie Horde 2 project build script ===
# This script copies over the previously packed ACSUtils files and puts them inside the library project.
# Secondly this script ensures all files are compiled.

# Note: You must call `pack-acsutils.py` before calling this file to ensure all files exist.
# Alternatively make sure that they do another way.

def main():
    setup_logging()
    paths = get_paths()

    bcc = paths["bcc"]

    logging.info("Build Zombie Horde 2")

    # Copy ACSUtils artifacts over from the module into lib.
    copy_file(paths["acsutils_dist"] / "bcsutils.bcs",
              paths["bcsutils_target"] / "bcsutils.acs")

    copy_file(paths["acsutils_dist"] / "cvarinfo.acsutils",
              paths["lib"] / "cvarinfo.acsutils")

    copy_file(paths["acsutils_dist"] / "decorate.acsutils",
              paths["lib"] / "decorate.acsutils")

    logging.info("Compiling...")

    macro_lib = ["-D", "DEV"]
    macro_core = ["-D", "DEV", "-D", "DEV_PLAYERCAP"]

    include_lib = ["-i", str(paths["lib_src"])]
    include_core = [
        "-i", str(paths["lib_src"]),
        "-i", str(paths["lib_src"] / "bcsutils")
    ]

    # Build BCSUtils source.
    logging.info("[bcsutils]")
    run_cmd([
        str(bcc),
        str(paths["lib_src"] / "bcsutils.acs"),
        str(paths["lib_acs"] / "bcsutils.o"),
    ])

    # Build lib source.
    logging.info("[lib]")
    run_cmd(
        [str(bcc)]
        + include_lib
        + macro_lib
        + [
            str(paths["lib_src"] / "zh2lib.acs"),
            str(paths["lib_acs"] / "zh2lib.o")
        ]
    )

    # Build core source.
    logging.info("[core]")
    run_cmd(
        [str(bcc)]
        + include_core
        + macro_core
        + [
            str(paths["core_src"] / "zh2game.acs"),
            str(paths["core_out"] / "zh2game.o")
        ]
    )

    logging.info("SUCCESS")


if __name__ == "__main__":
    main()
