#!/bin/sh

sudo cp etc/modprobe.d/alsa-base.conf /etc/modprobe.d/
sudo apt-get install $(cat packages  | tr "\n" " ")
sudo pip install pyalsa

git config --global user.email "pi@raspberry.local"
git config --global user.name "Raspberry Pi"
