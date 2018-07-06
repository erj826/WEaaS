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
from yaml import load
from flask import Flask, request
from threading import Thread
from collections import deque


app = Flask(__name__)
pathToYamlConfig = 'config.yml'


@app.route('/')
def needsEndpoint():
    """No endpoint given"""
    return 'No endpoint specified in the URL!\n'


@app.route('/<endpoint>')
def addQueueToDict(endpoint):
    """Initialize an empty queue for a client in the shared dictionary"""
    if endpoint in endpoints:
        D[endpoint].append(deque())
        return 'added event queue to %s key\n' % endpoint
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


if __name__ == "__main__":
    worker = listener.createListener()
    endpoints = readYaml()
    D = {}
    initializeDict(endpoints)
    startListener = Thread(target=worker.run).start()
    app.run()
