import warnings
import requests
import json

def basic_request(ip, username, password, redfish_item):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = (requests.get("https://" + ip + "/redfish/v1/" + redfish_item, auth=(username, password), verify=False))
    return response

def print_systems(ip, username, password):
    systems = json.loads(basic_request(ip,username,password,"Systems").text)
    for member in systems['Members']:
        print(member['@odata.id'])
