"""Index API module."""
import os
from flask import Flask


app = Flask(__name__)
import index.api  # noqa: E402  pylint: disable=wrong-import-position

app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
index.api.main.load_index(app.config["INDEX_PATH"])
