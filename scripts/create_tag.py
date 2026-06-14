import subprocess

MAJOR = 5
MINOR = 1
PATCH = 0
SUFFIX = "beta"

version = f"{MAJOR}.{MINOR}.{PATCH}"
tag = f"v{version}-{SUFFIX}" if SUFFIX else f"v{version}"
message = f"Zombie Horde 2 {SUFFIX} v{version}" if SUFFIX else f"Zombie Horde 2 v{version}"

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