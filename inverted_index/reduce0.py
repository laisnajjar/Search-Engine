#!/usr/bin/env python3
"""Reduce 0."""
import sys

TOTAL = 0
for line in sys.stdin:
    TOTAL += int(line.strip())
print(TOTAL)
