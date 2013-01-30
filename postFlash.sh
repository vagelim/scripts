#!/bin/bash
wget http://prdownloads.sourceforge.net/webadmin/webmin-1.530.tar.gz
tar zxvf webmin-1.530.tar.gz
cd webmin-1.530
./setup.sh
mkdir /var/cache/apt/archives/
mkdir /var/cache/apt/archives/partial
touch /var/cache/apt/archives/lock
apt-get update
apt-get upgrade
