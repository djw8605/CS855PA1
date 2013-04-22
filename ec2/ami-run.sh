#!/bin/sh

rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
yum -y install yum-priorities git

# Checkout the project
git clone git://github.com/djw8605/CS855PA1.git

# Start the server
cd CS855PA1
git checkout PA3
python src/ATMServer.py


