#!/usr/bin/env python3
import logging
import re
from logger import setup_logging
from utils import get_paths, move_file

# === Update mod version accross repository ===
# This script reads the project version from version.txt, and updates relevant files to use this.
# Currently, the following files are updated:
# - version.h.acs in the mod's core.

VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$")


def parse_version(version_text: str):
    match = VERSION_PATTERN.match(version_text)

    if not match:
        raise SystemExit(
            f'[ERROR] Invalid version "{version_text}". '
            'Expected format: major.minor.patch or major.minor.patch-suffix.'
        )

    major, minor, patch, suffix = match.groups()

    return {
        "major": major,
        "minor": minor,
        "patch": patch,
        "suffix": suffix or "",
    }


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

    version_file = paths["version"]
    template_file = paths["version_template"]
    build_file = paths["version_build"]
    target_file = paths["version_target"]

    if not version_file.exists():
        raise SystemExit(f'[ERROR] Version file "{version_file}" does not exist.')

    logging.info(f'Reading version from "{version_file}"...')

    version_text = version_file.read_text(encoding="utf-8").strip()

    logging.info(f'Version: {version_text}')

    version = parse_version(version_text)

    write_version_file(template_file, build_file, version)
    move_file(build_file, target_file)

    logging.info("Version generation finished.")


if __name__ == "__main__":
    main()