import re

def get_ips(ipString):
    initStrings = ipString.split(',')
    ipStrings = []

    for string in initStrings:
        stripped = string.strip()
        if (is_valid_ip_address(stripped)):
            ipStrings.append(stripped)

    return ipStrings

def is_valid_ip_address(input_string):
    ip_address_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    if re.match(ip_address_pattern, input_string):
        # Check if each octet is within the valid range (0-255)
        octets = input_string.split('.')
        if all(0 <= int(octet) <= 255 for octet in octets):
            return True

    return False