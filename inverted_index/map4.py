#!/usr/bin/env python3
"""Map 4."""
import sys

# Open and read from one HTML document at a time
for line in sys.stdin:
    key, value = line.strip().split("\t")
    idf, doc_id, tf = value.split()
    print(f"{doc_id}\t{idf} {key} {tf}")
