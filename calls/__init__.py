import requests
import warnings
from .functions import basic_request
from .functions import get_driveIDs
from .functions import get_storage_objects

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)

print(get_driveIDs(get_storage_objects(ip, username, password)[0]))

# get all the information
