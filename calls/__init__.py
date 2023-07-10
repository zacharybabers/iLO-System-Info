import requests
import warnings
from .functions import basic_request
from .functions import get_drive_objects
from .functions import get_storage_objects
from .functions import print_drive_info

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)

print_drive_info(get_drive_objects(ip, username, password, get_storage_objects(ip, username, password)[0])[0])

# get all the information
