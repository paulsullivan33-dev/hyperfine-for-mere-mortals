#!/usr/bin/env python3
"""Count the ERROR lines in the lab's log file.

Usage: python3 count_errors.py log.txt

The third contestant in chapter 6's comparison: the same job as
the grep and awk one-liners, done by a small Python script.
"""

import sys

count = 0
with open(sys.argv[1]) as f:
    for line in f:
        if "ERROR" in line:
            count += 1
print(count)
