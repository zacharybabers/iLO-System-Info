
from .redfish_functions import get_adapter_ports
from .redfish_functions import get_memory_sums
from .redfish_functions import get_processor_objects
from .redfish_functions import get_storage_objects
from .redfish_functions import get_drive_objects
from .redfish_functions import get_adapter_objects
from .redfish_functions import get_pci_objects
from .redfish_functions import get_network_interface_count
from .redfish_functions import get_model_name

class ComputerSystem:
    def __init__(self, model, memInfo, processors, drives, nics, interfaceCount):
        self.model = model
        self.memoryInfo = memInfo
        self.processorList = processors
        self.driveList = drives
        self.networkAdapterList = nics
        self.networkInterfaceCount = interfaceCount

class MemoryInfo:
    def __init__(self, memorySum):
        self.status = memorySum['Status'].get('HealthRollup', "Unavailable")
        self.totalMem = str(memorySum.get('TotalSystemMemoryGiB', "Unavailable"))
        self.persistentMem = str(memorySum.get('TotalSystemPersistentMemoryGiB', "Unavailable"))


class ProcessorInfo:
    def __init__(self, processor):
        self.model = processor.get('Model', "Unavailable")
        self.socket = processor.get('Socket', "Unavailable")
        self.totalCores = processor.get('TotalCores', "Unavailable")
        self.totalThreads = processor.get('TotalThreads', "Unavailable")
        self.instructionSet = processor.get('InstructionSet', "Unavailable")

class DriveInfo:
    def __init__(self, drive):
        self.name = drive.get('Name', "Unavailable")
        self.capacityBytes = drive.get('CapacityBytes', "Unavailable")
        self.capacityGB = "Unavailable"
        if(type(self.capacityBytes) == int):
            self.capacityGB = self.capacityBytes / 1000 / 1000 / 1000
        self.physicalLocation = drive['PhysicalLocation']['PartLocation'].get('ServiceLabel', "Unavailable")
        self.ordinalLocation = drive['PhysicalLocation']['PartLocation'].get('LocationOrdinalValue', "Unavailable")

class NetworkAdapterInfo:
    def __init__(self, adapter, devices):
        self.name = adapter.get('Name', "Unavailable")
        self.ID = adapter.get('Id', "Unavailable")
        self.location = adapter.get('Location', "Unavailable")
        self.ports = []
        portList = get_adapter_ports(adapter)
        for port in portList:
            self.ports.append(PortInfo(port))
        self.pciAddress(devices)

    def pciAddress(self, devices):
        address = ""
        for device in devices:
            if device.get('name', 'unavailable') == self.name:
                print("gotem")
                address += "0000:"
                address += hex(device.get('BusNumber'))[2:] + ":"
                address += hex(device.get('DeviceNumber'))[2:] + ":"
                address += hex(device.get('FunctionNumber'))[2:]
        if len(address) == 0:
            self.PciAddress = "Unavailable"
        else:
            self.PciAddress = address

        

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

# write a function to populate a system given credentials
def populate_system(ip, username, password):

    # Model
    model = get_model_name(ip, username, password)

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
    if not (len(storages) == 1):
        print(f"System at ip {ip} has wrong number of storages.")
    drives = get_drive_objects(ip, username, password, storages[0])
    driveInfos = []
    for drive in drives:
        driveInfos.append(DriveInfo(drive))

    # NICs
    devices = get_pci_objects(ip, username, password)
    adapters = get_adapter_objects(ip, username, password)
    nics = []
    for adapter in adapters:
        nics.append(NetworkAdapterInfo(adapter, devices))
    
    return ComputerSystem(model, memoryInfo, processors, driveInfos, nics, get_network_interface_count(ip, username, password))
    
    
