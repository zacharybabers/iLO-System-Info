import warnings
import requests
import json

def basic_request(ip, username, password, redfish_item):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        response = (requests.get("https://" + ip + redfish_item, auth=(username, password), verify=False))
    return response

def get_systemIDs(ip, username, password):
    systems = json.loads(basic_request(ip,username,password,"/redfish/v1/Systems").text)
    systems = []
    for member in systems['Members']:
        systems.append(member['@odata.id'])
    return systems


def get_memory_info(ip, username, password):
    systems = []
    systemIDs = get_systemIDs(ip, username, password)
    for systemID in systemIDs:
        systems.append(json.loads(basic_request(ip, username, password, systemID).text))
    for system in systems:
        print(system['MemorySummary'])


