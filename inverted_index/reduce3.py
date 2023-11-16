#!/usr/bin/env python3
"""Reducer 3."""
import sys
import itertools
import math

def read_total_document_count(file_path):
    """Read the total document count from a file."""
    with open(file_path, 'r', encoding="UTF-8") as file:
        count = file.read().strip()
        return int(count)

def reduce_one_group(key, group, doc_count):
    """Reduce one group."""
    for line in group:
        _, value = line.strip().split("\t")
        doc_id, tf, nk = value.split()
        idf = math.log10(doc_count / int(nk))
        print(f"{key} \t{idf} {doc_id} {tf}")

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    doc_count = read_total_document_count("total_document_count.txt")
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group, doc_count)


if __name__ == "__main__":
    main()
