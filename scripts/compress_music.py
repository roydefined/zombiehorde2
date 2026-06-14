#!/usr/bin/env python3
import logging
import subprocess
from pathlib import Path
from logger import setup_logging
from utils import get_root

# === Compress music ===
# This script converts MP3/OGG music files under `pk3/` to 128kbps OGG.
# Files are only replaced when the result is meaningfully smaller.
# Configure its values below.

MINIMUM_PERCENT_SAVING = 5
MINIMUM_BYTE_SAVING = 256 * 1024

MUSIC_EXTENSIONS = {".mp3", ".ogg"}


def convert_music_file(input_file: Path):
    temp_file = input_file.with_name(input_file.name + ".tmp.ogg")
    output_file = input_file.with_suffix(".ogg")

    old_size = input_file.stat().st_size

    logging.info(f'Converting "{input_file}"...')

    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", str(input_file),
                "-vn",
                "-c:a", "libvorbis",
                "-b:a", "128k",
                str(temp_file),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        raise SystemExit('[ERROR] ffmpeg was not found. Make sure it is installed and available in PATH.')
    except Exception:
        logging.exception(f'Failed to convert "{input_file}"')
        return

    if result.returncode != 0 or not temp_file.exists():
        logging.error(f'Failed to convert "{input_file}"')
        temp_file.unlink(missing_ok=True)
        return

    new_size = temp_file.stat().st_size
    saved_bytes = old_size - new_size
    saved_percent = (saved_bytes / old_size) * 100 if old_size else 0

    if saved_bytes >= MINIMUM_BYTE_SAVING and saved_percent >= MINIMUM_PERCENT_SAVING:
        try:
            input_file.unlink()

            if output_file.exists():
                output_file.unlink()

            temp_file.rename(output_file)
        except Exception:
            logging.exception(f'Failed to replace "{input_file}"')
            temp_file.unlink(missing_ok=True)
        else:
            logging.info(
                f'Replaced "{input_file}" with "{output_file}" '
                f'({saved_percent:.1f}% smaller, saved {saved_bytes / 1024:.0f} KB)'
            )
    else:
        temp_file.unlink(missing_ok=True)

        logging.info(
            f'Skipped "{input_file}" '
            f'({saved_percent:.1f}% smaller, saved {saved_bytes / 1024:.0f} KB)'
        )


def main():
    setup_logging()

    root = get_root()
    pk3folder = root / "pk3"

    if not pk3folder.exists():
        raise SystemExit(f'[ERROR] Source directory "{pk3folder}" does not exist.')

    logging.info(f'Compressing music files from "{pk3folder}"...')
    logging.info("")

    music_files = sorted(
        p for p in pk3folder.rglob("*")
        if p.is_file() and p.suffix.lower() in MUSIC_EXTENSIONS
    )

    if not music_files:
        logging.info("No MP3/OGG music files found.")
        return

    for music_file in music_files:
        convert_music_file(music_file)

    logging.info("")
    logging.info("Music compression finished.")


if __name__ == "__main__":
    main()