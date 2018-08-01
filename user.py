# Eric Jacobson
# erjacobs@redhat.com
# 23 July 2018

# Clients can use the watch endpoints service by invoking this script


import os
import argparse
import subprocess
import shlex
import yaml

#Server is running on:
appURL = 'http://127.0.0.1:5000/'


#Parse command line args
parser = argparse.ArgumentParser(description='Receives desired endpoint')
parser.add_argument('endpoint', type=str, help='endpoint to watch')
args = parser.parse_args()


#######################################################################


def main():
    #Get token
    try:
        token = subprocess.check_output(shlex.split('openstack token issue -f yaml'))
        projectID = yaml.load(token)['project_id']
    except Exception as e:
        print "Error: %s" % e
        print "Curling without token..."
        projectID = 'emptyToken'

    #Curl app server
    try:
        query = appURL + args.endpoint + '/' + projectID
        subprocess.call(shlex.split('curl %s' % query))
    except KeyboardInterrupt as e:
        print '\nClosing connection...\n'

    #Exit
    os._exit(0)


#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
