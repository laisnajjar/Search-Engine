#!/usr/bin/env python3
"""Reducer 5."""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    for line in group:
        key, value = line.strip().split("\t")
        term, doc_id, tf, idf, doc_normalization = value.split()
        final_data = f"{term} {idf} {doc_id} {tf} {doc_normalization}"
        print(final_data)

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
