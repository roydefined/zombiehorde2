#!/usr/bin/env python3
from utils import get_root

CFG_FILE = "docs/host.cfg"
TEMPLATE_FILE = "docs/host-template.cfg"


def get_maps(root):
    maps = []
    maps_root = root / "pk3" / "maps"

    for project_path in sorted(p for p in maps_root.iterdir() if p.is_dir()):

        # Skip the test maps.
        if project_path.name.lower() == "test":
            continue

        for map_path in sorted(p for p in project_path.iterdir() if p.is_dir()):
            maps.append(map_path.name)

    return maps


def get_maplist(root):
    return "\n".join(f"addmap {map_name}" for map_name in get_maps(root))


def build_cfg(root):
    template_path = root / TEMPLATE_FILE
    template = template_path.read_text(encoding="utf-8")

    return template.replace("{maplist}", get_maplist(root)) + "\n"


def main():
    root = get_root()
    cfg_path = root / CFG_FILE

    cfg = build_cfg(root)
    cfg_path.write_text(cfg, encoding="utf-8")

    print(f"Wrote {cfg_path}")


if __name__ == "__main__":
    main()