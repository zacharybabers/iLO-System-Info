import re
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

pie = "hi"
df = pd.DataFrame({'year': [2015, 2016],
                   'month': [2, 3],
                   'day': [4, 5]})

pd.to_datetime(df)