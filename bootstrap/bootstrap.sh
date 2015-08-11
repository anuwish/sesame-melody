#!/bin/sh

sudo apt-get update
sudo apt-get upgrade
sudo cp etc/modprobe.d/alsa-base.conf /etc/modprobe.d/
sudo apt-get install $(cat packages  | tr "\n" " ")
sudo apt-get install python-distutils-extra
sudo apt-get install python-pyrex
#sudo pip install python-pyrex
sudo pip install pyalsa
sudo pip install pyalsaaudio

git config --global user.email "pi@raspberry.local"
git config --global user.name "Raspberry Pi"
