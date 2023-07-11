import requests
import warnings
from .functions import basic_request
from .functions import adapter_info_dump
from .functions import drive_info_dump
from .functions import mem_info_dump
from .functions import processor_info_dump
from .functions import get_model_name

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful \n")
else:
    print("response unsuccessful with status code: \n", response.status_code)

print(get_model_name(ip, username, password))
print(mem_info_dump(ip, username, password))
print(processor_info_dump(ip, username, password))
print(adapter_info_dump(ip, username, password))
print(drive_info_dump(ip, username, password))