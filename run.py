"""Run the server in development mode."""
from werkzeug.serving import run_simple

from modly.server import get_instance

if __name__ == '__main__':
    run_simple('localhost', 5000, get_instance(),
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
