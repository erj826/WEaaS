#Eric Jacobson
#erjacobs@redhat.com
#29 June 2018
#
#Flask application for the watch endpoints service
#
#


import resources.rabbitListener as listener
import itertools
from yaml import load
from multiprocessing import Process, Manager
from flask import Flask


app = Flask(__name__)


@app.route('/')
def needsEndpoint():
    return "Please provide an endpoint in the URL\n"


@app.route('/<endpoint>')
def addQueueToDict(endpoint):
    if endpoint in endpoints:
        pass
    else:
        return "Invalid endpoint!\n"


def readYaml():
    """Returns a list of endpoints from config.yml"""
    config = load(file('config.yml', 'r'))
    listsOfEndpoints = [config[service] for service in config]
    endpoints = list(itertools.chain.from_iterable(listsOfEndpoints))
    return endpoints


def initializeDict(D, endpoints):
    """Initializes the shared dictionary to store endpoint data"""
    for endpoint in endpoints:
        D[endpoint] = []
    return


if __name__ == "__main__":
    worker = listener.createListener()
    endpoints = readYaml()
    manager = Manager()
    D = initializeDict(manager.dict(), endpoints)
    startListener = Process(target=worker.run).start()
    app.run()

