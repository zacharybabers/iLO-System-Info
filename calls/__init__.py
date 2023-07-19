import getpass
import sys
from .util_functions import get_ips
from .redfish_functions import basic_request
from .redfish_functions import adapter_info_dump
from .redfish_functions import drive_info_dump
from .redfish_functions import mem_info_dump
from .redfish_functions import processor_info_dump
from .redfish_functions import model_info_dump
from .redfish_functions import get_network_interface_count
from .redfish_functions import get_nic_pci_address


ipList = get_ips(input("Enter iLO IPs: "))
username = input("Enter iLO Username: ")
password = getpass.getpass("Enter iLO Password: ")

responses = []
for ip in ipList:
    responses.append(basic_request(ip, username, password, "/redfish/v1/Systems"))

for i in range(0, len(responses)):
    if(not responses[i].status_code == 200):
        print("response unsuccesful from ip " + ipList[i] +". Exiting the program")
        sys.exit()

print("responses successful")
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
    print("Network Interface Count: " + str(get_network_interface_count(ip, username, password)) + "\n")
    for address in get_nic_pci_address(ip, username, password):
        print(address + "\n")
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
    for address in get_nic_pci_address(ip, username, password):
        print(address + "\n")
    print("Drives: \n")
    print(drive_info_dump(ip, username, password))
# elif printMode == "dev":
#     print(str(get_nic_pci_address(ip, username, password)))
else:
    print("Invalid Print Mode")