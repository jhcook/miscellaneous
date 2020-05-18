#!/usr/bin/env bash
#
# Restart bluetooth and reconnect devices.
#
# Requires: blueutil https://github.com/toy/blueutil
#
# Usage: `basename $0`

blueutil >/dev/null 2>&1 || { echo "blueutil not found" ; exit 127 ; }

echo "Preparing a list of connected devices..."
connected=$(blueutil --recent | awk -F'[ ,]' '$4 ~ /^connected$/{print$2}')

echo "Restarting bluetooth service..."
blueutil -p 0 && sleep 1 && blueutil -p 1

echo "Waiting for bluetooth service..."
until blueutil -p | grep "1" >/dev/null; do sleep 1; done

echo "Reconnecting to each device..."
for device in ${connected[@]}; do
    for retry in {1..5}; do	
    	echo "Trying to connect to ${device} ..."
        if blueutil --connect ${device}; then break; fi
        echo "Failed to connect to ${device}"
        sleep 1
    done
done
