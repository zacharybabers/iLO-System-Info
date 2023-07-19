import requests
import warnings
import sys
from .functions import basic_request
from .functions import adapter_info_dump
from .functions import drive_info_dump
from .functions import mem_info_dump
from .functions import processor_info_dump
from .functions import model_info_dump
from .functions import interface_info_dump
from .functions import get_network_interface_count
from .functions import get_nic_pci_address

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

print("\n")
print(model_info_dump(ip, username, password))

if printMode == "memory":
    print(mem_info_dump(ip, username, password))
elif printMode == "cpu":
    print(processor_info_dump(ip, username, password))
elif printMode == "network":
    print(adapter_info_dump(ip, username, password))
    print("Network Interface Count: " + str(get_network_interface_count(ip, username, password)))
    print(interface_info_dump(ip, username, password))
elif printMode == "storage":
    print(drive_info_dump(ip, username, password))
elif printMode == "all":
    print("Memory: \n")
    print(mem_info_dump(ip, username, password))
    print("Processors: \n")
    print(processor_info_dump(ip, username, password))
    print("Network Adapters: \n")
    print(adapter_info_dump(ip, username, password))
    print("Network Interfaces: \n")
    print(interface_info_dump(ip, username, password))
    print("Drives: \n")
    print(drive_info_dump(ip, username, password))
elif printMode == "dev":
    print(str(get_nic_pci_address(ip, username, password)))
else:
    print("Invalid Print Mode")