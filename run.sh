#!/bin/bash

# TODO: Click the I Agree button on YaleGuest

source /home/pi/.bashrc
echo "Turning on wlan0"
sudo ifconfig wlan0 up
echo "Connecting to YaleGuest"
until iwconfig wlan0 | grep YaleGuest; do
    echo -n "."
	sudo iwconfig wlan0 essid YaleGuest;
	sleep 5;
done
echo "."
curl --data "email=YaleGuest@yale.edu&cmd=cmd" http://10.160.252.249/auth/index.html/u
sudo airmon-ng start wlan0
sudo tcpdump -e -i mon0 | /home/pi/ysniff-software/ysniff.py &
