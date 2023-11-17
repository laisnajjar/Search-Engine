"""Main API file for the index server."""
import flask
from flask import request, jsonify, json


app = flask.Flask(__name__)


def load_index(path):
    """Load the inverted index from a file."""
    inverted_index_file = {}
    pagerank_file = {}
    stopwords = set()

    # Load inverted index
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line[0]
            values = line[1:]
            inverted_index_file[word] = values
    # Load pagerank
    with open('pagerank.out', 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, score = line.split(',')
            pagerank_file[doc_id] = score
    # Load stopwords
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        stopwords = set(file.read().split('\n'))

    return inverted_index_file, pagerank_file, stopwords

@app.route('/api/v1/', methods=['GET'])
def index():
    """Return the API endpoints."""
    return jsonify({
        "hits": "/api/v1/hits",
        "url": "/api/v1/"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
