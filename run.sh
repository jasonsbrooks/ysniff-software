#!/bin/bash

# TODO: Click the I Agree button on YaleGuest

cd /home/pi/ysniff-software
git pull # Fetch updates

export LC_ALL=C

eth_ip = $(ifconfig | grep ether | head -1 | cut -c8-24)
time = $(date +%s)

export /home/pi/.bashrc
/home/pi/ysniff-software/tools/simpledb put dev-pi-locations $PI_LOCATION IP=$eth_ip LAST_PUSH=$time

source /home/pi/.bashrc
echo "Turning on wlan0"
sudo ifconfig wlan0 up
sudo airmon-ng start wlan0
sudo tcpdump -e -i mon0 | /home/pi/ysniff-software/ysniff.py &
