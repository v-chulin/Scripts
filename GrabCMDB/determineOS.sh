########################################################################################
# Run this script under a linux server ./serverlist.txt save all the karmalab servers. #
# ./windows.txt save all the windows servers, ./linux.txt save all the linux servers.  #
########################################################################################

#!/bin/bash

# read every line from serverlist.txt, each line is a server name #
while read line
# execute the command between do ...... done #
do
# ping the server name grab the line with keyword "ttl", then split by = and get 3rd item, cut it with " ", them get the 1st item#
# value should be the the value of ttl #
value=`ping -c 1 $line | grep ttl | awk -F "=" '{print $3}' | cut -d " " -f 1`
# if ttl's value bigger than 100, write the server name into windows.txt #
if [[ $value -gt 100 ]];then
 echo $line >> windows.txt
fi
# if ttl's value lower than 100&&bigger than 0, write the server name into linux.txt #
if [[ $value -gt 0 ]]&& [[ $value -lt 100 ]];then
 echo $line >> linux.txt
fi
done < serverlist.txt
