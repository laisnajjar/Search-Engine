"""Main API file for the index server."""
from pathlib import Path
import os
import flask
from flask import request, jsonify, json

app = flask.Flask(__name__)


def load_index(path):
    """Load the inverted index from a file."""
    inverted_index_file = {}
    pagerank_file = {}
    stopwords = set()

    # Get the paths
    cwd = Path.cwd()
    inverted_file_path = os.path.join(cwd, "index_server/index/inverted_index", path)
    pagerank_file_path = os.path.join(cwd, "index_server/index/", "pagerank.out")
    stopwords_file_path = os.path.join(cwd, "index_server/index/", "stopwords.txt")
    # Load inverted index
    with open(inverted_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            word = parts[0]
            values = parts[1:]
            inverted_index_file[word] = values
    # # Load pagerank
    with open(pagerank_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, score = line.split(',')
            pagerank_file[doc_id] = score
    # # Load stopwords
    with open(stopwords_file_path, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().split('\n'))

    return inverted_index_file, pagerank_file, stopwords

@app.route('/api/v1/', methods=['GET'])
def index():
    """Return the API endpoints."""
    return jsonify({
        "hits": "/api/v1/hits",
        "url": "/api/v1/"
    })

@app.route('/api/v1/hits', methods=['GET'])
def hits():
    """Return the hits for a given query."""
    query = request.args.get('q', default='', type=str)
    weight = request.args.get('w', default=0.5, type=float)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
