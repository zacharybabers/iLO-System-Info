This is a simple python utility that returns basic information about an HP server using redfish credentials. Now with support for Dell Poweredge servers.

Dependency: pip3 install pandas

Usage (make sure you have python3):  
clone this repo  
'python3 hpinfo.py -i 'list of ips' -u 'username:password' -m 'detailed/table' in your command line  
enter your redfish credentials and you're good to go. 

NOTES:

IPs can be inputted as a single value or a comma delimited list. 
If you want to input a range of IPs (i.e XXX.XXX.XXX.11, XXX.XXX.XXX.12, XXX.XXX.XXX.13), you can input 'XXX.XXX.XXX.11-13'.

