# Class definition
class Reference_Device:
    # Instance variables:
    # endpoint:         String, set by config.py at startup, should never be modified by the class
    # friendly_name:    String, set by the constructor called in config.py, should never be modified by the class

    # Class constructor:
    # self, and friendly_name are required
    # Other parameters may be added to the constructor
    def __init__(self, friendly_name):
        # DO NOT CHANGE
        self.friendly_name = friendly_name

        # Your constructor code here

    # Constructs an Alexa device descriptor
    def GetDeviceDescriptor(self):
        device = {
            # DO NOT CHANGE
            "endpointId": self.endpoint,
            "friendlyName": self.friendly_name,

            # Customise to this type of device
            "manufacturerName": "StereoRocker",
            "description": "Reference implementation of a device",
            "displayCategories": [],
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
        print(self.friendly_name + ": Power on request received!")
        return True

    # Handles a Power Off request, returns success as boolean
    def PowerOff(self):
        # Code to power off your device here
        print(self.friendly_name + ": Power off request received!")
        return True
