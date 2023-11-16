#!/usr/bin/env python3
"""Reducer 5."""


import sys
import itertools


def reduce_one_group(group):
    """Reduce one group."""
    previous_term = None
    final_data = None
    for line in group:
        _, value = line.strip().split("\t")
        term, doc_id, tf, idf, doc_normalization = value.split()
        if previous_term is None:
            previous_term = term
            final_data = f"{term} {idf} {doc_id} {tf} {doc_normalization}"
        elif term == previous_term:
            final_data += f" {doc_id} {tf} {doc_normalization}"
        else:
            # Print the aggregated data for the previous term
            print(final_data)
            # Start a new line for the new term
            final_data = f"{term} {idf} {doc_id} {tf} {doc_normalization}"
            previous_term = term

    # Print the final line after the loop
    if final_data:
        print(final_data)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
