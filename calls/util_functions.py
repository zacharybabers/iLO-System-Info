import re

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
            print("hi")
            valid = is_valid_ip_address(myList[0]) and myList[1].isdigit()
            if valid:
                lastNum = ip_last_num(myList[0])
                for i in range (int(lastNum), int(myList[1])):
                    initStrings.append(myList[0][0:(myList[0].rfind('.') + 1)] + str(i))

    print("intermittent list:", initStrings)
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
