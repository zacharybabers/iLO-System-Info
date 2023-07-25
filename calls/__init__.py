import getpass
import sys
import pandas as pd
from .util_functions import get_ips
from .util_functions import process_file
from .util_functions import df_list
from .util_functions import build_list
from .redfish_functions import basic_request
from .system_classes import populate_system


pie = "hi"
df = pd.DataFrame({'year': [2015, 2016],
                   'month': [2, 3],
                   'day': [4, 5]})

pd.to_datetime(df)

num_arguments = len(sys.argv) - 1
ipList = []
username = ""
password = ""

if num_arguments == 0:
    ipList = get_ips(input("Enter iLO IPs: "))
    username = input("Enter iLO Username: ")
    password = getpass.getpass("Enter iLO Password: ")
elif num_arguments == 1:
    credentials = process_file(sys.argv[1])
    ipList = get_ips(credentials[0])
    username = credentials[1]
    password = credentials[2]
else:
    print("Invalid num arguments")
    sys.exit()



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
lst = build_list(servers)
print(df_list(lst).to_string(justify='left', index=False))