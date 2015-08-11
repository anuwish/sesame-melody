#!/bin/sh

sudo apt-get install libsndfile1 libsndfile1-dev sndfile-tools sndfile-programs libsamplerate0 libsamplerate0-dev samplerate-programs libjack-jackd2-0 libjack-jackd2-dev jackd2 libavcodec-extra libavcodec-extra-54 libavcodec-dev libavformat54 libavformat-extra-54 libavformat-dev libavutil52 libavutil-dev libavutil-extra-52 libavresample1 libavresample-dev
wget http://aubio.org/pub/aubio-0.4.2.tar.bz2
tar xvfj aubio-0.4.2.tar.bz2 
cd aubio-0.4.2/
sudo chown -R pi:pi build/
./waf configure build
sudo ./waf install
cd python/
python setup.py build
sudo python setup.py install
cd ../..