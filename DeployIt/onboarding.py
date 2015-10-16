# !/usr/bin/python

###########################################################
# This script use for create new environment on Deployit. #
###########################################################

import urllib
import urllib2
import sys
from optparse import OptionParser
from xml.etree import ElementTree as ET

def main():
    global username
    global password
    global alltomcat
    global allserver
    global alldicts
    global tomcatname
    global timeout
    timeout = 3000
    # The code below uses OptionParser to gather input to the script
    parser = OptionParser(usage="Usage: %prog [arguments] -- All the arguments listed below are required!")
    parser.add_option("-u", "--username", dest="username", help="Your sea account use to login Deployit")
    parser.add_option("-p", "--password", dest="password", help="Your password of sea account")
    parser.add_option("-e", "--environment", dest="environment", help="The environment you want to create. e.g. Environments/INT/LUX/ABTestingSvc/ABTestingSvc_INT_ENV")
    (options, args) = parser.parse_args()

    #check if the username/password has been input#
    if (not(options.username and options.password)):
        parser.error("\nIncorrect options, please run the script with -help and input the correct options!")

    #check if environment has been input#
    if (not options.environment):
        parser.error("\nIncorrect options, please input environment which you want to create! e.g. Environments/INT/LUX/ABTestingSvc/ABTestingSvc_INT_ENV")

    #set the value from input for variables username/password/#
    username = options.username
    password = options.password
    env_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/exists/" + options.environment
    newenv_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/ci/" + options.environment

    #authentication begin#
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, env_url, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    #authentication end#
    #request the page#
    req = urllib2.Request(url = env_url)
    try:
        response = urllib2.urlopen(req, timeout = int(timeout))
    except Exception as HTTPErr:
        print "\n\n\t##### ERROR! ########" 
        print "\n\tCould not identify if the environment exists, because of the following error:"
        print "\n\n\t" + str(HTTPErr) + "\n"
        print "\n\tThis is likely because one of your inputs (Username/Password) are incorrect."
        sys.exit(1)
    
    #get the headers with authentication, used for different CIs' URLs#
    cookie= req.unredirected_hdrs.get('Authorization')
    headerWithAuth = {'Content-Type': 'application/xml', 'Authorization': cookie}

    #page show true/false for environment exists/non-exists#
    page = response.read()

    print "\n\t############################### Create new Environment ###############################"
    #check if the environment exists#
    if page.find("true") != -1:
        print "\n\tThe environment you want to create is exists! Please check!"
    else:
        #get the arguments from input#
        servernames = raw_input("\n\tPlease input the Server name you want to add for this Environment. e.g. CHELLIWEBQA705 (split by \";\" if more than one):\n\t")
        dictionarytype = raw_input("\n\tPlease input environment type of dictionary, e.g. INT\QA7:\n\t")
        #split the arguments and count the number of server/dictionary#
        servername = servernames.strip().split(";")
        servername_num = servernames.count(";") +1
        servernames = servernames.strip()
        dictionarytype = dictionarytype.strip()

        #allserver is used to save linux/windows host containers, tomcatname is used to save tomcat container#
        allserver = ""
        tomcatname = ""
        #check if servernames input is null#
        if servernames == "":
            allserver = ""
        else:
            #linuxhost_url/windowshost_url used to query the SshHost/CifsHost via API#
            linuxhost_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=overthere.SshHost&resultsPerPage=-1"
            windowshost_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=overthere.CifsHost&resultsPerPage=-1"

            #request the linux host page#
            req = urllib2.Request(url = linuxhost_url, headers = headerWithAuth)
            response = urllib2.urlopen(req, timeout = int(timeout))
            #linuxhostpage shows like below:
            #<list>
            # <ci ref="Infrastructure/QA/Linux/CHELLIWEBQA705" type="overthere.SshHost"/>
            # ......
            #</list>
            linuxhostpage = response.read()
            #Use ET module to deal with page, which mention on the top - from xml.etree import ElementTree as ET#
            root = ET.fromstring(linuxhostpage)
            linuxhost_list = []

            #save all the linux host into linuxhost_list#
            for child in root:
                #child.attrib['ref'] save CI from linuxhostpage, e.g. Infrastructure/QA/Linux/CHELLIWEBQA705 from <ci ref="Infrastructure/QA/Linux/CHELLIWEBQA705" type="overthere.SshHost"/>#
                linuxhost_list.append(child.attrib['ref'])

            #request the windows host page, the process refer to linux below#
            req = urllib2.Request(url = windowshost_url, headers = headerWithAuth)
            response = urllib2.urlopen(req, timeout = int(timeout))
            windowshostpage = response.read()
            root = ET.fromstring(windowshostpage)
            windowshost_list = []

            #save all the linux host into windowshost_list#
            for child in root:
                windowshost_list.append(child.attrib['ref'])

            #grep linux host containers from linuxhost_list, alllinux is used to save linux host containers#
            alllinux = ""
            for i in range(0,servername_num):
                for serverhost in linuxhost_list:
                    #if the input servername in the linux list, add them into alllinux#
                    if servername[i].upper() in serverhost.upper():
                        alllinux = alllinux + ("<ci ref=\"" + serverhost + "\"/>")

            #grep windows host containers from windowshost_list, allwindows is used to save windows host containers#
            allwindows = ""
            for i in range(0,servername_num):
                for serverhost in windowshost_list:
                    #if the input servername in the windows list, add them into allwindows#
                    if servername[i].upper() in serverhost.upper():
                        allwindows = allwindows + ("<ci ref=\"" + serverhost + "\"/>")

            #allserver include alllinux and allwindows#
            allserver = alllinux + allwindows

            ####### add tomcat containers #######
            #alltocmat is used to save tomcat.VirtualHost containers#
            alltomcat = ""
            #when alllinux isn't null, add tomcat.VirtualHost into alltomcat#
            if len(alllinux.strip()) != 0:
                #get the tomcat arguments from input#
                tomcatname = raw_input("\n\tPlease input the tomcat containers, e.g. ABTestingSvc_VH_QA/ABTesting:\n\t")
                tomcatname = tomcatname.strip()
                #check if tomcatname input is null#
                if tomcatname == "":
                    alltomcat = ""
                else:
                    #tomcat_url is query the tomcat.VirtualHost via API with key word tomcatname which from input argument#
                    tomcat_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=tomcat.VirtualHost&namePattern=%25" + tomcatname + "%25&resultsPerPage=-1"
                    req = urllib2.Request(url = tomcat_url, headers = headerWithAuth)
                    response = urllib2.urlopen(req, timeout = int(timeout))
                    #an example of the tomcatpage show - https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=tomcat.VirtualHost&namePattern=%25ABtesting%25&resultsPerPage=-1#
                    #<list>
                    #<ci ref="Infrastructure/INT/Linux/CHEILIWEB002/ABTestingSvc_Tomcat_INT/ABTestingSvc_VH_INT" type="tomcat.VirtualHost"/>
                    #<ci ref="Infrastructure/INT/Linux/CHEILIWEB001/ABTestingSvc_Tomcat_INT/ABTestingSvc_VH_INT" type="tomcat.VirtualHost"/>
                    #......
                    #</list>
                    tomcatpage = response.read()
                    #Use ET module to deal with page#
                    root = ET.fromstring(tomcatpage)
                    tomcat_list = []

                    for child in root:
                        #child.attrib['ref'] saves tomcat from tomcatpage#
                        tomcat_list.append(child.attrib['ref'])

                    #grep tomcat container for new environment from tomcat_list#
                    for i in range (0,servername_num):
                        for container in tomcat_list:
                            if servername[i].upper() in container.upper():
                                alltomcat = alltomcat + ("<ci ref=\"" + container + "\"/>")
            ####### add tomcat containers end #######

            ####### add IIS containers #######
            #alliis is used to save IIS.Server containers#
            alliis = ""
            #when allwindows isn't null, add IIS.Server into alliis#
            if len(allwindows.strip()) != 0:
                #iis_url is query all the iis.Server via API#
                iis_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=iis.Server&resultsPerPage=-1"
                req = urllib2.Request(url = iis_url, headers = headerWithAuth)
                response = urllib2.urlopen(req, timeout = int(timeout))
                #iispage show like: #
                #<list>
                #<ci ref="Infrastructure/STABLE/Windows/CHELPCAE2E201/IIS" type="iis.Server"/>
                #<ci ref="Infrastructure/INT/Windows/CHELLIPCSINT01/IIS" type="iis.Server"/>
                #......
                #</list>
                iispage = response.read()
                #Use ET module to deal with page#
                root = ET.fromstring(iispage)
                iis_list = []

                for child in root:
                    #child.attrib['ref'] saves iis from iispage#
                    iis_list.append(child.attrib['ref'])

                #grep iis container for new environment from iis_list#
                for i in range (0,servername_num):
                    container_list = []
                    for container in iis_list:
                        if servername[i].upper() in container.upper():
                            #if there's only one IIS container for servername[i] in iis_list, value containers#
                            containers = container
                            #if there's more than one IIS container for servername[i] in iis_list, append them into container_list#
                            container_list.append(container)
                    #if more than one iis container for servername[i], choose one from input argument#
                    if len(container_list) > 1:
                        print "\n\tThere are more than one IIS under this server, please choose one: "
                        for ii in range(0,len(container_list)):
                            print "\n\t\t" + str(ii+1) + ". " + container_list[ii]
                        choose = raw_input("\n\tInput the number of this options, e.g 1:\t")
                        alliis = alliis + ("<ci ref=\"" + container_list[int(choose.strip())-1] + "\"/>")
                    #only one iis container, use it by default#
                    else:
                        alliis = alliis + ("<ci ref=\"" + containers + "\"/>")
            ####### add IIS containers end #######

        #identify if the new environment is INT and OS is linux, if so, add AutoJira_CI for it#
        if dictionarytype.upper().find("INT") != -1 and len(alllinux.strip()) != 0:
            requiresChangeTicket = "true"
            container_jira = "<ci ref=\"Infrastructure/PROD/Linux/JiraCliHost/AutoJira_CI\"/>"
        else:
            requiresChangeTicket = "false"
            container_jira = ""

        Conts = "<members>" + allserver + alltomcat + alliis + container_jira + "</members>"

        #check if dictionary input is null#
        alldicts = ""
        if dictionarytype == "":
            alldicts = ""
        else:
            #dictionary_url is query the dictionaries via API#
            if tomcatname != "":
                dictionary_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=udm.Dictionary&namePattern=%25" + tomcatname + "%25&resultsPerPage=-1"
            else:
                #get the service arguments from input#
                servicename = raw_input("\n\tPlease input the service name, e.g. AnalyticsService:\n\t")
                servicename = servicename.strip()
                dictionary_url = "https://lpsdeploy.idxlab.expedmz.com/deployit/repository/query?type=udm.Dictionary&namePattern=%25" + servicename + "%25&resultsPerPage=-1"

            #only when one of tomcatname/servicename isn't null, that we can search out the specific dictionary#
            if tomcatname != "" or servicename != "":
                req = urllib2.Request(url = dictionary_url, headers = headerWithAuth)
                response = urllib2.urlopen(req, timeout = int(timeout))
                dictionarypage = response.read()
                #Use ET module to deal with dictionarypage#
                root = ET.fromstring(dictionarypage)
                dict_list = []

                for child in root:
                    #child.attrib['ref'] saves the dictionary from dictionarypage#
                    dict_list.append(child.attrib['ref'])

                for dictionary in dict_list:
                    if dictionarytype.upper() in dictionary.upper():
                        alldicts = alldicts + ("<ci ref=\"" + dictionary + "\"/>")
            else:
                alldicts = ""

        Dicts = "<dictionaries>" + alldicts + "</dictionaries>"

        #configurationitem is the data that we need to POST to Deployit to create new environment#
        #Refer to https://docs.xebialabs.com/generated/xl-deploy/3.9.x/rest-api/com.xebialabs.deployit.engine.api.RepositoryService.html#/repository/ci/{ID:.*?}:POST #
        configurationitem = ("<udm.Environment id=\"" +options.environment + "\">" 
                                 + Conts + Dicts +
                               "<requiresChangeTicket>" + requiresChangeTicket + "</requiresChangeTicket>"
                               "<requiresGoNoGoForProduction>false</requiresGoNoGoForProduction>"
                               "<requiresSmokeTested>false</requiresSmokeTested>"
                               "<requiresCRApproved>false</requiresCRApproved>"
                               "<requiresUnitTested>false</requiresUnitTested>"
                               "<requiresPerformanceTested>false</requiresPerformanceTested>"
                               "<managerialRecepients>lpsops@expedia.com</managerialRecepients>"
                               "<devOpsRecepients>deployit@expedia.com</devOpsRecepients>"
                               "<FeaturePM/>"
                               "<TesterforValidation/>"
                               "<ApplicationEngineer/>"
                               "<manualSteps/>"
                               "<triggers/>"
                             "</udm.Environment>")
        configurationitem = configurationitem.encode("utf8")

        print "\n\t---------------------------------------------------------"
        print "\n\tCreating Environment: " + options.environment
#        print configurationitem
        #POST the request#
        request = urllib2.Request(url = newenv_url, data = configurationitem, headers = headerWithAuth)
#        request.get_method = lambda: 'POST'
        try:
            response = urllib2.urlopen(request, timeout = int(timeout))
        except Exception as HTTPErr:
            print "\n\n\t##### ERROR! ########"
            print "\n\tCould not create the environment, because of the following error:"
            print "\n\n\t" + str(HTTPErr) + "\n"
            sys.exit(1)

        print "\n\tEnvironment has been created successfully!"
    print "\n\t#######################################  End  ########################################"

if __name__ == '__main__':
    main()
