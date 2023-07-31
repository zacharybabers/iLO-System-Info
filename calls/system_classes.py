
from .redfish_functions import get_adapter_ports
from .redfish_functions import get_memory_sums
from .redfish_functions import get_processor_objects
from .redfish_functions import get_storage_objects
from .redfish_functions import get_drive_objects
from .redfish_functions import get_adapter_objects
from .redfish_functions import get_pci_objects
from .redfish_functions import get_network_interface_count
from .redfish_functions import get_model_name
from .redfish_functions import server_is_dell

class ComputerSystem:
    def __init__(self, ip, model, memInfo, processors, drives, nics, interfaceCount):
        self.ip = ip
        self.model = model
        self.memoryInfo = memInfo
        self.processorList = processors
        self.driveList = drives
        self.networkAdapterList = nics
        self.networkInterfaceCount = interfaceCount

    def get_cpu_sum(self):
        cpuSum = dict()
        cpuSum['cpuCount'] = len(self.processorList)
        totalCores = 0
        totalThreads = 0
        for processor in self.processorList:
            totalCores += int(processor.totalCores)
            totalThreads += int(processor.totalThreads)
        cpuSum['totalCores'] = totalCores
        cpuSum['totalThreads'] = totalThreads
        return cpuSum
        


    def __str__(self):
        out = ""
        out += "Model: " + self.model + "\n\n"
        out += "Memory: \n\n"
        out += str(self.memoryInfo) + "\n"
        out += "Processors:\n\n"
        for processor in self.processorList:
            out += str(processor) + "\n"
        out += "Storage: \n\n"
        for drive in self.driveList:
            out += str(drive) + "\n"
        out += "Network: \n\n"
        for adapter in self.networkAdapterList:
            out += str(adapter) + "\n"
        out += "Network Interface Count: " + str(self.networkInterfaceCount)
        return out

class MemoryInfo:
    def __init__(self, memorySum):
        self.status = memorySum['Status'].get('HealthRollup', "Unavailable")
        self.totalMem = str(memorySum.get('TotalSystemMemoryGiB', "Unavailable"))
        self.persistentMem = str(memorySum.get('TotalSystemPersistentMemoryGiB', "Unavailable"))

    def __str__(self):
        infoString = ""
        infoString += "Status: " + self.status + "\n"
        infoString += "Total System Memory: " + self.totalMem + "\n"
        infoString += "Total System Persistent Memory: " + self.persistentMem + "\n"
        return infoString



class ProcessorInfo:
    def __init__(self, processor):
        self.model = processor.get('Model', "Unavailable")
        self.socket = processor.get('Socket', "Unavailable")
        self.totalCores = processor.get('TotalCores', "Unavailable")
        self.totalThreads = processor.get('TotalThreads', "Unavailable")
        self.instructionSet = processor.get('InstructionSet', "Unavailable")
    
    def __str__(self):
        infoString = ""
        infoString += "Model: " + self.model + "\n"
        infoString += "Socket: " + self.socket + "\n"
        infoString += "Total Cores: " + str(self.totalCores) + "\n"
        infoString += "Total Threads: " + str(self.totalThreads) + "\n"
        infoString += "Instruction Set: " + self.instructionSet + "\n"
        return(infoString)

class DriveInfo:
    def __init__(self, drive):
        self.name = drive.get('Name', "Unavailable")
        self.capacityBytes = drive.get('CapacityBytes', "Unavailable")
        self.capacityGB = "Unavailable"
        if(type(self.capacityBytes) == int):
            self.capacityGB = self.capacityBytes / 1000 / 1000 / 1000
        self.physicalLocation = drive['PhysicalLocation']['PartLocation'].get('ServiceLabel', "Unavailable")
        self.ordinalLocation = drive['PhysicalLocation']['PartLocation'].get('LocationOrdinalValue', "Unavailable")

    def __str__(self):
        infoString = ""
        infoString += "Name: " + self.name + "\n"
        infoString += "Capacity Bytes: " + str(self.capacityBytes) + "\n"
        infoString += "Capacity GB: " + str(self.capacityGB) + "\n"
        infoString += "Physical Location: " + self.physicalLocation + "\n"
        infoString += "Ordinal Location: " + str(self.ordinalLocation) + "\n"
        return(infoString)

