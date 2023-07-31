import warnings
import requests
import json

class CachedRequester:
    _cache = {}

    @staticmethod
    def cachedRequest(url, username, password):
        if url in CachedRequester._cache:
            return CachedRequester._cache[url]
        else:
            response = requests.get(url, auth=(username, password), verify=False, timeout=5)
            CachedRequester._cache[url] = response
            return response

def basic_request(ip, username, password, redfish_item):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        url = "https://" + ip + redfish_item
        response = (CachedRequester.cachedRequest(url, username, password))
    return response

def get_chassisIDs(ip, username, password):
    chassis = json.loads(basic_request(ip, username, password, "/redfish/v1/Chassis").text)
    chassisIDs = []
    for member in chassis['Members']:
        chassisIDs.append(member['@odata.id'])
    return chassisIDs

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


def get_memory_sums(ip, username, password):
    memorySums = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        memorySums.append(system['MemorySummary'])
    return memorySums

# A memory summary looks like:
# {'Status': {'HealthRollup': 'OK'}, 'TotalSystemMemoryGiB': x, 'TotalSystemPersistentMemoryGiB': 0}

def get_memory_info(memorySum):
    infoString = ""
    infoString += "Status: " + memorySum['Status']['HealthRollup'] + "\n"
    infoString += "Total System Memory: " + str(memorySum['TotalSystemMemoryGiB']) + "\n"
    infoString += "Total System Persistent Memory: " + str(memorySum['TotalSystemPersistentMemoryGiB']) + "\n"
    return infoString

def mem_info_dump(ip, username, password):
    out = ""
    sums = get_memory_sums(ip, username, password)
    for sum in sums:
        out += get_memory_info(sum)
    return out

def get_model_name(ip,username,password):
    names = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        names.append(system['Model'])
    return names

def model_info_dump(ip, username, password):
    names = get_model_name(ip, username, password)
    out = ""
    for name in names:
        out += name + "\n"
    return out

def get_cpu_summary(ip, username, password):
    cpuSums = []
    systems = get_system_objects(ip, username, password)
    for system in systems:
        cpuSums.append(system['ProcessorSummary'])
    return cpuSums
# A cpu summary looks like:
# {'Count': 2, 'Model': 'Vendor(R) CPU(R) Gold xN CPU @ x.xGHz', 'Status': {'HealthRollup': 'OK'}}

