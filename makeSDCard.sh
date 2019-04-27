#!/bin/bash

echo "Prepare image for CityMattersSensor"

apt-get update  -y 
apt-get upgrade -y 


echo "Setup NTP Service and set timezone to Berlin"

echo "NTP=0.de.pool.ntp.org 1.de.pool.ntp.org 2.de.pool.ntp.org 3.de.pool.ntp.org" >> /etc/systemd/timesyncd.conf
echo "FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org" >> /etc/systemd/timesyncd.conf

timedatectl set-ntp true
timedatectl set-timezone 'Europe/Berlin'

hwclock -w


echo "Install Python3 deps"
sudo apt-get install build-essential python3-dev python3-pip -y


echo "Install Adafruit PYthon BBB lib"
git clone git://github.com/adafruit/adafruit-beaglebone-io-python.git
cd adafruit-beaglebone-io-python
python3 setup.py install
cd 
rm -rf adafruit-*


echo "Install PySerial 3.4"
wget https://files.pythonhosted.org/packages/cc/74/11b04703ec416717b247d789103277269d567db575d2fd88f25d9767fe3d/pyserial-3.4.tar.gz 
tar -xzvf pyserial-3.4.tar.gz
cd pyserial-3.4 
python3 setup.py install 
cd 
rm -rf pyserial-3.4* 



echo "Remove unused packages"
apt-get remove apache2*
apt-get remove ardupilot*
apt-get remove roboticscape -y 
apt-get remove pru-software-support-package -y 
apt-get remove bonescript -y 
apt-get remove doc-beaglebone-getting-started -y
apt-get remove bb-node-red-installer -y
apt-get remove doc-beaglebonegreen-getting-started -y
apt-get remove c9-core-installer -y
apt-get remove doc-seeed-bbgw-getting-started -y
apt-get remove nodejs -y
apt-get remove firmware-am57xx-opencl-monitor -y
apt-get remove bone101 -y

if [ -d /var/lib/cloud9 ] 
then 
   rm -rf /var/lib/cloud9
fi 

if [ -d /usr/share/ti ] 
then 
   rm -rf /usr/share/ti
fi 