class NetworkAdapterInfo:
    def __init__(self, adapter, devices, functionNum):
        Oem = adapter.get("Oem", "Unavailable")
        if type(Oem) == dict and not Oem.get('Dell') == None:
            self.isDell = True
            self.name = Oem.get('Dell').get('DellNIC').get('ProductName')
        else:
            self.name = adapter.get('Name', "Unavailable") 
        self.name = self.name.split(' - ')[0].strip()
        self.ID = adapter.get('Id', "Unavailable")
        self.location = adapter.get('Location', "Unavailable")
        self.ports = []
        portList = get_adapter_ports(adapter)
        for port in portList:
            self.ports.append(PortInfo(port))
        self.PciAddress = self.pciAddress(devices, functionNum, Oem)
        self.name = self.name[:40]

    def pciAddress(self, devices, functionNum, Oem):
        address = ""
        if devices == None:
            address += "0000:"
            address += hex(Oem.get('Dell').get('DellNIC').get('BusNumber', 'Unavailable'))[2:] + ":"
            address += "00."
            address += hex(functionNum)[2:]
        else:
            for device in devices:
                if device.get('Name', 'Unavailable') == self.name:
                    address += "0000:"
                    address += hex(device.get('BusNumber'))[2:] + ":"
                    address += hex(device.get('DeviceNumber'))[2:] + "."
                    address += hex(device.get('FunctionNumber'))[2:]
        if len(address) == 0:
            return "Unavailable"
        else:
            return address

    def __str__(self):
        infoString = ""
        infoString += "Name: " + self.name + "\n"
        infoString += "ID: " + str(self.ID) + "\n"
        infoString += "Location: " + self.location + "\n"
        ports = self.ports
        for port in ports:
            infoString += "Port \n"
            infoString += str(port)
        infoString += "PCI Address: " + self.PciAddress + "\n"
        return infoString


        

class PortInfo:
    def __init__(self, port):
        self.ipv4Addresses = []
        ipv4 = port.get('IPv4Addresses')
        if len(ipv4) > 0:
            for address in ipv4:
                self.ipv4Addresses.append(address)
        self.ipv6Addresses = []
        ipv6 = port.get('IPv6Addresses')
        if len(ipv6) > 0:
            for address in ipv6:
                self.ipv6Addresses.append(address)
        self.macAddress = port.get('MacAddress', "Unavailable")
        self.speedMbps = port.get('SpeedMbps', "Unavailable")

    def __str__(self):
        infoString = ""
        ipv4 = self.ipv4Addresses
        if(len(ipv4) > 0):
            for address in ipv4:
                infoString += "IPV4 Address: " + str(address) + "\n"
        else:
            infoString += "IPV4 Address: None \n"
        ipv6 = self.ipv6Addresses
        if(len(ipv6) > 0):
            for address in ipv6:
                    infoString += "IPV6 Address: " + str(address) + "\n"
        else:
            infoString += "IPV6 Address: None \n"
        infoString += "Mac Address: " + self.macAddress + "\n"
        infoString += "Speed Mbps: " + str(self.speedMbps) + "\n"
        return(infoString)

# write a function to populate a system given credentials
def populate_system(ip, username, password):

    # Model
    model = get_model_name(ip, username, password)[0]

    # Memory
    sums = get_memory_sums(ip, username, password)
    if not (len(sums) == 1):
        print(f"System at ip {ip} has wrong number of memory sums.")
    memoryInfo = MemoryInfo(sums[0])

    # CPU
    processors = []
    objs = get_processor_objects(ip, username, password)
    for obj in objs:
        processors.append(ProcessorInfo(obj))

    # Drives
    storages = get_storage_objects(ip, username, password)
    drives = []
    for storage in storages:
        for driveObject in get_drive_objects(ip, username, password, storage):
            drives.append(driveObject)
    driveInfos = []
    for drive in drives:
        driveInfos.append(DriveInfo(drive))

    # NICs
    # devices = get_pci_objects(ip, username, password)
    dell = server_is_dell(ip, username, password)
    adapters = get_adapter_objects(ip, username, password)
    nics = []
    functionNumIterator = 0
    for i in range (0, len(adapters)):
        if not dell:
            nics.append(NetworkAdapterInfo(adapters[i], get_pci_objects(ip, username, password)))
        else:
            if i > 0:
                #if this network adapters bus number equals the last one, function num iterator gets one added. Otherwise it becomes 0
                if adapters[i].get('Oem').get('Dell').get('DellNIC').get('BusNumber') == adapters[i-1].get('Oem').get('Dell').get('DellNIC').get('BusNumber'):
                    functionNumIterator = functionNumIterator + 1
                else:
                    functionNumIterator = 0
            nics.append(NetworkAdapterInfo(adapters[i], devices=None, functionNum=functionNumIterator))
        
    
    return ComputerSystem(ip, model, memoryInfo, processors, driveInfos, nics, get_network_interface_count(ip, username, password))
    
    
