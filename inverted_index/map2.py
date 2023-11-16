#!/usr/bin/env python3
"""Map 1."""
import sys

# Open and read from one HTML document at a time
for line in sys.stdin:
    key, tf = line.strip().split("\t")
    term, doc_id = key.split()
    print(f"{term}\t{doc_id} {tf}")
