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
    systemIDs = []
    for member in systems['Members']:
        systemIDs.append(member['@odata.id'])
    return systemIDs

def get_system_objects(ip, username, password):
    systems = []
    systemIDs = get_systemIDs(ip, username, password)
    for systemID in systemIDs:
        systems.append(json.loads(basic_request(ip, username, password, systemID).text))
    return systems


def get_memory_info(ip, username, password):
    memorySums = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        memorySums.append(system['MemorySummary'])
    return memorySums

# A memory summary looks like:
# {'Status': {'HealthRollup': 'OK'}, 'TotalSystemMemoryGiB': x, 'TotalSystemPersistentMemoryGiB': 0}


def get_model_name(ip,username,password):
    names = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        names.append(system['Model'])
    return names

def get_cpu_summary(ip, username, password):
    cpuSums = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        cpuSums.append(system['ProcessorSummary'])
    return cpuSums
# A cpu summary looks like:
# {'Count': 2, 'Model': 'Vendor(R) CPU(R) Gold xN CPU @ x.xGHz', 'Status': {'HealthRollup': 'OK'}}