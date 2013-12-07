#!/usr/bin/env python

import boto.rds
import fileinput
import sys
import os

mac_index = 12
time_index = 1
start_t_us = 0
start_u_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 30 # Seconds.
PUSH_TO_AWS_PERIOD = 3600 # Seconds. One hour.
maclist = set()
buffer = {}

conn=boto.connect_sdb()
domain=conn.get_domain('tmp_ysniff')

# TODO: Upload buffer to AWS every collection period.
for line in fileinput.input():
    splitline = line.split(" ")
    if mac_index < len(splitline):
        mac = splitline[mac_index]
        if mac == "DA:Broadcast":
            mac = splitline[mac_index+1]
        ts = int(splitline[time_index][:-2])
        mac = mac[len(mac)-MAC_LEN:]

        # Make list of timestamps for each mac
        if mac not in buffer:
            buffer[mac]=[]

        # Only pair timestamp to mac address once
        if start_t_us not in buffer[mac]:
            buffer[mac].append(start_t_us)

        # Update start_t_us every SAMPLE_PERIOD
        if start_t_us is 0 or ts - start_t_us > (SAMPLE_PERIOD * 1000000):
            start_t_us = ts

        # upload buffer to AWS every PUSH_TO_AWS_PERIOD
        if start_u_us is 0:
            start_u_us = ts
        elif ts - start_u_us > (PUSH_TO_AWS_PERIOD  * 1000000):
            for key in buffer:
                item = domain.get_item(key)
                for timestamp in buffer[key]:
                    item[timestamp] = os.environ['PI_LOCATION']
                item.save()

            buffer = {}
            start_t_us = ts

#print buffer, len(buffer)

