import requests
import warnings
from .functions import basic_request
from .functions import get_adapter_objects
from .functions import print_adapter_info

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)

adapters = get_adapter_objects(ip, username, password)
for adapter in adapters:
    print_adapter_info(adapter)

# get all the information
