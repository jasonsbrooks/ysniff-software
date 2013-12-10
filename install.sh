#!/bin/bash

sudo apt-get install libssl-dev
sudo apt-get install iw
sudo apt-get install perl
wget http://download.aircrack-ng.org/aircrack-ng-1.2-beta1.tar.gz
tar xzvf aircrack-ng-1.2-beta1.tar.gz
cd aircrack-ng-1.2-beta1
make
sudo make install

sudo apt-get install tcpdump

git clone https://github.com/boto/boto.git
cd boto
python setup.py install

# Install SimpleDB deps
curl -Lo amazon-simpledb-perl-library.zip \
  http://amazon-simpledb-perl-library.notlong.com

unzip amazon-simpledb-perl-library.zip

sudo cp -r AmazonSimpleDB-2009-04-15-perl-library/ /usr/share/perl/5.14.2/

sudo cp run.sh /etc/init.d/
sudo chmod 755 /etc/init.d/run.sh
sudo update-rc.d run.sh defaults

read -p "Enter your AWS Access Key: " access_key
read -p "Enter your AWS Secret Access Key: " secret_key
read -p "Enter your Pi Location: " location

echo -e "[default]\nAWS_ACCESS_KEY_ID=$access_key\nAWS_SECRET_ACCESS_KEY=$secret_key\nPI_LOCATION=$location\n" >> ysniff.cfg
echo -e "export AWS_ACCESS_KEY_ID=$access_key\nexport AWS_SECRET_ACCESS_KEY=$secret_key\nexport PI_LOCATION=$location\n" >> /home/pi/.bashrc
sudo mv ysniff.cfg /etc/
