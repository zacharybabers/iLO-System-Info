import requests
import warnings
from .functions import basic_request
from .functions import get_processor_objects
from .functions import print_processor_info

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)

for processor in get_processor_objects(ip, username, password):
    print_processor_info(processor)

# get all the information
