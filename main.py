import requests

ip = input("enter redfish ip")
username = input("enter username")
password = input("enter password")

response = (requests.get("http://" + ip + "/redfish/v1/Systems/1", auth=(username, password)))

if response.status_code == 200:
    print("Response Successful")
    print(response.text)
else:
    print("response unsuccessful with status code: ", response.status_code)


