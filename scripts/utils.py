#!/usr/bin/env python3
import logging
from pathlib import Path

# ---------------------------------------------------------------------------
# Folder mapping: maps folder <-> mod folder
# ---------------------------------------------------------------------------

_MAP_TO_MOD = {
    "legacy": "ZombieHorde2Legacy",
    "modern": "ZombieHorde2Modern",
    "test": "ZombieHorde2TestMaps",
}

_MOD_TO_MAP = {v: k for k, v in _MAP_TO_MOD.items()}


def map_to_mod_folder(name: str) -> str:
    """maps folder -> mod folder (e.g. 'legacy' -> 'ZombieHorde2Legacy')."""
    try:
        return _MAP_TO_MOD[name]
    except KeyError:
        raise KeyError(f"Unknown maps folder: {name!r}. Known: {list(_MAP_TO_MOD.keys())}")


def mod_to_map_folder(name: str) -> str:
    """mod folder -> maps folder (e.g. 'ZombieHorde2Legacy' -> 'legacy')."""
    try:
        return _MOD_TO_MAP[name]
    except KeyError:
        raise KeyError(f"Unknown mod folder: {name!r}. Known: {list(_MOD_TO_MAP.keys())}")


def map_path_to_mod_path(path: Path) -> Path:
    """Replace the last path segment using the maps->mod mapping."""
    return path.with_name(map_to_mod_folder(path.name))


def mod_path_to_map_path(path: Path) -> Path:
    """Replace the last path segment using the mod->maps mapping."""
    return path.with_name(mod_to_map_folder(path.name))


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
        "bcsutils_target": root / "pk3" / "lib" / "acs_source" / "bcsutils",

        # Library
        "libsrc": root / "pk3" / "lib",
        "libsrc_acs_source": root / "pk3" / "lib" / "acs_source",
        "libsrc_acs": root / "pk3" / "lib" / "acs",

        # Core
        "core_src": root / "pk3" / "ZombieHorde2" / "acs_source",
        "core_out": root / "pk3" / "ZombieHorde2" / "acs",
    }


# Helper function to copy over a file.
def copy_file(src: Path, dest: Path):
    import shutil

    if not src.exists():
        raise FileNotFoundError(f"Source does not exist: {src}")

    logging.info(f"Copy {src.name} -> {dest}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


# Helper function to run an executable.
def run_cmd(cmd: list[str]):
    import subprocess
    #logging.info(" ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
