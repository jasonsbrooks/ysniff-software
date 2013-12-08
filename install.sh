#!/bin/bash

sudo apt-get install libssl-dev
sudo apt-get install iw
wget http://download.aircrack-ng.org/aircrack-ng-1.2-beta1.tar.gz
tar xzvf aircrack-ng-1.2-beta1.tar.gz
cd aircrack-ng-1.2-beta1
make
sudo make install

sudo apt-get install tcpdump

git clone git://github.com/boto/boto.git
cd boto
python setup.py install

sudo cp run.sh /etc/init.d/
sudo chmod 755 /etc/init.d/run.sh
sudo update-rc.d run.sh defaults

read -p "Enter your AWS Access Key: " access_key
read -p "Enter your AWS Secret Access Key: " secret_key
read -p "Enter your Pi Location: " location

echo -e "export AWS_ACCESS_KEY_ID=$access_key\nexport AWS_SECRET_ACCESS_KEY=$secret_key\nexport PI_LOCATION=$location\n" >> /home/pi/.bashrc
