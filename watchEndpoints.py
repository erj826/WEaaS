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
from resources.eventQueue import eventQueue
from yaml import load
from multiprocessing import Process, Manager
from flask import Flask


app = Flask(__name__)


@app.route('/')
def needsEndpoint():
    """No endpoint given"""
    return "No endpoint specified in the URL!\n"


@app.route('/<endpoint>')
def addQueueToDict(endpoint):
    """Initialize an empty queue for a client in the shared dictionary"""
    if endpoint in endpoints:
        #Following line isn't doing anything. Should be appending a queue to the list 
        #D[endpoint].append(eventQueue())
        #print D
        return "added event queue to %s key\n" % endpoint
    else:
        return "Invalid endpoint!\n"


def readYaml():
    """Returns a list of endpoints from config.yml"""
    config = load(file('config.yml', 'r'))
    listsOfEndpoints = [config[service] for service in config]
    endpoints = list(itertools.chain.from_iterable(listsOfEndpoints))
    return endpoints


def initializeDict(endpoints):
    """Initializes the shared dictionary to store endpoint data"""
    for endpoint in endpoints:
        D[endpoint] = manager.list()


if __name__ == "__main__":
    worker = listener.createListener()
    endpoints = readYaml()
    manager = Manager()
    D = manager.dict()
    initializeDict(endpoints)
    startListener = Process(target=worker.run).start()
    app.run()

