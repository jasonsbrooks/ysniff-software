#!/usr/bin/env python

import boto.rds
import fileinput
import sys

mac_index = 12
time_index = 1
start_t_us = 0
start_u_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 30 # Seconds.
PUSH_TO_AWS_PERIOD = 3600 # Seconds. One hour.
maclist = set()
buffer = {}

conn = boto.rds.connect_to_region("us-west-2",aws_access_key_id=sys.argv[1],aws_secret_key_id=sys.argv[2])
    aws_secret_access_key='<aws secret key>')

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

        # move maclist to buffer every SAMPLE_PERIOD
        if start_t_us is 0:
            start_t_us = ts
        elif ts - start_t_us > (SAMPLE_PERIOD * 1000000):
            buffer[start_t_us] = maclist
            maclist = set()
            start_t_us = ts

        # upload buffer every PUSH_TO_AWS_PERIOD
        if start_u_us is 0:
            start_u_us = ts
        elif ts - start_u_us > (PUSH_TO_AWS_PERIOD  * 1000000):
            # upload buffer here
            buffer = {}
            start_t_us = ts



        print ts,mac

#print buffer, len(buffer)

