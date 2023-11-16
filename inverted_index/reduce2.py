#!/usr/bin/env python3
"""Reducer 2."""


import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group."""
    doc_list = []
    tmp = 0
    for line in group:
        _, value = line.strip().split("\t")
        doc_id, tf = value.split()
        doc_list.append((doc_id, tf, tmp))
        tmp += 1

    nk = len(doc_list)
    for doc_id, tf, _ in doc_list:
        print(f"{key}\t{doc_id} {tf} {nk}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
