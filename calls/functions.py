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

def print_drive_info(drive):
    # name
    infoString = ""
    infoString += "Name: " + drive['Name'] + "\n"
    capacityBytes = drive['CapacityBytes']
    infoString += "Capacity Bytes: " + str(drive['CapacityBytes']) + "\n"
    if(type(capacityBytes) == int):
        capacityGB = capacityBytes / 1000 / 1000 / 1000
        infoString += "Capacity GB: " + str(capacityGB) + "\n"
    infoString += "Physical Location: " + drive['PhysicalLocation']['PartLocation']['ServiceLabel'] + "\n"
    infoString += "Ordinal Location: " + str(drive['PhysicalLocation']['PartLocation']['LocationOrdinalValue']) + "\n"
    print(infoString)

# Network Interface functions; there are currently no network interfaces being returned by our iLO, so I will just display the number of network interfaces so it is apparent if/when this functionality needs to be added
def get_network_interface_count(ip, username, password):
    interfaces = json.loads(basic_request(ip, username, password, "/redfish/v1/Systems/1/NetworkInterfaces").text)
    return interfaces['Members@odata.count']

####
def get_adapterIDs(ip, username, password):
    adapters = json.loads(basic_request(ip, username, password, "/redfish/v1/Systems/1/BaseNetworkAdapters").text)
    adapterIDs = []
    for id in adapters['Members']:
        adapterIDs.append(id['@odata.id'])
    return adapterIDs

def get_adapter_objects(ip, username, password):
    adapters = []
    adapterIDs = get_adapterIDs(ip, username, password)
    for id in adapterIDs:
        adapters.append(json.loads(basic_request(ip, username, password, id).text))
    return adapters


    
