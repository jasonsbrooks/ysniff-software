#!/usr/bin/env python

import boto.dynamodb
import md5
import fileinput
import sys
import re
import datetime
import time
import ConfigParser
from subprocess import call

mac_index = 12
time_index = 0
start_t_us = 0
start_u_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 60 # Seconds.
PUSH_TO_AWS_PERIOD = 5*60 # Seconds.
maclist = set()
buffer = {}

md = md5.new()

# Get configuration data
config = ConfigParser.RawConfigParser()
config.read('/etc/ysniff.cfg')
access_key = config.get('default','AWS_ACCESS_KEY_ID')
secret_key = config.get('default','AWS_SECRET_ACCESS_KEY')
pi_location= config.get('default','PI_LOCATION')

try:
    print "Connecting to boto"
    conn=boto.dynamodb.connect_to_region('us-east-1',aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    print "Getting DynamoDB table"
    table=conn.get_table('dev-ysniff')
except Exception as e:
    print e
print "Reading from tcpdump"
for line in fileinput.input():
    m = re.search("((?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2})", line)
    if m is not None:
      mac = m.group(0)
      splitline = line.split(" ")
      if mac_index < len(splitline):
        ts_raw = time.strftime("%Y:%m:%d:")+str(splitline[time_index][:-7])
        ts_list = ts_raw.split(':')
        ts_list = map(int, ts_list)
        ts_dt = datetime.datetime(*ts_list)
        ts = time.mktime(ts_dt.timetuple())

        # Make list of timestamps for each mac
        if mac not in buffer:
            buffer[mac]=[]

        # Only pair timestamp to mac address once
        if start_t_us not in buffer[mac]:
            buffer[mac].append(start_t_us)

        # Update start_t_us every SAMPLE_PERIOD
        if start_t_us is 0 or ts - start_t_us > (SAMPLE_PERIOD):
            start_t_us = ts

        # upload buffer to AWS every PUSH_TO_AWS_PERIOD
        if start_u_us is 0:
            start_u_us = ts
        elif ts - start_u_us > (PUSH_TO_AWS_PERIOD):
            print "This is the buffer: ", buffer
            for key in buffer:
                try:
                    print "Trying to get item:"
                    if key is None or key is '':
                        continue
                    print key
                    item = table.get_item(key) # Encrypt MAC with md5
                except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
                    print "item was None, key is: ", key
                    item = table.new_item(key) # Encrypt MAC with md5
                    print "new item is now: ", item
                except Exception as e:
                    print "Could not get item!"
                    print e
                for timestamp in buffer[key]:
                    print "Timestamp:", timestamp
                    item[timestamp] = pi_location

                try:
                    print "Writing data to SimpleDB"
                    item.put()
                except Exception as e:
                    print e

            buffer = {}
            start_t_us = ts

#print buffer, len(buffer)

