import requests

ip = input("enter redfish ip")
username = input("enter username")
password = input("enter password")

response = (requests.get("https://" + ip + "/redfish/v1/Systems/1", auth=(username, password), verify=False))

if response.status_code == 200:
    print("Response Successful")
else:
    print("response unsuccessful with status code: ", response.status_code)


# get all the information
