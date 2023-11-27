"""Search server index view."""

import flask
import search


@search.app.route('/', methods=["GET"])
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)
