######################################################################################################
# This script show how to use paramiko moudle to SSH/Remote linux servers and execute command on it. #
######################################################################################################

#!/usr/bin/python

import paramiko
import re
import sys

hostname = '192.168.1.2'
username = '******'
password = '******'

#paramiko.util.log_to_file('paramiko.log')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname,22,username,password)
except Exception as err:
    print "Failed due to: " + str(err)
    print "__________________"
    sys.exit(1)
stdin,stdout,stderr = ssh.exec_command('df -h')
print "======="
print stdout.read() 
print "======="
stdin,stdout,stderr = ssh.exec_command('ps -ef | grep httpd')
print stdout.read()
if "httpd" in stdout.read():
    print "Yes"
else:
    print "No"
ssh.close()
