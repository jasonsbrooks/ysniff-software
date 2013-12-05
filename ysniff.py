#!/usr/bin/env python

import fileinput

mac_index = 12
time_index = 1
start_t_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 30 # Seconds. 5 minutes.
PUSH_TO_AWS_PERIOD = 3600 # Seconds. One hour.
maclist = set()
buffer = {}

# TODO: Upload buffer to AWS every collection period.
for line in fileinput.input():
    splitline = line.split(" ")
    if mac_index < len(splitline):
        mac = splitline[mac_index]
        if mac == "DA:Broadcast":
            mac = splitline[mac_index+1]
        ts = int(splitline[time_index][:-2])
        mac = mac[len(mac)-MAC_LEN:]
        maclist.update(mac)

        if start_t_us is 0:
            start_t_us = ts
        elif ts - start_t_us > (SAMPLE_PERIOD * 1000000):
            buffer[start_t_us] = maclist
            maclist = set()
            start_t_us = 0
        print ts,mac

#print buffer, len(buffer)

