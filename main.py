import sys
import redfish

# When running remotely connect using the address, account name, 
# and password to send https requests
login_host = input("iLO IP?")
login_account = input("iLO username?")
login_password = input("iLO password?")

## Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host, \
                                     username=login_account, \
                                     password=login_password)

# Login into the server and create a session
REDFISH_OBJ.login(auth="basic")

# Do a GET on a given path
response = REDFISH_OBJ.get("/redfish/v1/systems/")

# Print out the response
sys.stdout.write("%s\n" % response.text)

# Logout of the current session
REDFISH_OBJ.logout()