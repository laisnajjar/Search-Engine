#!/usr/bin/env python3
"""Map 5."""
import sys

# Open and read from one HTML document at a time
for line in sys.stdin:
    key, value = line.strip().split("\t")
    _, doc_id = key.split()
    segment = int(doc_id) % 3
    print(f"{segment}\t{key} {value}")
