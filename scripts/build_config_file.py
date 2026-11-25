#!/usr/bin/env python3
import logging
from logger import setup_logging, get_log_level
from utils import get_root

CFG_FILE = "docs/maplist-{package}.cfg"

# Maps that are not to be included as they are unfinished.
DISABLED_MAPS = ["ZM27B", "ZM33M"]


def get_maps(project_path):
    maps = []

    for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
        maps.append(map_path.name)

    return maps


def get_maplist(project_path):
    lines = []

    for map_name in get_maps(project_path):

        # Disabled maps are kept in the list, but commented out.
        if map_name in DISABLED_MAPS:
            lines.append(f"//addmap {map_name} // TODO")
        else:
            lines.append(f"addmap {map_name}")

    return "\n".join(lines)


def build_cfg(package, project_path):
    header = (
        f"// Map list of the {package} package.\n"
        f"// Exec this after host.cfg, e.g. `+exec host.cfg +exec maplist-{package}.cfg`\n"
        "\n"
    )

    return header + get_maplist(project_path) + "\n"


def main():
    setup_logging(get_log_level())

    root = get_root()
    maps_root = root / "pk3" / "maps"

    for project_path in sorted(p for p in maps_root.iterdir() if p.is_dir()):

        # Skip the test maps.
        if project_path.name.lower() == "test":
            continue

        package = project_path.name.lower()
        cfg_path = root / CFG_FILE.format(package=package)
        cfg_path.write_text(build_cfg(package, project_path), encoding="utf-8")

        logging.info(f"Wrote {cfg_path}")


if __name__ == "__main__":
    main()