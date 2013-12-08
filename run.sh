#!/bin/bash

# TODO: Click the I Agree button on YaleGuest

source /home/pi/.bashrc
ifconfig wlan0 up
iwconfig wlan0 essid YaleGuest
sleep 10
iwconfig wlan0 essid YaleGuest
sleep 10
curl --data "email=YaleGuest@yale.edu&cmd=cmd" http://10.160.252.249/auth/index.html/u
sudo airmon-ng start wlan0
sudo tcpdump -e -i mon0 | sudo /home/pi/ysniff-software/ysniff.py
