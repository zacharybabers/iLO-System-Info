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

for storage in get_storage_objects(ip, username, password):
    for drive in get_drive_objects(ip, username, password, storage):
        print_drive_info(drive)

# get all the information
