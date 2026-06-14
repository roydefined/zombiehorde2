#!/usr/bin/env python3
import logging
from logger import setup_logging
from utils import get_paths, get_version, move_file

# === Update mod version across repository ===
# This script reads the project version from version.txt, and updates relevant files to use this.
# Currently, the following files are updated:
# - version.h.acs in the mod's core.


def write_version_file(template_file, output_file, version):
    if not template_file.exists():
        raise SystemExit(f'[ERROR] Version template "{template_file}" does not exist.')

    logging.info(f'Reading template from "{template_file}"...')

    template = template_file.read_text(encoding="utf-8")

    for key, value in version.items():
        template = template.replace(f"{{{{Version{key.capitalize()}}}}}", value)

    logging.info(f'Generate "{output_file}"')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(template, encoding="utf-8")


def main():
    setup_logging()
    paths = get_paths()

    version = get_version()

    logging.info(f'Version: {version["text"]}')

    write_version_file(
        paths["version_template"],
        paths["version_build"],
        version
    )

    move_file(paths["version_build"], paths["version_target"])

    logging.info("Version generation finished.")


if __name__ == "__main__":
    main()