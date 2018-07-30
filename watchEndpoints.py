#Eric Jacobson
#erjacobs@redhat.com
#29 June 2018
#
#Watch endpoints as a service (WEaaS)
#


import itertools
import resources.rabbitListener as listener
import os
import sys
import threading
from yaml import load
from flask import Flask, Response
from resources.client import Client


app = Flask(__name__)
pathToYamlConfig = 'config.yml'
AUTH_REQUIRED = True 
D = {}



############################################################################


@app.route('/')
def needsEndpoint():
    """No endpoint given"""
    return 'No endpoint specified in the URL!\n'


@app.route('/<endpoint>', defaults={'projectID': 'emptyToken'})
@app.route('/<endpoint>/<projectID>')
def index(endpoint, projectID):
    """Adds a deque to the shared dictionary and performs a
    transfer via http back to client"""

    #verify that client curled with correct args
    if (projectID == 'emptyToken') and (endpoint != 'close') and (AUTH_REQUIRED):
        return "Can't authenticate token!"

    if endpoint == 'close':
        return close()

    if endpoint not in D.keys():
        return 'Invalid endpoint!'

    #client is connected, boolean will be set to False when client disconnects
    global Connected
    Connected = True

    C = Client()
    C.projectID = projectID


    #generate a chunked http response for the client
    def generate():
        """Infinite loop listening for events in the deques"""
        addDequeToDict(endpoint, C)

        while Connected:
            if len(C.deque) > 0:
                event = C.deque.popleft()
                if (event['payload']['port']['project_id'] == C.projectID) or (not AUTH_REQUIRED):
                    yield str(event) + "\n\n"

        #remove the client's deque from the shared dictionary
        D[endpoint].remove(C.deque)

    return Response(generate(), mimetype='application/json')


############################################################################


def close():
    """Close connection"""
    Connected = False
    return '\n'


def addDequeToDict(endpoint, C):
    """Initialize an empty deque for a client in the shared dictionary"""
    if endpoint in D.keys():
        D[endpoint].append(C.deque)
        return 'Added event queue to %s key.\n' % endpoint
    else:
        return 'Invalid endpoint!\n'


def readYaml():
    """Returns a list of endpoints from config.yml"""
    config = load(file(pathToYamlConfig, 'r'))
    listsOfEndpoints = [config[service] for service in config]
    endpoints = list(itertools.chain.from_iterable(listsOfEndpoints))
    return endpoints


def initializeDict(endpoints):
    """Initializes the shared dictionary to store endpoint data"""
    for endpoint in endpoints:
        D[endpoint] = []


############################################################################


def configure_listener():
    #Initialize shared dictionary D with endpoints
    endpoints = readYaml()
    initializeDict(endpoints)

    #Create and start up listener thread
    worker = listener.createListener(D)
    startListener = threading.Thread(target=worker.run, name="Listener").start()

configure_listener()
