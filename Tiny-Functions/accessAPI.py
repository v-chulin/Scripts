#########################################
# This scrip show how to access to API  #
#########################################

#!/usr/bin/python

import urllib2
import sys
from optparse import OptionParser

def main():
    # The code below uses OptionParser to gather input to the script #
    parser = OptionParser(usage="Usage: %prog [arguments] -- All the arguments listed below are required!")
    parser.add_option("-u", "--username", dest="username", help="Your account use to login apiinstance")
    parser.add_option("-p", "--password", dest="password", help="Your password")
    (options, args) = parser.parse_args()

    username = options.username
    password = options.password
    apidomain = "APIinstance.domain.test.com"
    api_url = "https://" + apidomain + "/api/"
    timeout = 3000

    # authentication begin #
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, api_url, username, password)
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    # authentication end #

    req = urllib2.Request(url=api_url)
    # If HTTPErr, access fail and exit, else print successful info #
    try:
        response = urllib2.urlopen(req,timeout=int(timeout))
    except Exception as HTTPErr:
        print "\n\tCan't access API due to:\n\t" + str(HTTPErr)
        print "\n\tPlease check if the service is available!"
        sys.exit(1)

    print "\n\tAccess to API, the service is available!"

    cookie = req.unredirected_hdrs.get('Authorization')
    headerWithAuth = {'Content-Type': 'application/xml', 'Authorization': cookie}
    # task_url used for check the tasks via API #
    task_url = "https://" + apidomain + "/api/task/current/all"

    req = urllib2.Request(url=task_url,headers=headerWithAuth)
    response = urllib2.urlopen(req,timeout=int(timeout))
    task_page = response.read()

if __name__=='__main__':
    main()
