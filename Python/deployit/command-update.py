# !/usr/bin/python

###################################################################################################################################
# This script use for update the start/stop command in Deployit to make J2DA work smooth when the service start                   #
# old: <startCommand>/sbin/service <servicename> start</startCommand>                                                             #
#      <stopCommand>/sbin/service <servicename> stop</stopCommand>                                                                #
# new: <startCommand> if [ -e /etc/init.d/<servicename> ]; then /sbin/service <servicename> start; else break; fi </startCommand> #
#      <stopCommand> if [ -e /etc/init.d/<servicename> ]; then /sbin/service <servicename> stop; else break; fi </stopCommand>    #
###################################################################################################################################

import urllib
import urllib2
import re
import sys
from optparse import OptionParser
from xml.etree import ElementTree as ET

def commandupdate(ConfigItem):
    pre_url = 'https://lpsdeploy/deployit/repository/ci/'
    CI_url = pre_url + ConfigItem
    #request pages for every single CI#
    req = urllib2.Request(url = CI_url, headers = headerWithAuth)
    response = urllib2.urlopen(req)
    #read the configurationitem of CIs#
    configurationitem = response.read()

    #check if start/stop command exist/need to be updated.#
    startcommandexist = configurationitem.find('<startCommand>/sbin/service')
    stopcommandexist = configurationitem.find('<stopCommand>/sbin/service')
    #only when both start/stop command don't need to be updated#
    if startcommandexist == -1 and stopcommandexist ==-1:
        print "\n\tUpdate isn't needed for CI: " + ConfigItem
        print "\n\tIt has the new start/stop command or doesn't need the start/stop command!"
    else:
        #([^>]+) means all string don't start with >, should be service name here#
        name = '''<startCommand>/sbin/service ([^>]+) start'''
        #update start command#
    	for servicename in re.findall(name,configurationitem):
			oldcommand = '''<startCommand>/sbin/service ''' + servicename + ''' start</startCommand>'''
			newcommand = '''<startCommand>if [ -e /etc/init.d/''' + servicename + ''' ]; then /sbin/service ''' + servicename + ''' start; else break; fi</startCommand>'''
			#switch the command, using new command instead old command#
			strinfo = re.compile(oldcommand)
			updateddata = strinfo.sub(newcommand,configurationitem)
			updateddata = updateddata.encode("utf8")
			print "\n\tUpdating start command for CI: " + ConfigItem
			#using urllib2.Request to PUT the new start command to Deployit#
			#req = urllib2.Request(url = CI_url, data = updated, headers = headerWithAuth)
			req = urllib2.Request(url = CI_url, data = updateddata, headers = headerWithAuth)
			req.get_method = lambda: 'PUT'
			try:
				response = urllib2.urlopen(req, timeout = int(timeout))
			except Exception as HTTPErr:
				print "\n\n\t##### ERROR! ########"
				print "\n\tCould not updated the start command, because of the following error:"
				print "\n\n\t" + str(HTTPErr) + "\n"
				print "\n\n\t#####################"
				sys.exit(1)

			print "\n\tStart command updated successfully!"

        #([^>]+) means all string don't start with >, should be service name here#
        name = '''<stopCommand>/sbin/service ([^>]+) stop'''
        #re-read page, in case start command update above change it#
        req = urllib2.Request(url = CI_url, headers = headerWithAuth)
        response = urllib2.urlopen(req)		
        configurationitem = response.read()
        #update stop command#
        for servicename in re.findall(name,configurationitem):
			oldcommand = '''<stopCommand>/sbin/service ''' + servicename + ''' stop</stopCommand>'''
			newcommand = '''<stopCommand>if [ -e /etc/init.d/''' + servicename + ''' ]; then /sbin/service ''' + servicename + ''' stop; else break; fi</stopCommand>'''
			#switch the command, using new command instead old command#
			strinfo = re.compile(oldcommand)
			updateddata = strinfo.sub(newcommand,configurationitem)
			updateddata = updateddata.encode("utf8")
			print "\n\tUpdating stop command for CI: " + ConfigItem
			#using urllib2.Request to PUT the new start command to Deployit#
			#req = urllib2.Request(url = CI_url, data = updated, headers = headerWithAuth)
			req = urllib2.Request(url = CI_url, data = updateddata, headers = headerWithAuth)
			req.get_method = lambda: 'PUT'
			try:
				response = urllib2.urlopen(req, timeout = int(timeout))
			except Exception as HTTPErr:
				print "\n\n\t##### ERROR! ########"
				print "\n\tCould not updated the stop command, because of the following error:"
				print "\n\n\t" + str(HTTPErr) + "\n"
				print "\n\n\t#####################"
				sys.exit(1)

			print "\n\tStop command updated successfully!"

    return(0)

