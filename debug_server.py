import logging
import urllib2
from wsgiref.simple_server import make_server

PORT = 5050

GET_BODY = """This is a simple echo webserver that
logs data submitted by POST request. Use this
for debugging GAE python code (as GAE restricts writes).

Usage:
=====

Run server:

    python debug_server.py

In your code just put somewhere:

    from debug_server import debug
    debug(your_data)

Then check ``debug.log`` in the same folder as ``debug_server.py``

    tail -f debug.log

"""


logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def debug(data):
    urllib2.urlopen(urllib2.Request('http://localhost:5050',
                                    'a={0}'.format(data)))


def test_app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            request_body = "0"
        try:
            response_body = request_body[request_body.find('=') + 1:]
            logging.debug(response_body)
        except:
            response_body = "error"
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [response_body]
    else:  # GET request
        response_body = GET_BODY
        status = '200 OK'
        headers = [('Content-type', 'text/plain'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]


def start_server():
    """Start the server."""
    httpd = make_server("", PORT, test_app)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        exit('\nServer stopped by user')

if __name__ == "__main__":
    start_server()
