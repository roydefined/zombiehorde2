#!/usr/bin/env python3
import logging
from pathlib import Path

# Helper function that sets up the logger used for logging script output.
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
        datefmt="%H:%M:%S"
    )

# Helper function that returns the root of the project.
def get_root() -> Path:
    return Path(__file__).resolve().parent.parent

# Helper function that returns common paths.
def get_paths():
    root = get_root()
    return {
        "bcc": root / "tools" / "Zt-bcc_x86" / "zt-bcc.exe",

        # ACSUtils
        "acsutils_dist": root / "modules" / "acsutils" / "dist",
        "bcsutils_target": root / "libsrc" / "acs_source" / "bcsutils",

        # Library
        "libsrc": root / "libsrc",
        "libsrc_acs_source": root / "libsrc" / "acs_source",
        "libsrc_acs": root / "libsrc" / "acs",

        # Core
        "core_src": root / "src" / "ZombieHorde2" / "acs_source",
        "core_out": root / "src" / "ZombieHorde2" / "acs",
    }

# Helper function to copy over a file.
def copy_file(src: Path, dest: Path):
    import shutil
    logging.info(f"Copy {src} -> {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)

# Helper function to run an executable.
def run_cmd(cmd: list[str]):
    import subprocess
    logging.info(" ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
