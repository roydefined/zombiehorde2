import subprocess
import sys

MAJOR = 5
MINOR = 1
PATCH = 0
SUFFIX = "beta"

DELETE_EXISTING = "--delete" in sys.argv

version = f"{MAJOR}.{MINOR}.{PATCH}"
tag = f"v{version}-{SUFFIX}" if SUFFIX else f"v{version}"
message = f"Zombie Horde 2 {SUFFIX} v{version}" if SUFFIX else f"Zombie Horde 2 v{version}"

tag_exists = subprocess.run(
    ["git", "rev-parse", tag],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
).returncode == 0

if tag_exists:
    if not DELETE_EXISTING:
        print(f"Tag '{tag}' already exists.")
        print("Run with --delete to replace it.")
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