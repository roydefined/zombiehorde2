#!/usr/bin/env python3
import logging
import subprocess
import sys
from logger import setup_logging, get_log_level
from utils import get_version

setup_logging(get_log_level())

DELETE_EXISTING = "--delete" in sys.argv

version_info = get_version()

version = version_info["version"]
suffix = version_info["suffix"]

tag = f"v{version}-{suffix}" if suffix else f"v{version}"
message = f"Zombie Horde 2 {suffix} v{version}" if suffix else f"Zombie Horde 2 v{version}"

tag_exists = subprocess.run(
    ["git", "rev-parse", tag],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
).returncode == 0

if tag_exists:
    if not DELETE_EXISTING:
        logging.error(f"Tag '{tag}' already exists.")
        logging.error("Run with --delete to replace it.")
        sys.exit(1)

    subprocess.run(["git", "tag", "-d", tag], check=False)
    subprocess.run(["git", "push", "origin", f":refs/tags/{tag}"], check=False)

subprocess.run(
    ["git", "tag", "-a", tag, "-m", message],
    check=True
)

subprocess.run(
    ["git", "push", "origin", tag],
    check=True
)