import getpass
import sys
import pandas as pd
import time
from .util_functions import get_ips
from .util_functions import process_file
from .util_functions import df_list
from .util_functions import build_list
from .redfish_functions import basic_request
from .system_classes import populate_system

num_arguments = len(sys.argv) - 1
ipList = []
username = ""
password = ""
printMode = ""

if num_arguments == 0:
    ipList = get_ips(input("Enter iLO IPs: "))
    username = input("Enter iLO Username: ")
    password = getpass.getpass("Enter iLO Password: ")
    printMode = input("Enter print mode (table, detailed): ")
elif num_arguments == 1:
    credentials = process_file(sys.argv[1])
    ipList = get_ips(credentials[0])
    username = credentials[1]
    password = credentials[2]
    printMode = credentials[3]
else:
    print("Invalid num arguments")
    sys.exit()

ipList = sorted(ipList, key=lambda ip: [int(num) for num in ip.split('.')])

responses = []
for ip in ipList:
    responses.append(basic_request(ip, username, password, "/redfish/v1/Systems"))

for i in range(0, len(responses)):
    if(not responses[i].status_code == 200):
        print("response unsuccesful from ip " + ipList[i] +". Response code: " + str(responses[i].status_code) +  ". Exiting the program")
        sys.exit()

print("All redfish responses successful.")

print("\n")


servers = []
for ip in ipList:
    startTime = time.time()
    servers.append(populate_system(ip, username, password))
    endTime = time.time()

    executionTime = endTime - startTime
    
    print("Populated information for server at ip " + ip + " in " + executionTime)

if printMode == "table":
    lst = build_list(servers)
    print(df_list(lst).to_string(index=False))
elif printMode == "detailed":
    for server in servers:
        print("Server at IP " + ip + ": \n")
        print(server)
else:
    print("Invalid print mode.")
