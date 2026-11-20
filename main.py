#!/usr/bin/env python3
"""news-image-20261120 v2 entrypoint (Python 3.13, stdlib only).

Copies the pre-rendered front-page image (entry.png, next to this file)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
No network, no randomness: every run writes the same bytes.
The image is validated before copying: it must exist, be a real PNG,
be exactly 1024x1024, and be at most 1 MiB.
"""
import os
import shutil
import struct
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
MAX_BYTES = 1048576  # 1 MiB
EXPECTED_W = 1024
EXPECTED_H = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_png(path):
    """Fail loudly (exit 1) unless path is a valid 1024x1024 PNG <= 1 MiB."""
    if not path.is_file():
        sys.exit(f"error: {IMAGE_NAME} missing: {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        sys.exit(f"error: {IMAGE_NAME} is {size} bytes, over the 1 MiB limit")
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != PNG_MAGIC:
        sys.exit(f"error: {IMAGE_NAME} is not a PNG (bad magic bytes)")
    if len(header) < 24 or header[12:16] != b"IHDR":
        sys.exit(f"error: {IMAGE_NAME} has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        sys.exit(
            f"error: {IMAGE_NAME} is {width}x{height}, "
            f"expected {EXPECTED_W}x{EXPECTED_H}"
        )


def main():
    here = Path(__file__).resolve().parent
    src = here / IMAGE_NAME
    check_png(src)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / IMAGE_NAME)


if __name__ == "__main__":
    main()
