#!/usr/bin/env python3
"""Map 0."""
import re
import sys

for line in sys.stdin:
    print("\t1")
# clean document
def clean_document(document):
    """Clean document."""
    with open(document, 'w', encoding='UTF-8') as f:
        text = f.read()
        text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
        text = text.lower()
        text.split()
        # remove words in stopwords.txt
        with open('stopwords.txt', 'r', encoding='UTF-8') as f:
            stopwords = f.read()
            stopwords = stopwords.split()
            text = [word for word in text if word not in stopwords]
