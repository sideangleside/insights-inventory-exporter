#!/usr/bin/env python

# File: insights-inventory-exporter.py
# Author: Rich Jerrido <rjerrido@outsidaz.org>
# Purpose: 
#          
#          
#          
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import json
import requests
import getpass
import os
import urllib2
import urllib
import base64
import sys
import ssl
import csv
from optparse import OptionParser

default_login     = "default"
default_password  = ""
default_server = "cloud.redhat.com"

parser = OptionParser()
parser.add_option("-l", "--login", dest="login", help="Login user", metavar="LOGIN", default=default_login)
parser.add_option("-f", "--filename", dest="filename", help="Login user", metavar="FILENAME")
parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD", default=default_password)
parser.add_option("-s", "--server", dest="server", help="FQDN of server - omit https://", metavar="SERVER", default=default_server)
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="Verbose output")
parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Debugging output (debug output enables verbose)")
(options, args) = parser.parse_args()



class error_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# if not (options.login and options.server):
#     print "Must specify login, server, and orgid options.  See usage:"
#     parser.print_help()
#     print "\nExample usage: ./insights-inventory-exporter.py -l admin -s cloud.redhat.com"
#     sys.exit(1)
# else:
#     login = options.login
#     password = options.password
#     server = options.server


if options.filename:
    FILENAME = options.filename
    FILEINPUTMODE = True
elif not (options.login and options.server):
    print "Must specify login, server, and orgid options.  See usage:"
    parser.print_help()
    print "\nExample usage: ./insights-inventory-exporter.py -l admin -s cloud.redhat.com"
    sys.exit(1)
else:
    FILEINPUTMODE = False

login = options.login
password = options.password
server = options.server

if not (FILEINPUTMODE or password):
     password = getpass.getpass("%s's password:" % login)

if options.debug:
    DEBUG = True
    VERBOSE = True
    print "[%sDEBUG%s] LOGIN -> %s " % (error_colors.OKBLUE, error_colors.ENDC, login)
    print "[%sDEBUG%s] PASSWORD -> %s " % (error_colors.OKBLUE, error_colors.ENDC, password)
    print "[%sDEBUG%s] SERVER -> %s " % (error_colors.OKBLUE, error_colors.ENDC, server)
else:
    DEBUG = False
    VERBOSE = False

if options.verbose:
    VERBOSE = True



if DEBUG and not FILEINPUTMODE:
    outputfile = open(("cloud.redhat.com_output-%s.json" % login), "w")

systemdata = []
if FILEINPUTMODE:
    f = open(FILENAME,"r")
    jsondata = json.load(f)
    systemdata = jsondata['results']
else:
    try:
        url = 'https://' + server + '/api/inventory/v1/hosts'
        if VERBOSE:
            print "=" * 80
            print "[%sVERBOSE%s] Connecting to -> %s " % (error_colors.OKGREEN, error_colors.ENDC, url)
        result = requests.get(url, auth=(login, password)).content
        jsonresult = json.loads(result)

        if VERBOSE:
            print
            "=" * 80
    except urllib2.URLError, e:
        print
        "Error: cannot connect to the API: %s" % (e)
        print
        "Check your URL & try to login using the same user/pass via the WebUI and check the error!"
        sys.exit(1)
    except Exception, e:
        print
        "FATAL Error - %s" % (e)
        sys.exit(2)

    try:
        page = 0
        per_page = 100
        while (page == 0 or int(jsonresult['per_page']) == len(jsonresult['results'])):
            page += 1
            q = [('page', page), ('per_page', per_page)]
            url = "https://cloud.redhat.com/api/inventory/v1/hosts?" + urllib.urlencode(q)
            if VERBOSE:
                print "=" * 80
                print "[%sVERBOSE%s] Connecting to -> %s " % (error_colors.OKGREEN, error_colors.ENDC, url)
            result = requests.get(url, auth=(login, password)).content
            jsonresult = json.loads(result)
            systemdata += jsonresult['results']
            if DEBUG:
                outputfile.write(result)

    except Exception, e:
        print "FATAL Error - %s" % (e)
        sys.exit(2)

if DEBUG and not FILEINPUTMODE:
    outputfile.close()


for system in systemdata:
	print "=" * 80
	print "%s Reported by -> %s" % (system['display_name'], system['reporter'])
	if system.has_key('facts'):
		print "  Facts"
		for entry in system['facts']:
			print "    Namespace - %s" % entry['namespace']
			for fact, value in entry['facts'].iteritems():
				print "      %s,%s" % (fact,value) 

