#!/bin/sh

IP="192.168.0.5"
xterm -e "echo \"$0: connect to device $IP...\"; ssh -tt root@$IP top"
