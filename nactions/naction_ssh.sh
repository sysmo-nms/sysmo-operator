#!/bin/sh

. ./lib_action.sh

IP=`lib_action_get Ip`
#ID=`lib_action_get Id`
#IPVER=`lib_action_get IpVersion`
#RPERM=`lib_action_get ReadPerm`
#WPERM=`lib_action_get WritePerm`
#OTHER=`lib_action_get Other`
#USERNAME=`lib_action_get UserName`

#PROBE PROPERTY=`lib_action_get probe 1 value`

# print all values in a YAML style
# lib_action_pretty_print

xterm -e "echo \"connect to device...\"; ssh root@$IP"
