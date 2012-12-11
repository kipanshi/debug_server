============
DEBUG SERVER
============

This is a simple echo webserver that
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
