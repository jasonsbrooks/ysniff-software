#!/bin/bash

# TODO: Click the I Agree button on YaleGuest

source /home/pi/.bashrc
sudo ifconfig wlan0 up
sudo iwconfig wlan0 essid YaleGuest
sleep 10
sudo iwconfig wlan0 essid YaleGuest
sleep 10
curl --data "email=YaleGuest@yale.edu&cmd=cmd" http://10.160.252.249/auth/index.html/u
sudo airmon-ng start wlan0
sudo tcpdump -e -i mon0 | /home/pi/ysniff-software/ysniff.py
