This is a simple python utility that returns basic information about an HP server using redfish credentials.

Usage (make sure you have python3):  
clone this repo  
'python3 hpinfo.py' in your command line  
enter your redfish credentials and you're good to go.  

You can also use an input file to tell the program your redfish credentials and what information it should print as input instead of initially at runtime.

See input.txt as an example input file; the usage then becomes:
python3 hpinfo.py input.txt


NOTES:

IPs can be inputted as a single value or a comma delimited list. If you want to input a range of IPs (i.e XXX.XXX.XXX.11, XXX.XXX.XXX.12, XXX.XXX.XXX.13), you can input 'XXX.XXX.XXX.11-13'.
