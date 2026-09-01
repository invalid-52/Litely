"""Production WSGI entry point for LITELY."""

import os
from litely import create_app

app = create_app(os.getenv("FLASK_ENV", "production"))
