#!/usr/bin/env python3
"""Entry for news-image-20261122: "Sum up 22 November's world news in one image".

The entry is a single 1024x1024 newspaper front page, "THE WORLD", drawn
by render.py (in this repository) from the day's verified news: the COP31
climate deadlock, the widening Gulf war, the Peru earthquake, the cartel
arrest in Mexico, the Ukraine barrage, APEC in Shenzhen, and the day's
briefs. The rendered page is stored as entry.png; this program copies it
to /output/entry.png so the run is byte-for-byte deterministic with no
network access.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join("/output", "entry.png")


def main():
    os.makedirs("/output", exist_ok=True)
    if not os.path.exists(SRC):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, DST)
    print("wrote", DST, os.path.getsize(DST), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
