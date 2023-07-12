import requests
import warnings
import sys
from .functions import basic_request
from .functions import adapter_info_dump
from .functions import drive_info_dump
from .functions import mem_info_dump
from .functions import processor_info_dump
from .functions import model_info_dump

ip = input("Enter iLO IP: ")
username = input("Enter iLO Username: ")
password = input("Enter iLO Password: ")

response = basic_request(ip, username, password, "/redfish/v1/Systems")

if response.status_code == 200:
    print("Response Successful \n")
else:
    print("response unsuccessful with status code: \n", response.status_code)
    sys.exit()

optionsString = "What information do you want printed? \nOptions: \nmemory, cpu, network, storage, all \n"
printMode = input(optionsString)

print(model_info_dump(ip, username, password))
gotOut = False
if printMode == "memory" or printMode == "all":
    gotOut = True
    print(mem_info_dump(ip, username, password))
if printMode == "cpu" or printMode == "all":
    gotOut = True
    print(processor_info_dump(ip, username, password))
if printMode == "network" or printMode == "all":
    gotOut = True
    print(adapter_info_dump(ip, username, password))
if printMode == "storage" or printMode == "all":
    gotOut = True
    print(drive_info_dump(ip, username, password))

if not gotOut:
    print("invalid print mode")


# TODO ADD MULTIPLE LANES OF SELECTION TO PROGRAM