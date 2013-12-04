#!/bin/bash

sudo apt-get install iw
wget http://download.aircrack-ng.org/aircrack-ng-1.2-beta1.tar.gz
tar xzvf aircrack-ng-1.2-beta1.tar.gz
cd aircrack-ng-1.2-beta1
make
sudo make install

sudo cp run.sh /etc/init.d/
sudo chmod 755 /etc/init.d/run.sh
sudo update-rc.d run.sh defaults


