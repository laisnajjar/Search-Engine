"""Search server index view."""

import threading
import heapq
import flask
import search
import requests
from search.config import SEARCH_INDEX_SEGMENT_API_URLS


def fetch_results(url, q, w, results):
    """Fetch results from a url."""
    params = {"q": q, "w": w}
    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.Timeout:
        print("Timeout occurred")

    results.append(response.json()["hits"])


@search.app.route('/', methods=["GET"])
def show_index():
    """Display / route."""
    q = flask.request.args.get("q", default=None, type=str)
    w = flask.request.args.get("w", default=0.3, type=float)
    db = search.model.get_db()
    context = {"results": []}

    if q is not None:
        results = []
        threads = []

        for url in SEARCH_INDEX_SEGMENT_API_URLS:
            thread = threading.Thread(
                target=fetch_results,
                args=(url, q, w, results))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # merge results & grab top 10 using heappq
        results = heapq.merge(*results, key=lambda x: x["score"], reverse=True)
        results = heapq.nlargest(10, results, key=lambda x: x["score"])

        for result in results:
            doc_fetch_info = db.execute(
                "SELECT * FROM Documents WHERE docid = ? ", (result["docid"],)
            ).fetchone()
            if doc_fetch_info is not None:
                context["results"].append(doc_fetch_info)
    return flask.render_template("index.html", **context)
