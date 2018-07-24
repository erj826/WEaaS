# Eric Jacobson
# erjacobs@redhat.com
# 23 July 2018

# Clients can use the watch endpoints service by invoking this script


import os
import argparse


#Server is running on:
appURL = 'http://127.0.0.1:5000/'


#Parse command line args
parser = argparse.ArgumentParser(description='Receives desired endpoint')
parser.add_argument('endpoint', type=str, help='endpoint to watch')
args = parser.parse_args()


#######################################################################


def main():
    #curl app server
    query = appURL + args.endpoint
    os.system('curl %s' % query)

    #close connection
    print '\n\nClosing connection...'
    close = query + '/close'
    os.system('curl %s' % close)

    #Exit successfully
    os._exit(0)


#######################################################################


if __name__ == "__main__":
    main()


#######################################################################
