"""Main API file for the index server."""
from collections import defaultdict
from pathlib import Path
import os
import re
from flask import request, jsonify
import index


# global variables
inverted_index_file = {}
pagerank_file = {}
stopwords = set()
cwd = Path.cwd()
# stopwrods loading
stopwords_file_path = os.path.join(
    cwd,
    "index_server/index/",
    "stopwords.txt"
)
with open(stopwords_file_path, 'r', encoding='utf-8') as sf:
    stopwords = set(sf.read().split('\n'))
# pagrank loading
pagerank_file_path = os.path.join(
    cwd,
    "index_server/index/",
    "pagerank.out"
)
with open(pagerank_file_path, 'r', encoding='utf-8') as pf:
    for line in pf:
        doc_id, num = line.split(',')
        pagerank_file[doc_id] = num


def load_index(path):
    """Load the inverted index from a file."""
    inverted_file_path = os.path.join(
        cwd,
        "index_server/index/inverted_index",
        path
    )
    # Load inverted index
    with open(inverted_file_path, 'r', encoding='utf-8') as invf:
        for lne in invf:
            parts = lne.split()
            word = parts[0]
            idf = parts[1]

            docs = parts[2:]
            word_dict = {
                'idf': idf,
                'docs': {}
            }

            for i in range(0, len(docs), 3):
                docid = docs[i]
                tf = docs[i + 1]
                norm = docs[i + 2]
                word_dict['docs'][docid] = {
                    'tf': tf,
                    'norm': norm
                }
            inverted_index_file[word] = word_dict
        # this is what inverted_index_file looks like for michigan:
        # {
        #     'idf': '0.6066714848835395',
        #     'docs': {
        #         '0003': {'tf': '6', 'norm': '89890.53910567179'},
        #         '0009': {'tf': '3', 'norm': '9718.720255495253'}
        #         ...
        #     }
        # }


def clean_query(query):
    """Clean the query."""
    # Remove stopwords and special characters
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.lower().split()
    query = [word for word in query if word not in stopwords]
    # remove idf zero
    # query = [w for w in query if w in inverted_index_file
    #          and inverted_index_file[w]['idf'] != '0']
    return query


@index.app.route('/api/v1/', methods=['GET'])
def index1():
    """Return the API endpoints."""
    return jsonify({
        "hits": "/api/v1/hits",
        "url": "/api/v1/"
    })


def get_query_vector(tf_query):
    """Return the query vector."""
    query_vector = []
    for word, qtf in tf_query.items():
        idf = float(inverted_index_file[word]['idf'])
        query_vector.append((qtf * idf))
    return query_vector


def get_doc_vector(query, docid):
    """Return the document vector."""
    doc_vector = []
    for word in query:
        tf = float(inverted_index_file[word]['docs'][docid]['tf'])
        idf = float(inverted_index_file[word]['idf'])
        tfidf = tf * idf
        doc_vector.append(tfidf)
    return doc_vector


def get_doc_count(tf_query):
    """Return the document count."""
    doc_count = defaultdict(int)
    for word in tf_query:
        for docid in inverted_index_file[word]['docs']:
            doc_count[docid] += 1
    return doc_count


def get_query_norm(query_vector):
    """Return the query norm."""
    query_norm = 0
    for m in query_vector:
        query_norm += m ** 2
    query_norm = query_norm ** 0.5
    return query_norm


def get_doc_norm(query, docid):
    """Return the document norm."""
    word = query[0]  # get first word in query
    # since all words in docid have same norm
    doc_norm = float(inverted_index_file[word]['docs'][docid]['norm']) ** 0.5
    return doc_norm


def get_score(docid, query, weight, query_vector, doc_vector):
    """Return the score."""
    # query normalization
    query_norm = get_query_norm(query_vector)
    # document normalization
    doc_norm = get_doc_norm(query, docid)
    # dot product: document vector * query vector
    dot_product = sum(float(a)*float(b) for a, b in zip(
        query_vector, doc_vector))
    tfidf = dot_product / (query_norm * doc_norm)
    # score
    score = (weight * float(pagerank_file[docid])) + ((1 - weight) * tfidf)
    return score


@index.app.route('/api/v1/hits/', methods=['GET'])
def hits():
    """Return the hits for a given query."""
    query = clean_query(request.args.get('q', default='', type=str))
    weight = request.args.get('w', default=0.5, type=float)
    final_hits = {
        "hits": []
    }

    tf_query = defaultdict(int)
    for word in query:  # Debugging line
        if word in inverted_index_file:
            if inverted_index_file[word]['idf'] != 0:
                tf_query[word] += 1
        else:
            return final_hits

    query_vector = get_query_vector(tf_query)
    doc_count = get_doc_count(tf_query)

    for docid, count in doc_count.items():
        # if doc has all words in query
        if count == len(tf_query):
            # score
            doc_vector = get_doc_vector(query, docid)
            final_score = get_score(
                docid,
                query,
                weight,
                query_vector,
                doc_vector
            )
            final_hits['hits'].append({
                "docid": int(docid),
                "score": final_score,
            })
            # sort by score
    final_hits['hits'] = sorted(
        final_hits['hits'],
        key=lambda k: k['score'],
        reverse=True
    )
    return jsonify(final_hits)
