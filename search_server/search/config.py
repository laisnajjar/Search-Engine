"""SEARCH development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_FILENAME = SEARCH_ROOT/'var'/'search.sqlite3'

# API URLs
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]
