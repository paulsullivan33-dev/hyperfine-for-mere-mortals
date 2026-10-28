#!/usr/bin/env python3
"""Generate the lab's fixture files, deterministically.

Usage: python3 make_fixtures.py [directory]

Creates, in the chosen directory (default: current directory):
  log.txt        50,000 lines of invented server log, about 5% ERROR
  numbers.txt    200,000 shuffled integers, one per line
  article.txt    about 8 MB of invented prose, for compression runs
  article.txt.gz article.txt compressed once, for decompression runs

Everything is invented, the seeds are fixed, and re-running the
script reproduces the same files.
"""

import gzip
import random
import shutil
import sys
from pathlib import Path

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out.mkdir(parents=True, exist_ok=True)

# --- log.txt -----------------------------------------------------
rng = random.Random(20260115)
workers = [f"worker-{n}" for n in range(1, 7)]
actions = ["opened a session", "fetched a record", "stored a result",
           "checked a queue", "renewed a lease", "flushed a buffer"]
with open(out / "log.txt", "w") as f:
    for i in range(50_000):
        roll = rng.random()
        level = "ERROR" if roll < 0.05 else "WARN" if roll < 0.20 else "INFO"
        f.write(
            f"2026-01-15T08:{rng.randrange(60):02d}:{rng.randrange(60):02d} "
            f"{level:5s} {rng.choice(workers)} {rng.choice(actions)} "
            f"(item {1000 + i})\n"
        )

# --- numbers.txt ---------------------------------------------------
rng = random.Random(42)
numbers = list(range(1, 200_001))
rng.shuffle(numbers)
with open(out / "numbers.txt", "w") as f:
    f.write("\n".join(map(str, numbers)) + "\n")

# --- article.txt ---------------------------------------------------
paragraph = (
    "The harbour office kept its records in a tin box above the door. "
    "Every morning the clerk wrote the tide, the wind, and the names of "
    "the boats that had come in during the night. Nobody could remember "
    "when the habit started, and nobody saw a reason to stop. A record "
    "that is kept the same way every day becomes a kind of promise: "
    "whoever reads it later can trust that the gaps mean something too. "
)
with open(out / "article.txt", "w") as f:
    block = 0
    written = 0
    while written < 8_000_000:
        block += 1
        text = f"Section {block}. " + paragraph * 6 + "\n\n"
        f.write(text)
        written += len(text)

with open(out / "article.txt", "rb") as src, \
        gzip.open(out / "article.txt.gz", "wb", compresslevel=6) as dst:
    shutil.copyfileobj(src, dst)

for name in ["log.txt", "numbers.txt", "article.txt", "article.txt.gz"]:
    p = out / name
    print(f"{name:16s} {p.stat().st_size:>10,} bytes")
