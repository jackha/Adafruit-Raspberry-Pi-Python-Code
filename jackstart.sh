#!/bin/bash 
## Stop the ntp service
sudo service ntp stop

## Stop the triggerhappy service
sudo service triggerhappy stop

## Stop the dbus service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo service dbus stop

## Stop the console-kit-daemon service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo killall console-kit-daemon

## Stop the polkitd service. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
sudo killall polkitd

## Only needed when Jack2 is compiled with D-Bus support (Jack2 in the AutoStatic RPi audio repo is compiled without D-Bus support)
#export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket

## Remount /dev/shm to prevent memory allocation errors
sudo mount -o remount,size=128M /dev/shm

## Kill the usespace gnome virtual filesystem daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall gvfsd

## Kill the userspace D-Bus daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall dbus-daemon

## Kill the userspace dbus-launch daemon. Warning: this can cause unpredictable behaviour when running a desktop environment on the RPi
killall dbus-launch

## Uncomment if you'd like to disable the network adapter completely
#echo -n “1-1.1:1.0” | sudo tee /sys/bus/usb/drivers/smsc95xx/unbind

## Set the CPU scaling governor to performance
echo -n performance | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

## And finally start JACK
jackd -R -P70 -p8 -t2000 -d alsa -dhw:0,0 -p 128 -n 3 -r 44100 -s &

cd ~pi/raspberry-stomp

echo Sleeping...
python sleep.py
echo pd-extended
pd-extended -jack -nogui -midiindev 1 -path /home/pi/raspberry-stomp/pd/diy2 pd/loader.pd &

echo Sleeping...
python sleep.py
# let supervisor handle this
#echo Starting RP stomp...
#sudo python rpstomp.py

#halt