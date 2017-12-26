#!/usr/bin/env python3

# Imports
import time
import json
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from config import *

# Helper functions
def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())

# Endpoint handlers
def invalid_handler(handler):
    # Send response status code
    handler.send_response(404)
    
    # Send headers
    handler.send_header('Content-type','text/plain')
    handler.end_headers()

    # Send content
    response = "Invalid endpoint"
    handler.wfile.write(bytes(response, "utf8"))
    return

def discover(handler):
    # Send response status code
    handler.send_response(200)

    # Send headers
    handler.send_header('Content-type','application/json')
    handler.end_headers()

    # Generate JSON content

    devices = []
    for device in endpoints:
        devices.append(device.GetDeviceDescriptor())
    
    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": get_uuid()
            },
            "payload": {
                "endpoints": devices
            }
        }
    }

    # Write JSON response
    jsontext = json.dumps(response)
    handler.wfile.write(bytes(jsontext, "utf8"))
    return

endpoints = {"default": invalid_handler, "/discover": discover}

# HTTPRequestHandler class
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        # Call handler
        handler = endpoints.get(self.path, endpoints["default"])
        handler(self)
        return

def run():
    print("Starting server")

    # Server settings
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    httpd.serve_forever()

try:
    run()
except:
    print("Server stopped")
