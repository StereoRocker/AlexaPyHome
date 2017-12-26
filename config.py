# DO NOT MODIFY

# Import all files in the devices/ directory
from devices import *

# Define an array
endpoints = []

# Add your own devices here

endpoints.append(reference.Reference_Device("reference"))

# DO NOT MODIFY
def configure():
    for i, obj in enumerate(endpoints):
        obj.endpoint = str(i)
