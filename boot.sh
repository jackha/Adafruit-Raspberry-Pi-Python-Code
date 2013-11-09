#!/bin/bash 
cd ~pi/raspberry-stomp
./jackstart.sh
python bye.py &
halt
