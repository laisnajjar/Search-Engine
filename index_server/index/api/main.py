"""Main API file for the index server."""
from collections import defaultdict
from pathlib import Path
import os
import flask
from flask import request, jsonify, json
import index

inverted_index_file = {}
pagerank_file = {}
stopwords = set()

def load_index(path):
    """Load the inverted index from a file."""
    # inverted_index_file = {}
    # pagerank_file = {}
    # stopwords = set()
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

    # # Load pagerank
    with open(pagerank_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, score = line.split(',')
            pagerank_file[doc_id] = score
    # # Load stopwords
    with open(stopwords_file_path, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().split('\n'))

    return inverted_index_file, pagerank_file, stopwords

def clean_query(query):
    """Clean the query."""
    # Remove stopwords
    query = query.lower().split()
    query = [word for word in query if word not in stopwords]
    # remove idf zero
    query = [w for w in query if w in inverted_index_file 
             and inverted_index_file[w]['idf'] != '0']
    return query

@index.app.route('/api/v1/', methods=['GET'])
def index1():
    """Return the API endpoints."""
    return jsonify({
        "hits": "/api/v1/hits",
        "url": "/api/v1/"
    })

# def query_vector(tf_query):
#     """Return the query vector."""
#     query_vector = []
#     for word, qtf in tf_query.items():
#         idf = float(inverted_index_file[word]['idf'])
#         query_vector.append((qtf * idf))
#     return query_vector

@index.app.route('/api/v1/hits/', methods=['GET'])
def hits():
    """Return the hits for a given query."""
    query = clean_query(request.args.get('q', default='', type=str))
    weight = request.args.get('w', default=0.5, type=float)
    final_hits = {
        "hits": []
    }
    tf_query = defaultdict(int)
    for word in query:
        tf_query[word] += 1

    query_vector = []
    # loop through tf_query since it keys are unique words
    for word, qtf in tf_query.items():
        idf = float(inverted_index_file[word]['idf'])
        query_vector.append((qtf * idf))


    doc_count = defaultdict(int)
    for word in tf_query:
        for docid in inverted_index_file[word]['docs']:
            doc_count[docid] += 1
    for docid, count in doc_count.items():
        # if doc has all words in query
        if count == len(tf_query):
            # query normalization
            query_norm = 0
            for m in query_vector:
                query_norm += m ** 2
            query_norm = query_norm ** 0.5

            # get document vector
            doc_vector = []
            for word in query:
                tf = float(inverted_index_file[word]['docs'][docid]['tf'])
                idf = float(inverted_index_file[word]['idf'])
                tfidf = tf * idf
                doc_vector.append(tfidf)
            # dot product: document vector * query vector
            dot_product = sum([float(a)*float(b) for a,b in zip(query_vector, doc_vector)])
            # document normalization
            word = query[0] # get first word in query
            # since all words in docid have same norm
            doc_norm = float(inverted_index_file[word]['docs'][docid]['norm']) ** 0.5
            tfidf = dot_product / (query_norm * doc_norm)
            # score
            score = (weight * float(pagerank_file[docid])) + ((1 - weight) * tfidf)
            final_hits['hits'].append({
                "docid": int(docid),
                "score": score,
            })
            # sort by score
            final_hits['hits'] = sorted(final_hits['hits'], key=lambda k: k['score'], reverse=False)
    return jsonify(final_hits)
