#!/usr/bin/env python

import fileinput

mac_index = 12
time_index = 1
MAC_LEN = 17
SAMPLE_PERIOD = 300 # Seconds. 5 minutes.
maclist = []
buffer = {}
# TODO: add maclists to buffer every sample period.
# TODO: Upload buffer to AWS every collection period.
for line in fileinput.input():
    splitline = line.split(" ")
    if mac_index < len(splitline):
        mac = splitline[mac_index]
        if mac == "DA:Broadcast":
            mac = splitline[mac_index+1]
        ts = splitline[time_index]
        mac = mac[len(mac)-MAC_LEN:]
        if mac not in maclist:
            maclist.append(mac)
        print ts,mac
