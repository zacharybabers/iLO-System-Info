import requests
import warnings
from .functions import basic_request
from .functions import get_adapter_objects
from .functions import get_adapter_info
from .functions import get_drive_info
from .functions import get_drive_objects

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful \n")
else:
    print("response unsuccessful with status code: \n", response.status_code)

adapters = get_adapter_objects(ip, username, password)
for adapter in adapters:
    print(get_adapter_info(adapter))

drives = get_drive_objects(ip, username, password)
for drive in drives:
    print(get_drive_info(drive))
# get all the information
