#!/usr/bin/env python3
import logging
import subprocess
import sys
import time

from logger import setup_logging, get_log_level
from utils import get_root, get_paths, map_to_mod_folder

# === Zombie Horde 2 local host launcher ===
# This script starts a local host and client instance for quick multiplayer testing.
# By default the server uses a host config, located at 'docs/host.cfg'.
# After it, the map list of every loaded package is executed, e.g. 'docs/maplist-legacy.cfg'.
# This can be disabled by passing `--nohostconfig`.
# Note doing so will make the script add `+addmap` parameters instead for the maps of the loaded packages and the test maps.
# The server also loads 'docs/host-testing.cfg' for local testing settings.
# This can be disabled by passing `--notestingconfig`.
# Pass `--classicmode` to also load 'docs/classicmode.cfg' on top of the host config.
# The client loads all radio packs in 'pk3/radiopacks'.
# This can be disabled by passing `--noradio`.
# The script asks how many clients to start (0-6), pressing enter starts 1 and 0 starts only the host.
# Pass `--clients <count>` to skip the question.

# All packages are loaded by default but can be excluded from loading individually.
# However, this is all based on an order. If you exclude a folder everything that depends on it is also excluded.
# The order of execution is as follows:
#   core (lib + core) -> resources (resources + Doom) -> legacy -> modern

# The following parameters provide the exclusion, and what won't load.
#   `--nomodern` excludes modern.
#   `--nolegacy` excludes legacy and modern.
#   `--noresources` excludes resources, legacy and modern.

PORT = "10666"
MAX_CLIENTS = 6

# Packages in load order, and the folders that represent them.
# Each package requires all packages before it.
ZH2_PACKAGES = [
    ("core", ["libraries/ZombieHorde2Lib", "ZombieHorde2"]),
    ("resources", ["ZombieHorde2Resources", "ZombieHorde2Doom"]),
    ("legacy", ["ZombieHorde2Legacy"]),
    ("modern", ["ZombieHorde2Modern"]),
]

ZH2_TEST_FILES = ["ZombieHorde2TestMaps"]

# Loading stops before the first excluded package.
# First index is skipped as the core should always be loaded.
# The approach is generic, so more folders can be added as a package.
def get_last_package_index():
    for index in range(1, len(ZH2_PACKAGES)):
        name, _ = ZH2_PACKAGES[index]
        if f"--no{name}" in sys.argv:
            return index - 1

    return len(ZH2_PACKAGES) - 1


def get_file_args(root, packages, use_radio):
    args = []

    folders = [folder for _, package_folders in packages for folder in package_folders]
    for name in folders + ZH2_TEST_FILES:
        args.extend(["-file", str(root / "pk3" / name)])

    # Radio packs are loaded after the main files. Only the client loads them.
    if use_radio:
        radio_root = root / "pk3" / "radiopacks"
        for radio_path in sorted(p for p in radio_root.iterdir() if p.is_dir()):
            args.extend(["-file", str(radio_path)])

    return args


def get_map_args(root, packages):
    args = []
    maps_root = root / "pk3" / "maps"

    # The test maps are always loaded, the other maps only when their package is loaded.
    loaded_folders = list(ZH2_TEST_FILES)
    for _, package_folders in packages:
        loaded_folders.extend(package_folders)

    for project_path in sorted(p for p in maps_root.iterdir() if p.is_dir()):

        # Skip the maps of packages that aren't loaded.
        if map_to_mod_folder(project_path.name) not in loaded_folders:
            continue

        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            args.extend(["+addmap", map_path.name])

    return args


def get_host_config_args(root, packages):
    args = ["+exec", str(root / "docs" / "host.cfg")]

    # Execute the map list of every loaded package. Packages without maps have no map list.
    for name, _ in packages:
        maplist_path = root / "docs" / f"maplist-{name}.cfg"
        if maplist_path.exists():
            args.extend(["+exec", str(maplist_path)])

    return args


def get_testing_config_args(root):
    return ["+exec", str(root / "docs" / "host-testing.cfg")]


def get_classic_mode_config_args(root):
    return ["+exec", str(root / "docs" / "classicmode.cfg")]


def log_cmd(label, cmd):
    logging.info(f"{label}:")
    logging.info(" ".join(f'"{c}"' if " " in c else c for c in cmd))
    logging.debug("")


def start_host(root, paths, packages, use_host_config, use_testing_config, use_classic_mode):
    cmd = [
        str(paths["zandronum"]),
        "-host",
        "-iwad", str(paths["iwad"]),

        # The radio is never loaded on the host.
        *get_file_args(root, packages, use_radio=False),
    ]

    # Use the predefined host config by default.
    # Otherwise generate map arguments dynamically.
    if use_host_config:
        cmd.extend(get_host_config_args(root, packages))
    else:
        cmd.extend(get_map_args(root, packages))

    # Local testing settings are loaded after the host config so they override it.
    if use_testing_config:
        cmd.extend(get_testing_config_args(root))

    # Classic mode is loaded last so it overrides the host config's settings.
    if use_classic_mode:
        cmd.extend(get_classic_mode_config_args(root))

    log_cmd("Host command", cmd)
    return subprocess.Popen(cmd)


def start_client(root, paths, packages, use_radio):
    cmd = [
        str(paths["zandronum"]),
        "-connect", f"127.0.0.1:{PORT}",
        "-iwad", str(paths["iwad"]),
        *get_file_args(root, packages, use_radio),
    ]

    log_cmd("Join command", cmd)
    return subprocess.Popen(cmd)


def ask_client_count():
    # Ask until a valid number is entered. Pressing enter defaults to 1.
    while True:
        try:
            answer = input(f"How many clients to start (0-{MAX_CLIENTS})? [1]: ").strip()
        except EOFError:
            return 1

        if answer == "":
            return 1

        if answer.isdigit():
            return int(answer)

        print("Please enter a number, or press enter for 1.")


def get_client_count():
    # Check `--clients <count>` or ask for client count.
    if "--clients" not in sys.argv:
        return ask_client_count()

    index = sys.argv.index("--clients")
    if index + 1 >= len(sys.argv) or not sys.argv[index + 1].isdigit():
        logging.error("`--clients` requires a number.")
        sys.exit(1)

    return int(sys.argv[index + 1])


def main():
    setup_logging(get_log_level())

    root = get_root()
    paths = get_paths()

    # Disable the host config when --nohostconfig is passed.
    use_host_config = "--nohostconfig" not in sys.argv
    use_testing_config = "--notestingconfig" not in sys.argv
    use_classic_mode = "--classicmode" in sys.argv
    use_radio = "--noradio" not in sys.argv
    packages = ZH2_PACKAGES[:get_last_package_index() + 1]
    logging.info(f"Loading packages: {', '.join(name for name, _ in packages)}")

    client_count = get_client_count()
    if client_count > MAX_CLIENTS:
        logging.warning(f"Clamped client count {client_count} to {MAX_CLIENTS}.")
        client_count = MAX_CLIENTS

    host = start_host(root, paths, packages, use_host_config, use_testing_config, use_classic_mode)

    # Give the server a short moment to initialize before joining.
    time.sleep(0.5)

    clients = [start_client(root, paths, packages, use_radio) for _ in range(client_count)]

    host.wait()
    for client in clients:
        client.wait()


if __name__ == "__main__":
    main()