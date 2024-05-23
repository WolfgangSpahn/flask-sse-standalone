import os
import logging
from multiprocessing import Process, Event

import flask


# -- local imports

from flask_sse.routes import setup_sse_listen, stream
from flask_sse.manager import start_sse

logger = logging.getLogger(__name__)

# --- Flask and SSE setup
app = flask.Flask(__name__)
sse_manager = setup_sse_listen(app)  # Setup SSE listening route

# Define the SSE endpoint route
# test with
# curl -X GET http://localhost:5050/events
@app.route('/events')
def events():
    """SSE endpoint for both pings and name changes."""
    return flask.Response(stream(sse_manager), mimetype='text/event-stream')

if __name__ == '__main__':
    # --- start the SSE server
    sse_ready_event = Event()
    sse_process = Process(target=start_sse, daemon=True, args=(sse_ready_event,))
    sse_process.start()
    global_pid = sse_process.pid  # Store PID in the global variable
    logging.info(f"SSE -- Started SSE server process with PID: {global_pid}")
    sse_ready_event.wait() # wait for the server to be ready
    logger.warning("Starting Flask app")
    # Start the Flask application in a separate thread
    app.run(host='0.0.0.0', port=5050, threaded=True, debug=False)