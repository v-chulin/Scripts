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
stdin,stdout,stderr = ssh.exec_command('ps -ef | grep xebialabs/deployit')
print stdout.read()
if "nohup /opt/xebialabs/deployit" in stdout.read():
    print "Yes"
else:
    print "No"
ssh.close()
