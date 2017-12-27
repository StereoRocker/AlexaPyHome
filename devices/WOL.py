import sys, struct, socket

# Configuration variables
broadcast = '255.255.255.255'
wol_port = 9

# Helper functions
def WakeOnLan(macaddress):

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (broadcast, wol_port))

# Class definition
class WOL:
    # Instance variables:
    # endpoint:         String, set by config.py at startup, should never be modified by the class
    # friendly_name:    String, set by the constructor called in config.py, should never be modified by the class

    # Class constructor:
    # self, and friendly_name are required
    # Other parameters may be added to the constructor
    def __init__(self, friendly_name, macaddress):
        # DO NOT CHANGE
        self.friendly_name = friendly_name

        # Your constructor code here
        self.macaddress = macaddress

    # Constructs an Alexa device descriptor
    def GetDeviceDescriptor(self):
        device = {
            # DO NOT CHANGE
            "endpointId": self.endpoint,
            "friendlyName": self.friendly_name,

            # Customise to this type of device
            "manufacturerName": "StereoRocker",
            "description": "Wake-on-LAN capable device",
            "displayCategories": ["SMARTPLUG"],
            "capabilities": [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PowerController",
                "version": "3",
                "properties": {
                    "supported": [
                        {"name": "powerState"}
                    ],
                    "proactivelyReported": False,
                    "retrievable": False
                }
            }
            ]
        }
        return device

    # Handles a Power On request, returns success as boolean
    def PowerOn(self):
        # Code to power on your device here

        WakeOnLan(self.macaddress)
        return True

    # Handles a Power Off request, returns success as boolean
    def PowerOff(self):
        # Code to power off your device here

        # There's no Shutdown-on-LAN packets, thankfully, so do nothing
        return True
