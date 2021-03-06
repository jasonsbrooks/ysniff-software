#!/usr/bin/env python

import boto.dynamodb
import fileinput
import sys
import re
import datetime
import calendar
import time
import ConfigParser
import subprocess

mac_index = 12
time_index = 0
start_t_us = 0
start_u_us = 0
MAC_LEN = 17
SAMPLE_PERIOD = 2*60 # Seconds.
PUSH_TO_AWS_PERIOD = 2.5*60 # Seconds.
maclist = set()
buffer = {}

logfile = open('log', 'a')

# Get configuration data
config = ConfigParser.RawConfigParser()
config.read('/etc/ysniff.cfg')
access_key = config.get('default','AWS_ACCESS_KEY_ID')
secret_key = config.get('default','AWS_SECRET_ACCESS_KEY')
pi_location= config.get('default','PI_LOCATION')
table_name = 'prod-ysniff' # TODO: Use cfg file to get table name

try:
    print >>logfile, "Connecting to boto"
    conn=boto.dynamodb.connect_to_region('us-east-1',aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    print >>logfile, "Getting Mac DynamoDB table"
    table=conn.get_table(table_name)
    print >>logfile, "Getting IP DynamoDB table"
    ip_table=conn.get_table('prod-ysniff-ips')
except Exception as e:
    print(e, logfile)

print("Phoning home", logfile)
ip_addr = subprocess.Popen(['/home/pi/ysniff-software/tools/getip.sh'],stdout=subprocess.PIPE).communicate()[0][:-1]
cur_time = calendar.timegm(time.gmtime())

#get rid of get_item and replace with update_item from layer 1
# logfile stuff needs to be better (redirectr stdout and stderr to file)
# add run.sh to etc and init.d so there is a link to the link so on git pull it has the latest stuff
# deploy two other pies
# film a good movie
try:
    item = ip_table.get_item(pi_location)
except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
    item = ip_table.new_item(pi_location)
    print("new item is now: ", item, logfile)
except Exception as e:
    print("Could not get item!", logfile)
    print(e, logfile)
item.put_attribute('IP Address', ip_addr)
item.put_attribute('Last Push', cur_time)
try:
    print("Writing data to SimpleDB", logfile)
    conn.update_item(item)
except Exception as e:
    print(e, logfile)

print("Reading from tcpdump", logfile)
for line in fileinput.input():
    isbroadcast = re.search("Broadcast", line);
    m = re.search("(?:SA|DA)[:-]((?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2})", line)
    if m is not None and isbroadcast is not None:
      mac = m.group(1)
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

        # Update start_t_us every SAMPLE_PERIOD
        if start_t_us is 0 or ts - start_t_us > (SAMPLE_PERIOD):
            start_t_us = ts
        # Only pair timestamp to mac address once
        if start_t_us not in buffer[mac]:
            buffer[mac].append(start_t_us)


        # upload buffer to AWS every PUSH_TO_AWS_PERIOD
        if start_u_us is 0:
            start_u_us = ts
        elif ts - start_u_us > (PUSH_TO_AWS_PERIOD):
            print("This is the buffer: ", buffer, logfile)
            for key in buffer:
                try:
                    print("Trying to get item:", logfile)
                    if key is None or key is '':
                        continue
                    print(key, logfile)
                    item = table.get_item(key) # Encrypt MAC with md5
                except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
                    print("item was None, key is: ", key, logfile)
                    item = table.new_item(key) # Encrypt MAC with md5
                    print("new item is now: ", item, logfile)
                except Exception as e:
                    print("Could not get item!", logfile)
                    print(e, logfile)
                for timestamp in buffer[key]:
                    print("Timestamp:", timestamp, logfile)
                    item.put_attribute(timestamp,pi_location)
                try:
                    print("Writing data to SimpleDB", logfile)
                    conn.update_item(item)
                except Exception as e:
                    print(e, logfile)

            cur_time = calendar.timegm(time.gmtime())
            item = ip_table.get_item(pi_location)
            item.put_attribute('Last Push', cur_time)
            conn.update_item(item)
            buffer = {}
            start_t_us = ts

#print(buffer, len(buffer), logfile)

