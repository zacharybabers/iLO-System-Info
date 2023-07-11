import requests
import warnings
from .functions import basic_request
from .functions import get_adapter_objects
from .functions import get_adapter_ports

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
    print(get_adapter_ports(adapter)[0])

# get all the information
