"""Index API module."""
import os
from flask import Flask
import index.api.main


app = Flask(__name__)

app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
index.api.main.load_index(app.config["INDEX_PATH"])
