import pytest
import sys
from os.path import dirname, join, abspath
import logging
from multiprocessing import Process, Event
import flask
import requests
import time

# -- local imports
from flask_sse.routes import setup_sse_listen, stream
from flask_sse.manager import start_sse

# Add the root project folder to the python path, so that the tests can import the app
this_dir = dirname(__file__)
sys.path.insert(0, abspath(join(this_dir, "..")))

# logging
# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

global_pid = None  # Define the global variable outside the function

def start_flask_server(sse_ready_event):
    app = flask.Flask(__name__)
    sse_manager = setup_sse_listen(app)  # Setup SSE listening route

    # Define the SSE endpoint route
    @app.route('/events')
    def events():
        """SSE endpoint for both pings and name changes."""
        return flask.Response(stream(sse_manager), mimetype='text/event-stream')

    sse_ready_event.set()  # Indicate the Flask server is ready
    app.run(host='0.0.0.0', port=5050, threaded=True, debug=False)

@pytest.fixture(scope="module")
def sse_server():
    sse_ready_event = Event()
    sse_process = Process(target=start_sse, daemon=True, args=(sse_ready_event,))
    sse_process.start()
    global global_pid
    global_pid = sse_process.pid  # Store PID in the global variable
    logging.info(f"SSE -- Started SSE server process with PID: {global_pid}")
    sse_ready_event.wait()  # wait for the server to be ready
    yield
    sse_process.terminate()
    sse_process.join()

@pytest.fixture(scope="module")
def flask_server():
    flask_ready_event = Event()
    flask_process = Process(target=start_flask_server, args=(flask_ready_event,))
    flask_process.start()
    flask_ready_event.wait()  # wait for the Flask server to be ready
    yield
    flask_process.terminate()
    flask_process.join()

def test_sse(flask_server, sse_server):
    logging.info("Testing SSE server")
    
    # Give some time for the servers to start and emit events
    time.sleep(2)
    
    # Send a request to the /events endpoint
    response = requests.get('http://localhost:5050/events', stream=True)
    
    received_pings = []

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            logger.debug(f"Received: {decoded_line}")
            if "event: PING" in decoded_line:
                received_pings.append(decoded_line)
            if len(received_pings) >= 3:  # Check for three pings
                break

    assert len(received_pings) >= 3
    logger.info("Received pings as expected")

if __name__ == '__main__':
    pytest.main(['-s', '--log-cli-level=DEBUG'])
