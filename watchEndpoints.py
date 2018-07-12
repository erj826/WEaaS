#Eric Jacobson
#erjacobs@redhat.com
#29 June 2018
#
#
#Flask application for the watch endpoints service
#
#


import itertools
import resources.rabbitListener as listener
import os
import threading
from yaml import load
from flask import Flask, Response, stream_with_context
from collections import deque


app = Flask(__name__)
pathToYamlConfig = 'config.yml'


@app.route('/')
def needsEndpoint():
    """No endpoint given"""
    return 'No endpoint specified in the URL!\n'


@app.route('/<endpoint>')
def index(endpoint):
    """Adds a deque to the shared dictionary and performs a 
    transfer via http back to client"""
    addQueueToDict(endpoint)
    #Transfer
    print threading.enumerate()
    def generate():
        while True:
            try:
                #for client in clientThreads():
                #print 'I want to send an event to ' + str(client)
                yield D[endpoint][0].popleft()
                #D[endpoint] = rotate(D[endpoint])
            except:
                pass
    return Response(generate(), mimetype='application/json')


def clientThreads():
    """Returns a list of client threads running"""
    return [thread for thread in threading.enumerate() if thread.name[0:6] == 'Thread']


def addQueueToDict(endpoint):
    """Initialize an empty queue for a client in the shared dictionary"""
    if endpoint in endpoints:
        D[endpoint].append(deque())
        return 'Added event queue to %s key.\n' % endpoint
    else:
        return 'Invalid endpoint!\n'


def readYaml():
    """Returns a list of endpoints from config.yml"""
    config = load(file(pathToYamlConfig, 'r'))
    listsOfEndpoints = [config[service] for service in config]
    endpoints = list(itertools.chain.from_iterable(listsOfEndpoints))
    return endpoints


def rotate(l):
    """Rotates a list by 1"""
    return l[1:] + l[:1]


def initializeDict(endpoints):
    """Initializes the shared dictionary to store endpoint data"""
    for endpoint in endpoints:
        D[endpoint] = []


if __name__ == "__main__":
    #Initialize shared dictionary D with endpoints
    endpoints = readYaml()
    D = {}
    initializeDict(endpoints)

    #Create and start up listener thread
    worker = listener.createListener(D)
    startListener = threading.Thread(target=worker.run, name="Listener").start()
    app.run(threaded=True)
    
    #Terminate app
    print('\n')
    os._exit(0)
        
