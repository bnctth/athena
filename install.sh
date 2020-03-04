#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as 'sudo $0'"
  exit
fi

echo "Some sufficent programs will be installed, please press any key to continue."

apt update
apt upgrade
apt install python3.7 python3-pip -y
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

