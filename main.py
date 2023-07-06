from http.client import HTTPSConnection
from base64 import b64encode


# Authorization token: we need to base 64 encode it 
# and then decode it to acsii as python 3 stores it as a byte string
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

ip = input("enter redfish ip")
username = input("enter username")
password = input("enter password")

#This sets up the https connection
c = HTTPSConnection("https://" + ip + "/redfish.Systems/1")
#then connect
headers = { 'Authorization' : basic_auth(username, password) }
c.request('GET', '/', headers=headers)
#get the response back
res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
data = res.read()  