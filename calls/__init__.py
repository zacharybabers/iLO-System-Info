import getpass
import sys
import pandas as pd
import argparse
from .util_functions import get_ips
from .util_functions import process_file
from .util_functions import df_list
from .util_functions import build_list
from .redfish_functions import basic_request
from .system_classes import populate_system

ipList = []
username = ""
password = ""
printMode = ""

parser = argparse.ArgumentParser(description="This program gets information from HP and Dell lights out (iLO/iDRAC)")
parser.add_argument('-i', '--ip', type=str, help='Input a list of IPs (comma delimited). Can input a range of ips ie XXX.XXX.XXX.11-13')
parser.add_argument('-u', '--username', type=str, help='Input credentials for lights out utility in format username:password')
parser.add_argument('-m', '--mode', type=str, help='Input return mode for information. Modes: table, detailed')

args = parser.parse_args()


ipString = args.ip
username = args.username.split(':')[0]
password = args.username.split(':')[1]
printMode = args.mode

if(ipString == None):
    print("No ip given. Provide ip with -i")
if(username == None):
    print("No username given. Provide credentials with -u")
if(password == None):
    print("No password given. Provide credentials with -u")
if(printMode == None):
    print("No mode given. Provide mode with -m")

ipList = get_ips(ipString)

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
    servers.append(populate_system(ip, username, password))

if printMode == "table":
    lst = build_list(servers)
    print(df_list(lst).to_string(index=False))
elif printMode == "detailed":
    for server in servers:
        print("Server at IP " + ip + ": \n")
        print(server)
else:
    print("Invalid print mode.")
