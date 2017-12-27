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

def FunctionExists(obj, method):
    if hasattr(obj, method) and callable(getattr(obj, method)):
        return True
    else:
        return False

# Endpoint handlers
def invalid_handler(handler, data):
    # Send response status code
    handler.send_response(404)
    
    # Send headers
    handler.send_header('Content-type','text/plain')
    handler.end_headers()

    # Send content
    response = "Invalid endpoint"
    handler.wfile.write(bytes(response, "utf8"))
    return

def discover(handler, data):
    # Send response status code
    handler.send_response(200)

    # Send headers
    handler.send_header('Content-type','application/json')
    handler.end_headers()

    # Generate JSON content

    devices = []
    for device in device_instances:
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

def power(handler, data):
    # Send response
    handler.send_response(200)

    # Send headers
    handler.send_header('Content-type','application/json')
    handler.end_headers()

    # Parse data
    request = json.loads(data.decode("utf8"))

    # Get device
    device = None
    for obj in device_instances:
        if obj.endpoint == request["directive"]["endpoint"]["endpointId"]:
            device = obj

    # Figure out which function to call
    funcname = request["directive"]["header"]["name"]
    result = False
    state = None
    
    if funcname == "TurnOn":
        if FunctionExists(device, "PowerOn"):
            result = device.PowerOn()
        if result == True:
            state = "ON"
        else:
            state = "OFF"

    if funcname == "TurnOff":
        if FunctionExists(device, "PowerOff"):
            result = device.PowerOff()
        state = "OFF"

    # Generate response
    response = {
        "context": {
            "properties": [{
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": state,
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 500
            }]
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "payloadVersion": "3",
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"]
            },
            "endpoint": {
                "endpointId": device.endpoint,
                "scope": {
                    "token": "access-token-from-Amazon",
                    "type": "BearerToken"
                }
            }
        },
        "payload": {}
    }

    # Write JSON response
    jsontext = json.dumps(response)
    handler.wfile.write(bytes(jsontext, "utf8"))

endpoints = {"default": invalid_handler, "/discover": discover, "/power": power}

# HTTPRequestHandler class
class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):

        # Call handler
        handler = endpoints.get(self.path, endpoints["default"])
        handler(self, None)
        return

    # POST
    def do_POST(self):
        # Call handler
        handler = endpoints.get(self.path, endpoints["default"])
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        handler(self, data_string)
        return
        

def run():
    print("Starting server")

    # Server settings
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    httpd.serve_forever()

try:
    # Configure devices
    configure()

    # Run server
    run()
except:
    print("Server stopped")
