############################################################################################################
# This script use for grab owner from CMBD.xml files (/etc/CMDB.xml) under all karmalab/Lab Linux servers. #
# Run as ./grabCMDB.sh under a karmalab linux server, you will be requested to input username&password.    #
# Need a file save all the servers' name. (./linux.txt)                                                    #
############################################################################################################

#!/bin/bash

# get the username&password which use to login karmalab/linxu servers from input #
echo "Please input your LDAP account:"
read user
echo "Your password:"
read pass
# set time out 5 second #
set timeout 5
# read every line on servers.txt, and execute command between do ...... done for them #
while read line
do
  # every line on servers.txt is a server's name, value the server name to variable -- server #
  server=$line
  # scp to copy /etc/CMDB.xml from every single server to local path and rename it to $server.xml #
  command="scp $user@$server:/etc/CMDB.xml ./$server.xml"
  # use expect to execute the command between -c " ...... " #
  expect -c "
  # spawn the scp command #
  spawn $command;
      expect {
              # send yes when read (yes/no)? on the screen #
              \"(yes/no)?\" {send \"yes\r\"; exp_continue}
              # send password when read password: on the screen #
              \"*assword:\" {send \"$pass\r\"; exp_continue}
             }
            # jump out the interact #
            interact
            "
  # an example of CMDB.xml as below: #

  # <CmdbOwner>
  #  <Owner id="6e93c86b4017f000f1cb11369ea67b85" name="Platform Infrastructure Services: End to End Integration Environments" /> 
  #  <Application id="e4dc608b60e74588a73845e3fd845ae7" name="E2E" /> 
  #  <Modified date="10-09-2013" person="SEA\becole" /> 
  # </CmdbOwner>

  # grap the owner form CMDB.xml, and write the server name and owner into linux_list.txt #
  # grab the line with keyword "<Owner", and split by " then get 4th item #
  # should be Platform Infrastructure Services: End to End Integration Environments on above CMDB.xml #
  grep "<Owner" $server.xml | awk -F "\"" '{print "'$server'\t-- " $4}' >> linux_list.txt
  # grab the line with keyword "person" and split by " then get 4th item #
  # should be SEA\becole on above CMDB.xml #
  grep "person" $server.xml | awk -F "\"" '{print "\t\t-- " $4 }' >> linux_list.txt
  # remove file $server.xml #
  rm $server.xml
# ./linux.txt save all the kamalab Linux servers  
done < ./linux.txt
