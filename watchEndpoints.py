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
import logging
from keystonemiddleware import auth_token
from yaml import load
from flask import Flask, Response
from resources.client import Client
from werkzeug.contrib import fixers


import configparser
config = configparser.ConfigParser()
config.read('api-paste.ini')

#Initialize app with or without Keystone Authentication
AUTH_REQUIRED = True

app = Flask(__name__) 
if AUTH_REQUIRED:
    app.wsgi_app = auth_token.AuthProtocol(app.wsgi_app, config)
    app.wsgi_app = fixers.ProxyFix(app.wsgi_app)

pathToYamlConfig = 'config.yml'
D = {}


#Debug log (prints to stdout)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

#Note: use app.logger.debug("hello world") to print messages to stdout

############################################################################


@app.route('/')
def needsEndpoint():
    """No endpoint given"""
    return 'No endpoint specified in the URL!\n'


@app.route('/<endpoint>')
def index(endpoint):
    """Adds a deque to the shared dictionary, D, and performs a
    transfer via http back to client"""

    if endpoint not in D.keys():
        return 'Invalid endpoint!'

    #Initialize client object
    C = Client()

    #Generate a chunked http response for the client
    def generate():
        """Generator with an infinite loop listening for events in D"""
        addDequeToDict(endpoint, C)

        while True:
            if len(C.deque) > 0:
                event = C.deque.popleft()

                try:
                    yield str(event) + '\n\n'
                except GeneratorExit:
                    app.logger.debug('Detected client disconnect.')
                    break

        #Remove the client's deque from the shared dictionary
        D[endpoint].remove(C.deque)

    return Response(generate(), mimetype='application/json')


############################################################################


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


def configureListener():
    """Configure and start up listener"""
    #Initialize shared dictionary D with endpoints
    endpoints = readYaml()
    initializeDict(endpoints)

    #Create and start up listener thread
    worker = listener.createListener(D)
    startListener = threading.Thread(target=worker.run, name='Listener').start()

configureListener()


############################################################################
