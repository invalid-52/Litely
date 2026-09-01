#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""LITELY V1 Entry Point.

Beautiful code. Instantly.
"""

import os
from litely import create_app

# Create application instance using environment or default configuration
env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    default_debug = "false" if env.lower() == "production" else "true"
    debug = os.getenv("DEBUG", default_debug).lower() in ("true", "1")
    
    use_reloader = os.getenv("USE_RELOADER", "false").lower() in ("true", "1")
    print(f"Starting LITELY V1 server at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=use_reloader)
