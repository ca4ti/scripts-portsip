#!/usr/bin/env python3
from sys import argv
import re
#with open("/tmp/tmp.txt", "a") as f:
#   f.write(argv[1]+"\n")
from websocket import create_connection
try:
    ws = create_connection("wss://ippabx:8885/",timeout=5)
    ws.send('{"command":"auth","username":"Admin","password":"1Passwords2","domain" : "'+argv[1].split("@")[1]+'"}')
except Exception as e:
    print("Impossibile monitorare")
    exit(2)
try:
    log =ws.recv()
    ws.send('{"command":"subscribe","topics":[ "extension_events"],"extensions":["'+argv[1].split("@")[0]+'"]}')
    log =ws.recv()
    #print(ws.recv())
    pattern = '(.+online.:true.+)'
    test_string = ws.recv()
    if not re.match(".+extension_status.+", test_string) :
        test_string = ws.recv()
except Exception as e:
    print("Autenticazione errata")
    exit(3)
#with open("/tmp/tmp.txt", "a") as f:
#   f.write(test_string+"\n")
if re.match(pattern, test_string) :
    print(test_string)
    exit(0)
else:
    print("Telefono OffLine")
    exit(2)
ws.close()
#for i in $(grep -E "[0-9]+@.+ipcentrex$" -o /opt/portsip/opt/nagios/etc/objects/* -R | awk -F: '{print $2}' | sort -u) ; do echo ">>>>>>>>> $i" ; python3 portsip.py $i  ; done 2>&1 | tee /tmp/log.log | grep telefono -i  -B 1
