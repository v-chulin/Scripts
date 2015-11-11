#!/usr/bin/env python

import paramiko
import re
import sys
from optparse import OptionParser

class sshclient:

    def __init__(self,hostname,port,username,password):
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname,port,username,password)
        except Exception as err:
            print "Failed due to: " + str(err)
            print "__________________"
            sys.exit(1)

    def Rtest(self):
        print "\n============================\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo ls /opt/app', get_pty = True)
        stdin.write(self.password + '\n')
        stdin.flush()
        print stderr.read()#,stdout.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo wget -qP /opt/app/thirdparty http://chellssapp60/repository/jdk-8u45-linux-x64.tar.gz && ls -l /opt/app/thirdparty')
        print stdout.read(),stderr.read()
        #stdin,stdout,stderr = self.ssh.exec_command('[ -d /opt/app/lntest ] || [ -f /opt/app/lntest ] && echo "path exists" || sudo ln -s /opt/app/test/ /opt/app/lntest')
        #print stdout.read(),stderr.read()
        print "\n============================"

    def adduser_tomcat(self):
        print "\n==== Add user: tomcat =====\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo ls /opt', get_pty = True)
        stdin.write(self.password + '\n')
        stdin.flush()
        stdin,stdout,stderr = self.ssh.exec_command('sudo groupadd tomcat && sudo useradd -g tomcat -s /bin/sh -m -d /home/tomcat tomcat && cat /etc/passwd | grep tomcat ')
        print stdout.read(),stderr.read()
        print "\n============================"

    def JDKinstall(self):
        print "\n====== Jdk install =========\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo ls /opt', get_pty = True)
        stdin.write(self.password + '\n')
        stdin.flush()
        print stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo mkdir -p /opt/jlux /opt/app/thirdparty && sudo chown -R tomcat:tomcat /opt/jlux /opt/app')
        print stdout.read(),stderr.read()
        print "Downloading jdk-7u25 from repository...\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo wget -qP /opt/app/thirdparty http://chellssapp60/repository/jdk-7u25-linux-x64.rpm')
        print stdout.read(),stderr.read()
        print "Installing jdk-7u25...\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo rpm -ivh /opt/app/thirdparty/jdk-7u25-linux-x64.rpm')
        print stdout.read(),stderr.read()
        print "Creat symbolic link for JDK. \n"
        stdin,stdout,stderr = self.ssh.exec_command('[ -d /opt/app/thirdparty/jdk7 ] || [ -f /opt/app/tomcat] && echo "Folder or file /opt/app/thirdparty/jdk7 exist! Can not create symbolic link for JDK, please check" || sudo ln -sv /usr/java/jdk1.7.0_25/ /opt/app/thirdparty/jdk7')
        print stdout.read(),stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo chown -R tomcat:tomcat /opt/jlux /opt/app')
        print stdout.read(),stderr.read()
        print "\n============================"

    def Tomcatinstall(self):
        print "\n===== Tomcat install =====\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo ls /opt', get_pty = True)
        stdin.write(self.password + '\n')
        stdin.flush()
        print stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo mkdir -p /opt/jlux /opt/app /var/run/tomcat /var/log/tomcat && sudo chown -R tomcat:tomcat /opt/jlux /opt/app')
        print stdout.read(),stderr.read()
        print "Downloading tomcat-deployit-7 from repository...\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo wget -qP /opt/app http://chellssapp60/repository/tomcat-deployit-support-0.3-2.noarch.rpm')
        print stdout.read(),stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo wget -qP /opt/app http://chellssapp60/repository/tomcat-deployit-7.0.42-0.noarch.rpm')
        print stdout.read(),stderr.read()
        print "Installing tomcat-deployit-7...\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo rpm -ivh /opt/app/tomcat-deployit-support-0.3-2.noarch.rpm')
        print stdout.read(),stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo rpm -ivh /opt/app/tomcat-deployit-7.0.42-0.noarch.rpm')
        print stdout.read(),stderr.read()
        print "Creat symbolic link for tomcat.\n"
        stdin,stdout,stderr = self.ssh.exec_command('[ -d /opt/app/tomcat ] || [ -f /opt/app/tomcat ] && echo "Folder or file /opt/app/tomcat exist! Can not create symbolic link for JDK, please check" || sudo ln -sv /opt/apache/tomcat-7.0.42/ /opt/app/tomcat')
        print stdout.read(),stderr.read()
        print "\n============================"

    def ENVexport(self):
        print "\n======= Env export ========\n"
        stdin,stdout,stderr = self.ssh.exec_command('sudo ls /opt', get_pty = True)
        stdin.write(self.password + '\n')
        stdin.flush()
        stdin,stdout,stderr = self.ssh.exec_command('sudo sh -c \'[ -f /etc/profile.d/java.sh ] || touch /etc/profile.d/java.sh\' ')
        print stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('sudo sh -c \'echo -e "#JAVA_HOME set for Oracle JDK \n#this file is written to /etc/profile.d/ \nJAVA_HOME=/opt/app/thirdparty/jdk7 \nCATALINA_HOME=/opt/app/tomcat \nPATH=$PATH:$JAVA_HOME/bin \nexport JAVA_HOME PATH CATALINA_HOME" >> /etc/profile.d/java.sh\' ')
        print stderr.read()
        stdin,stdout,stderr = self.ssh.exec_command('source /etc/profile.d/java.sh && echo -e "JAVA_HOME = $JAVA_HOME \nCATALINA_HOME =$CATALINA_HOME"')
        print stdout.read(),stderr.read()
        print "\n============================"

    def close(self):
        self.ssh.close()

if __name__=='__main__':

    # The code below uses OptionParser to gather input to the script
    parser = OptionParser(usage="Usage: %prog [arguments] -- All the arguments listed below are required!")
    parser.add_option("-u", "--username", dest="username", help="Your sea account use to login Deployit")
    parser.add_option("-p", "--password", dest="password", help="Your password of sea account")
    parser.add_option("-s", "--servers", dest="servers", help="The hostname of servers")
    (options, args) = parser.parse_args()

    #check if the username/password has been input#
    if (not(options.username and options.password)):
        parser.error("\nIncorrect options, please run the script with -help and input the correct options!")

    if (not options.servers):
        parser.error("\nIncorrect options, please input hostname which you want to install JDK/Tomcat! e.g. chelliwebqa704")

    conn = sshclient(options.servers,22,options.username,options.password)
    conn.adduser_tomcat()
    conn.JDKinstall()
    conn.Tomcatinstall()
    conn.ENVexport()
    #conn.Rtest()
    conn.close()
