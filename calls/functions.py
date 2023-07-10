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

def get_processorIDs(ip, username, password):
    processorIDs = []
    processors = json.loads(basic_request(ip, username, password, "/redfish/v1/Systems/1/Processors").text)
    for processor in processors['Members']:
        processorIDs.append(processor['@odata.id'])
    return processorIDs

def get_processor_objects(ip, username, password):
    processors = []
    processorIDs = get_processorIDs(ip, username, password)
    for id in processorIDs:
        processors.append(json.loads(basic_request(ip, username, password, id).text))
    return processors

def print_processor_info(processor):
    infoString = ""
    infoString += "Model: " + processor['Model'] + "\n"
    infoString += "Socket: " + processor['Socket'] + "\n"
    infoString += "Total Cores: " + str(processor['TotalCores']) + "\n"
    infoString += "Total Threads: " + str(processor['TotalThreads']) + "\n"
    infoString += "Instruction Set: " + processor['InstructionSet'] + "\n"
    print(infoString)

def get_storageIDs(ip, username, password):
    storageIDs = []
    storages = json.loads(basic_request(ip, username, password, "/redfish/v1/Systems/1/Storage").text)
    for storage in storages['Members']:
        storageIDs.append(storage['@odata.id'])
    return storageIDs

def get_storage_objects(ip, username, password):
    storage = []
    storageIDs = get_storageIDs(ip, username, password)
    for id in storageIDs:
        storage.append(json.loads(basic_request(ip, username, password, id).text))
    return storage

def get_driveIDs(storage):
    driveIDs = []
    for drive in storage['Drives']:
        driveIDs.append(drive['@odata.id'])
    return driveIDs

def get_drive_objects(ip, username, password, storage):
    drives = []
    driveIDs = get_driveIDs(storage)
    for id in driveIDs:
        drives.append(json.loads(basic_request(ip, username, password, id).text))
    return drives

    
