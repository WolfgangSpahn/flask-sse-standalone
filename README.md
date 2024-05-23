# Flask SSE Standalone ![build-status](https://github.com/singingwolfboy/flask-sse/workflows/Test/badge.svg) ![coverage-status](http://codecov.io/github/singingwolfboy/flask-sse/coverage.svg?branch=master) ![docs](https://readthedocs.org/projects/flask-sse/badge/?version=latest&style=flat)

A Flask extension for HTML5 [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) support, standalone

Example of setting up a SSE server

~~~~python
import os
import logging
from multiprocessing import Process, Event


# -- local imports
from sse.manager import start_sse

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # --- start the SSE server
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
        # process event to synchronize server startups, wait for SSE server to be ready
        logger.warning("We run under Werkzeug, so we are in the reloaded subprocess")
        sse_ready_event = Event()
        sse_process = Process(target=start_sse, daemon=True, args=(sse_ready_event,))
        sse_process.start()
        global_pid = sse_process.pid  # Store PID in the global variable
        logging.info(f"SSE -- Started SSE server process with PID: {global_pid}")
        sse_ready_event.wait() # wait for the server to be ready
        logger.warning("Starting Flask app")
    # Start the Flask application in multiple thread, one is the sse stream
    app.run(host='0.0.0.0', port=socketNr, threaded=True, debug=False)
~~~~