def main():
    global username
    global password
    global CI
    global headerWithAuth
    global timeout
    timeout = 3000
	
    # The code below uses OptionParser to gather input to the script
    parser = OptionParser(usage="Usage: %prog [arguments] -- All the arguments listed below are required!")
    parser.add_option("-u", "--username", dest="username", help="Your sea account use to login Deployit")
    parser.add_option("-p", "--password", dest="password", help="Your password for sea account")
    parser.add_option("-c", "--CI", dest="CI", help="The CI which you want to update start/stop command for. Could be a specific CI e.g. Infrastructure/QA/Linux/CHELLIWEBQA705/ABTestingSvc_Tomcat_QA. Could be all environments under a folder, e.g. Environments/QA/LUX/ABTestingSvc. Could be all CIs, e.g. all")
    (options, args) = parser.parse_args()
	
    #check if the username/password has been input#
    if (not(options.username and options.password)):
	    parser.error("\nIncorrect options, please run the script with -help and input the correct options!")

	#check if CI has been input#
    if (not options.CI):
	    parser.error("\nIncorrect options, please input CI which you want to update: Specific CI/Environment folder/all! ")

    #set the value from input for variables username/password/#
    username = options.username
    password = options.password
    getCI_url = 'https://lpsdeploy/deployit/repository/query?type=tomcat.Server&resultsPerPage=-1'

    #authentication begin#
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, getCI_url, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    #authentication end#
    #request the page#
    req = urllib2.Request(url = getCI_url)
    try:
        response = urllib2.urlopen(req, timeout = int(timeout))
    except Exception as HTTPErr:
        print "\n\n\t##### ERROR! ########" 
        print "\n\tCould not gather the CIs information, because of the following error:"
        print "\n\n\t" + str(HTTPErr) + "\n"
        print "\n\tThis is likely because one of your inputs (Username/Password) are incorrect."
        print "\n\n\t#####################"
        sys.exit(1)
    
    #get the headers with authentication, used for different CIs' URLs#
    cookie= req.unredirected_hdrs.get('Authorization')
    headerWithAuth = {'Content-Type': 'application/xml', 'Authorization': cookie}

    #page show all CIs, e.g <ci ref="Infrastructure/QA/Linux/RyantestECOS/ContentMain_Ryan_ECOS" type="tomcat.Server"/>#
    page = response.read()

    print "\n\t################################### Begin ########################################"

	#Get the input CI#
    CI = options.CI
	
    #Update for all CIs#
    if CI.strip() == "all":
        #deal with all the CIs that shown on link: https://lpsdeploy/deployit/repository/query?type=tomcat.Server&resultsPerPage=-1#
        #the number of CIs depends on the permissions of the username#
        #Use ET module to deal with page, which mention on the top - from xml.etree import ElementTree as ET#
        #Read more https://docs.python.org/2/library/xml.etree.elementtree.html #
        root = ET.fromstring(page)
        for child in root:
           #child.attrib["ref"] save CIs, e.g. Infrastructure/QA/Linux/RyantestECOS/ContentMain_Ryan_ECOS#
           ConfigItems = child.attrib["ref"]
           #print ConfigItems
           #Call commandupdate with CI to perform the update#
           commandupdate(ConfigItems)
		   
    #Update for a specific CI -- only when the CI input is unique and between "...", will be take as a right CI. In case input is e.g. "a", and we can find it on page.#	   
    elif page.count("\"" + CI + "\"") == 1:
        commandupdate(CI)
		
    #Update the tomcat instances under a folder#
    elif "Environment" in CI:
        #url for search environments under folder#
        folder_url = "https://lpsdeploy/deployit/repository/query?parent=" + CI + "&type=udm.Environment&resultsPerPage=-1"
        req = urllib2.Request(url = folder_url, headers = headerWithAuth)
        response = urllib2.urlopen(req, timeout = int(timeout))
        folderpage = response.read()
        root = ET.fromstring(folderpage)
        for child in root:
		    #child.attrib['ref'] save all the CI on floderpage#
            #env_url show the content of the environments under the folder#
            env_url = "https://lpsdeploy/deployit/repository/ci/" + child.attrib['ref']
            req = urllib2.Request(url = env_url, headers = headerWithAuth)
            response = urllib2.urlopen(req, timeout = int(timeout))
            env_page = response.read()
            root = ET.fromstring(env_page)
            for child in root:
                for kid in child:
				    #kid.attrib["ref"] save all CI on env_page, CI.split("/")[-1] save tomcat name, e.g. ABTestingSvc in CI(Environments/QA/LUX/ABTestingSvc)#
                    ci_url = "https://lpsdeploy/deployit/repository/query?parent=" + kid.attrib["ref"] + "&type=tomcat.Server&namePattern=%25" + CI.split("/")[-1] + "%25&resultsPerPage=-1"
                    req = urllib2.Request(url = ci_url, headers = headerWithAuth)
                    response = urllib2.urlopen(req, timeout = int(timeout))
                    ci_page = response.read()
                    root = ET.fromstring(ci_page)
                    for child in root:
                        #child.attrib["ref"] save the tomcat.Server CIs on ci_page#
                        ConfigItems = child.attrib["ref"]
                        #print ConfigItem
                        commandupdate(ConfigItems)
					
    #Wrong CI input#
    else:
	    print "\n\tWrong CI input, please check!"
		
    print "\n\t###################################  End  ########################################"
    print "\n\tThe CIs already have the new start/stop command. No updates needed"

if __name__ == '__main__':
    main()