def get_processorIDs(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    processorIDs = []
    processors = json.loads(basic_request(ip, username, password, systemID + "/Processors").text)
    for processor in processors['Members']:
        processorIDs.append(processor['@odata.id'])
    return processorIDs

def get_processor_objects(ip, username, password):
    processors = []
    processorIDs = get_processorIDs(ip, username, password)
    for id in processorIDs:
        processors.append(json.loads(basic_request(ip, username, password, id).text))
    return processors

def get_processor_info(processor):
    infoString = ""
    infoString += "Model: " + processor['Model'] + "\n"
    infoString += "Socket: " + processor['Socket'] + "\n"
    infoString += "Total Cores: " + str(processor['TotalCores']) + "\n"
    infoString += "Total Threads: " + str(processor['TotalThreads']) + "\n"
    if('InstructionSet' in processor.keys()):
        infoString += "Instruction Set: " + processor['InstructionSet'] + "\n"
    else:
        infoString += "Instruction set unavailable \n"
    return(infoString)

def processor_info_dump(ip, username, password):
    processors = get_processor_objects(ip, username, password)
    out = ""
    for processor in processors:
        out += get_processor_info(processor)
    return out

def get_storageIDs(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    storageIDs = []
    storages = json.loads(basic_request(ip, username, password, systemID + "/Storage").text)
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

def get_drive_info(drive):
    infoString = ""
    infoString += "Name: " + drive['Name'] + "\n"
    capacityBytes = drive['CapacityBytes']
    infoString += "Capacity Bytes: " + str(drive['CapacityBytes']) + "\n"
    if(type(capacityBytes) == int):
        capacityGB = capacityBytes / 1000 / 1000 / 1000
        infoString += "Capacity GB: " + str(capacityGB) + "\n"
    infoString += "Physical Location: " + drive['PhysicalLocation']['PartLocation']['ServiceLabel'] + "\n"
    infoString += "Ordinal Location: " + str(drive['PhysicalLocation']['PartLocation']['LocationOrdinalValue']) + "\n"
    return(infoString)

def drive_info_dump(ip, username, password):
    storages = get_storage_objects(ip, username, password)
    out = ""
    for storage in storages:
        drives = get_drive_objects(ip, username, password, storage)
        for drive in drives:
            out += get_drive_info(drive)
    return out

# Network Interface functions; there are currently no network interfaces being returned by our iLO, so I will just display the number of network interfaces so it is apparent if/when this functionality needs to be added
def get_network_interface_count(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    interfaces = json.loads(basic_request(ip, username, password, systemID + "/NetworkInterfaces").text)
    return interfaces['Members@odata.count']

def get_interfaceIDs(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    interfaces = json.loads(basic_request(ip, username, password, systemID + "/NetworkInterfaces").text)
    driveIDs = []
    for id in interfaces['Members']:
        driveIDs.append(id['@odata.id'])
    return driveIDs

def get_interface_objects(ip, username, password):
    interfaces = []
    interfaceIDs = get_interfaceIDs(ip, username, password)
    for id in interfaceIDs:
        interfaces.append(json.loads(basic_request(ip, username, password, id).text))
    return interfaces

def interface_info_dump(ip, username, password):
    interfaces = get_interface_objects(ip, username, password)
    infoString = ""
    for interface in interfaces:
        infoString+="Interface Name: " + interface["Name"] + "\n"
    return infoString

def get_adapterIDs(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    system = json.loads(basic_request(ip, username, password, systemID).text)
    adapterIDs = []
    dell = system.get('Oem').get('Hpe', 'Unavailable') == 'Unavailable'
    if dell:
        chassisID = get_chassisIDs(ip, username, password)[0]
        adapters = json.loads(basic_request(ip,username,password, chassisID + "/NetworkAdapters").text)
        viewIDs = []
        for id in adapters['Members']:
            viewIDs.append(id['@odata.id'])
        for viewID in viewIDs:
            networkFunctions = json.loads(basic_request(ip, username, password, viewID + "/NetworkDeviceFunctions").text)
            for id in networkFunctions['Members']:
                adapterIDs.append(id['@odata.id'])
    else:
        adapters = json.loads(basic_request(ip, username, password, systemID + "/BaseNetworkAdapters").text)
        for id in adapters['Members']:
            adapterIDs.append(id['@odata.id'])
    return adapterIDs

def get_adapter_objects(ip, username, password):
    adapters = []
    adapterIDs = get_adapterIDs(ip, username, password)
    for id in adapterIDs:
        adapters.append(json.loads(basic_request(ip, username, password, id).text))
    return adapters

def get_adapter_ports(adapter):
    ports = adapter.get('PhysicalPorts', [])
    return ports

def get_port_info(port):
    infoString = ""
    ipv4 = port['IPv4Addresses']
    if(len(ipv4) > 0):
        for address in ipv4:
            infoString += "IPV4 Address: " + str(address) + "\n"
    else:
        infoString += "IPV4 Address: None \n"
    ipv6 = port['IPv6Addresses']
    if(len(ipv6) > 0):
        for address in ipv6:
                infoString += "IPV6 Address: " + str(address) + "\n"
    else:
        infoString += "IPV6 Address: None \n"
    infoString += "Mac Address: " + str(port['MacAddress']) + "\n"
    infoString += "Speed Mbps: " + str(port['SpeedMbps']) + "\n"
    return(infoString)

def get_adapter_info(adapter):
    infoString = ""
    infoString += "Name: " + adapter['Name'] + "\n"
    infoString += "ID: " + str(adapter['Id']) + "\n"
    infoString += "Location: " + adapter['Location'] + "\n"
    ports = get_adapter_ports(adapter)
    for port in ports:
        infoString += "Port \n"
        infoString += get_port_info(port)
    return infoString

def adapter_info_dump(ip, username, password):
    adapters = get_adapter_objects(ip, username, password)
    out = ""
    for adapter in adapters:
        out += get_adapter_info(adapter)
    return out
    
def get_pciIDs(ip, username, password):
    systems = get_systemIDs(ip, username, password)
    systemID = systems[0]
    devices = json.loads(basic_request(ip, username, password, systemID + "/pcidevices").text)
    deviceIDs = []
    for id in devices['Members']:
        deviceIDs.append(id['@odata.id'])
    return deviceIDs

def get_pci_objects(ip, username, password):
    devices = []
    IDs = get_pciIDs(ip, username, password)
    for id in IDs:
        devices.append(json.loads(basic_request(ip, username, password, id).text))
    return devices

def get_nic_pci_address(ip, username, password):
    devices = get_pci_objects(ip, username, password)
    nics = []
    for device in devices:
        if(device['DeviceType'] == 'NIC'):
            nics.append(device)
    out = []
    for nic in nics:
        pcistring = ""
        pcistring += "0000:"
        pcistring += hex(nic['BusNumber'])[2:] + ":"
        pcistring += hex(nic['DeviceNumber'])[2:] + "."
        pcistring += hex(nic['FunctionNumber'])[2:]
        out.append(nic['Name'] + " PCI Address: " + pcistring)
    return out

def server_is_dell(ip, username, password):
    system = get_system_objects(ip, username, password)[0]
    if system.get('Oem').get('Hpe', 'Unavailable') == 'Unavailable':
        return True
    return False

    
