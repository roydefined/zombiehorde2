#!/usr/bin/env python3
import subprocess
import sys
import time

from utils import get_root, get_paths

# === Zombie Horde 2 local host launcher ===
# This script starts a local host and client instance for quick multiplayer testing.
# By default the server uses a host config, located at 'docs/zh2-host.cfg'.
# This can be disabled by passing `--nohostconfig`.
# Note doing so will make the script add `+addmap` parameters instead for the maps.

PORT = "10666"

ZH2_FILES = [
    "lib",
    "ZombieHorde2",
    "ZombieHorde2Doom",
    "ZombieHorde2Legacy",
    "ZombieHorde2Modern",
    "ZombieHorde2Resources",
    "ZombieHorde2TestMaps",
]


def get_file_args(root):
    args = []

    for name in ZH2_FILES:
        args.extend(["-file", str(root / "pk3" / name)])

    return args


def get_map_args(root):
    args = []
    maps_root = root / "pk3" / "maps"

    for project_path in sorted(p for p in maps_root.iterdir() if p.is_dir()):
        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            args.extend(["+addmap", map_path.name])

    return args


def get_host_config_args(root):
    return ["+exec", str(root / "docs" / "host.cfg")]


def log_cmd(label, cmd):
    print(f"{label}:")
    print(" ".join(f'"{c}"' if " " in c else c for c in cmd))
    print("")


def start_host(root, paths, use_host_config):
    cmd = [
        str(paths["zandronum"]),
        "-host", "1",
        "-iwad", str(paths["iwad"]),
        *get_file_args(root),
    ]

    # Use the predefined host config by default.
    # Otherwise generate map arguments dynamically.
    if use_host_config:
        cmd.extend(get_host_config_args(root))
    else:
        cmd.extend(get_map_args(root))

    log_cmd("Host command", cmd)
    return subprocess.Popen(cmd)


def start_client(root, paths):
    cmd = [
        str(paths["zandronum"]),
        "-connect", f"127.0.0.1:{PORT}",
        "-iwad", str(paths["iwad"]),
        *get_file_args(root),
    ]

    log_cmd("Join command:", cmd)
    return subprocess.Popen(cmd)


def main():
    root = get_root()
    paths = get_paths()

    # Disable the host config when --nohostconfig is passed.
    use_host_config = "--nohostconfig" not in sys.argv

    host = start_host(root, paths, use_host_config)

    # Give the server a short moment to initialize before joining.
    time.sleep(0.5)

    client = start_client(root, paths)

    host.wait()
    client.wait()


if __name__ == "__main__":
    main()