#!/usr/bin/env python3
"""Map 1."""
import pathlib
import re
import sys

import bs4

# Open and read from one HTML document at a time
for line in sys.stdin:
    # Each line is a path to a document from the dataset
    # Documents are stored at <INPUT_DIR>/crawl/<doc_id>.html
    doc_path = pathlib.Path(line.strip())
    # Get doc_id from filename
    doc_id = line.split(".")[0][-4:]
    # Read document body from file
    text = doc_path.read_text(encoding="utf-8")
    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(text, "html.parser")
    # Parse text from document
    text = soup.text
    # Clean document
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.lower()
    text = text.split()
    with open('stopwords.txt', 'r', encoding='UTF-8') as f:
        stopwords = f.read()
        stopwords = stopwords.split()
        text = [word for word in text if word not in stopwords]
    # (key, value) = (term, {doc_id, 1})
    for word in text:
        print(f"{word} {doc_id}\t1")
