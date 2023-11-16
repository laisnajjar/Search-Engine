#!/usr/bin/env python3
"""Reducer 4."""
import sys
import itertools

def reduce_one_group(key, group):
    """Reduce one group."""
    doc_normalization = 0
    doc_list = []
    doc_id = key
    for line in group:
        _, value = line.strip().split("\t") # key is doc_id
        idf, term, tf = value.split()
        tf_idf_square = (float(tf) * float(idf)) ** 2
        doc_normalization += tf_idf_square
        doc_list.append((term, tf, idf))

    for term, tf, idf in doc_list:
        print(f"{term} {doc_id}\t{tf} {idf} {doc_normalization}")

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
