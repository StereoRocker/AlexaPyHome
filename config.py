# DO NOT MODIFY

# Import all files in the devices/ directory
from devices import *

# Define an array
device_instances = []

# Add your own devices here

#device_instances.append(reference.Reference_Device("reference"))
device_instances.append(WOL.WOL("Atlas", "00:1C:C0:BE:57:46"))

# DO NOT MODIFY
def configure():
    for i, obj in enumerate(device_instances):
        obj.endpoint = str(i)
        
