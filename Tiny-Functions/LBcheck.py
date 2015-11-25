#!/usr/bin/env python

#################################################################################
# This script use for identify if the VIPs have been loadBalanced in Netsclaer. #
# You need to provide a source VIPs list that you want to identify.             #
# Run this script as belew:                                                     #
# python ../../LBcheck.py -u *** -p *** -s ../../source_list.file.              #
#################################################################################

import urllib2
import sys
import json
from optparse import OptionParser

def getpage(api_url, username, password, timeout):
    ''' Get the page data from API, should include all the VIPs. Need login username/password. '''
    print "\n\t######################################"
    print "\n\tGathering the LBs information..."
    # authentication begin #
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, api_url, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    # authentication end #
    # Request the page via api_url #
    req = urllib2.Request(url = api_url)
    try:
        # Get the response of page info via api_url #
        response = urllib2.urlopen(req, timeout = int(timeout))
    except Exception as HTTPErr:
        print "\n\n\t##### ERROR! ########"
        print "\n\tCould not gather the LBs information, because of the following error:"
        print "\n\n\t" + str(HTTPErr) + "\n"
        print "\n\tThis is likely because one of your inputs (Username/Password) are incorrect."
        print "\n\n\t#####################"
        sys.exit(1)

    # Read out the page info #
    pageread = response.read()
    # The page format is Json, so tranfer to python format #
    pageread = json.loads(pageread)
    print "\n\tGathered the LBs information!"
    print "\n\t--------------------------------------"
    return pageread

def identify_LB(lb_groups, source_list):
    ''' Base on the source VIPs list, compare with all VIPs info, identify if it has been loadBalanced '''
    print "\n\tGoing to identify VIP info..."
    # Open a source_list file that include the VIPs your want to identify 'r+' stand for read #
    source_ip = open(source_list,'r+')
    # Open file LoadBalanced_Yes.txt, if it doesnt exist, will create a new one. 'w+' stand for write #
    LBstatus_Yes = open('LoadBalanced_Yes.txt','w+')
    # Open file LoadBalanced_No.txt, if it doesnt exist, will create a new one. 'w+' stand for write #
    LBstatus_No = open('LoadBalanced_No.txt','w+')
    # Read the source VIPs list line by line #
    for line in source_ip:
        # If the line is startswith '#' or empty, then do nothing #
        if not line.startswith("#") and not line.isspace():
            # Get the VIP from every line #
            # e.g. line - *everestadmintools.com.integration,10.184.2.62 #
            # Will get the '10.184.2.62' from it #
            vip = line.split(",")[1].strip("\n").strip()
            # Count out how many time has this vip appear in all VIPs page (lb_groups) #
            vip_num = str(lb_groups).count(vip)
            # If there's no record, then with this vip to file LoadBalanced_No.txt #
            if vip_num == 0:
                LBstatus_No.write(line.strip("\n") + "\n\tNot info was found for this VIP! It might non-exist or not in used.\n")
            # If, there's record for this vip in all VIPs page #
            else:
                # List - lb_vips used to save all the VIPs that appear in lb_groups #
                lb_vips = []
                for i in range(len(lb_groups)):
                    # lb_groups[i]['vip']['ip'] grab VIPs from lb_groups #
                    lb_vips.append(lb_groups[i]['vip']['ip'])
                # Only when we can find the this vip appear in the position lb_groups[i]['vip']['ip'] that we assume it was setup as VIP #
                if vip in lb_vips:
                    # ip_list used to save IPs under the this vip #
                    ip_list = []
                    # servers_and_ips used to save the servernames & ips under the this vips #
                    servers_and_ips = ""
                    for i in range(len(lb_groups)):
                        # If this vip appear in position - lb_groups[i]['vip']['ip'] , grab the serves & ips under it #
                        if vip == lb_groups[i]['vip']['ip']:
                            # Read out the server's name under this vip #
                            server_name = lb_groups[i]['server']['name']
                            # Read out the ip under this vip #
                            server_ip = lb_groups[i]['server']['ip']
                            # Append all the ips under this vip #
                            ip_list.append(server_ip)
                            # servers_and_ips will be written into file - LoadBalanced_No.txt #
                            servers_and_ips = servers_and_ips + "\t\tServers: %s IP: %s\n" %(server_name,server_ip)
                    # set(...) used to deduplication, if the ips under this vip more than 1, we assume it was loadBalanced #
                    if len(list(set(ip_list))) > 1:
                        # Write this vip's info into file - LoadBalanced_Yes.txt #
                        # set(servers_and_ips.strip("\n").split("\n") - deduplication, "\n".join - join them line by line #
                        LBstatus_Yes.write(line.strip("\n") + "\n\tThis VIP has been loadBalanced! List the servers under it:\n" + "\n".join(set(servers_and_ips.strip("\n").split("\n"))) + "\n")
                    # If the ips under this vip <1, we assume it was not loadBalanced #
                    else:
                        # write this vip inof into file - LoadBalanced_No.txt #
                        LBstatus_No.write(line.strip("\n") + "\n\tThis VIP has not been loadBalanced, only one server was setup for it, refer to:\n" + "\n".join(set(servers_and_ips.strip("\n").split("\n"))) + "\n")
                # If the this vip doesn't appear in the position lb_groups[i]['vip']['ip'], it should be a real IP #
                else:
                    LBstatus_No.write(line.strip("\n") + "\n\tSeems this is not a VIP, it might be a real IP, please check!\n")
    # Close the open files - LoadBalanced_No.txt & LoadBalanced_Yes.txt & source_list #
    source_ip.close()
    LBstatus_Yes.close()
    LBstatus_No.close()
    print "\n\tIdentified! \n\n\tTwo file ( LoadBalanced_Yes.txt & LoadBalanced_No.txt ) have been created under the path where this cript ran, please check!"
    print "\n\t######################################"

def main():
    # The code below uses OptionParser to gather input to the script #
    parser = OptionParser(usage="Usage: %prog [arguments] -- All the arguments listed below are required!")
    parser.add_option("-u", "--username", dest="username", help="Your sea account use to login https://getsmartlab")
    parser.add_option("-p", "--password", dest="password", help="Your password of sea account")
    parser.add_option("-s", "--sourcelist", dest="sourcelist", help="The path & file name of your source VIPs list file, e.g. C:\source_ip.txt")
    (options, args) = parser.parse_args()

    # Check if the username/password has been input #
    if (not(options.username and options.password)):
        parser.error("\nIncorrect options, please run the script with -help and input the correct options!")

    # Check if the source VIPs file has been specificed #
    if (not options.sourcelist):
        parser.error("\nIncorrect options, please input the path & file name which include your source VIPs list!")

    # API url, it provides all the VIPs info on it #
    LB_url = "https://getsmartlab/api/v1/groupmembers"
    # Call getpage function to grab all the VIPs info via API #
    pageinfo = getpage(api_url = LB_url, username = options.username, password = options.password, timeout = 3000)
    # Grab the info of source VIPs list from all the VIPs info, identify if they were loadBalanced #
    identify_LB(lb_groups = pageinfo, source_list = options.sourcelist)

if __name__=='__main__':
    main()
