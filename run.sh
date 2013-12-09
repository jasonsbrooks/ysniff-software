#!/bin/bash

# TODO: Click the I Agree button on YaleGuest

cd /home/pi/ysniff-software
git pull # Fetch updates

source /home/pi/.bashrc
echo "Turning on wlan0"
sudo ifconfig wlan0 up
sudo airmon-ng start wlan0
sudo tcpdump -e -i mon0 | /home/pi/ysniff-software/ysniff.py &
