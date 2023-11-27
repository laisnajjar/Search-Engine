"""Engine package initializer."""
from flask import Flask

# app is a single object used by all the code modules in this package
app = Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module (search/config.py)
app.config.from_object('search.config')

import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position
