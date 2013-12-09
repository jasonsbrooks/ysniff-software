#!/usr/bin/env python

import boto.rds
import fileinput
import sys
import re
import ConfigParser
from subprocess import call

mac_index = 12
time_index = 1
start_t_us = 0
start_u_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 30 # Seconds.
PUSH_TO_AWS_PERIOD = 120 # Seconds.
maclist = set()
buffer = {}

# Get configuration data
config = ConfigParser.RawConfigParser()
config.read('/etc/ysniff.cfg')
access_key = config.get('default','AWS_ACCESS_KEY_ID')
secret_key = config.get('default','AWS_SECRET_ACCESS_KEY')
pi_location= config.get('default','PI_LOCATION')

try:
    print "Connecting to boto"
    conn=boto.connect_sdb(access_key,secret_key)
    print "Getting SimpleDB domain"
    domain=conn.get_domain('tmp_ysniff')
except Exception as e:
    print e

print "Reading from tcpdump"
for line in fileinput.input():
    splitline = line.split(" ")
    if mac_index < len(splitline):
        mac = splitline[mac_index]
        if mac == "DA:Broadcast":
            mac = splitline[mac_index+1]
        ts = int(splitline[time_index][:-2])

        # TODO USE REGEX TO FIND MAC
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
                try:
                    print "Trying to get item:"
                    key = 'WAT' if key is None else key
                    print key
                    item = domain.get_item(key)
                    if item is None:
                        print "item was None, key is: ", key
                        item = domain.new_item(key)
                        print "new item is now: ", item
                except Exception as e:
                    print "Could not get item!"
                    print e
                for timestamp in buffer[key]:
                    print "Timestamp:", timestamp
                    item[timestamp] = pi_location

                try:
                    print "Writing data to SimpleDB"
                    item.save()
                except Exception as e:
                    print e

            buffer = {}
            start_t_us = ts

#print buffer, len(buffer)

