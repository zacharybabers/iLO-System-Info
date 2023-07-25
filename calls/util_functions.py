import re
from .system_classes import ComputerSystem
import pandas as pd

def get_ips(ipString):
    rawStrings = ipString.split(',')
    initStrings = []
    for string in rawStrings:
        init = string.strip()
        initStrings.append(init)
    ipStrings = []

    for string in initStrings:
        myList = string.split('-')
        if len(myList) == 2:
            valid = is_valid_ip_address(myList[0]) and myList[1].isdigit()
            if valid:
                lastNum = ip_last_num(myList[0])
                for i in range (int(lastNum), int(myList[1]) + 1):
                    initStrings.append(myList[0][0:(myList[0].rfind('.') + 1)] + str(i))
    for string in initStrings:
        stripped = string.strip()
        if (is_valid_ip_address(stripped)):
            ipStrings.append(stripped)

    return list(set(ipStrings))

def is_valid_ip_address(input_string):
    ip_address_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    if re.match(ip_address_pattern, input_string):
        # Check if each octet is within the valid range (0-255)
        octets = input_string.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            return True

    return False

def ip_last_num(input_string):
    parts = input_string.rsplit('.', 1)
    if len(parts) > 1:
        return parts[-1]
    else:
        return input_string
    
def process_file(file_path):
    credentials = []
    try:
        with open(file_path, 'r') as file:
            lines = [next(file) for _ in range(3)]
        
        for line in lines:
            credentials.append(line.strip())
    except FileNotFoundError:
        print("File not found: " + file_path)
    
    return credentials

def get_sys_rows(computerSystem):
    cpuSum = computerSystem.get_cpu_sum()
    rows = []
    mainRow = []
    mainRow.append(computerSystem.model)
    mainRow.append(computerSystem.memoryInfo.status)
    mainRow.append(computerSystem.memoryInfo.totalMem)
    mainRow.append(computerSystem.memoryInfo.persistentMem)
    mainRow.append(cpuSum.get('cpuCount'))
    mainRow.append(cpuSum.get('totalCores'))
    mainRow.append(cpuSum.get('totalThreads'))
    mainRow.append(computerSystem.networkAdapterList[0].name)
    mainRow.append(computerSystem.driveList[0].name)
    rows.append(mainRow)

    maxNumRows = len(computerSystem.networkAdapterList) if len(computerSystem.networkAdapterList) > len(computerSystem.driveList) else len(computerSystem.driveList)
    if maxNumRows > 1:
        for i in range(1, maxNumRows):
            extraRow = []
            for j in range(0, 7):
                extraRow.append('-')
            if len(computerSystem.networkAdapterList) > i:
                extraRow.append(computerSystem.networkAdapterList[i].name)
            else:
                extraRow.append('-')
                print("list length: " + str(len(computerSystem.networkAdapterList)), "i: " + str(i))
            if len(computerSystem.driveList) > i:
                extraRow.append(computerSystem.driveList[i].name)
            else:
                extraRow.append('-')
                print("list length: " + str(len(computerSystem.driveList)), "i: " + str(i))
            rows.append(extraRow)

    return rows

def add_sys_rows(df, computerSystem):
    rows = get_sys_rows(computerSystem)
    for row in rows:
        df.append(row)

def build_list(computerSystems):
    lst = []
    for computerSystem in computerSystems:
        add_sys_rows(lst, computerSystem)
    
    return lst

def df_list(lst):
    return pd.DataFrame(lst, columns=['| Model', '| Mem Status', '| Total Memory', '| Persistent Memory', '| CPU Sockets', '| Total Cores', '| TotalThreads', '| Network', '| Storage'], dtype=str)