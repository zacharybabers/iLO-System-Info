import requests
import warnings
from .functions import basic_request

ip = input("enter redfish ip")
username = input("enter username")
password = input("enter password")

response = basic_request(ip, username, password, "Systems/1")

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)


# get all the information
