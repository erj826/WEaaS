#Eric Jacobson
#erjacobs@redhat.com
#29 June 2018
#
#Watch endpoints as a service (WEaaS)
#


import tornado.ioloop
import tornado.web
import itertools
import resources.rabbitListener as listener
import os
import threading
from yaml import load
from resources.client import Client


pathToYamlConfig = 'config.yml'


class MainHandler(tornado.web.RequestHandler):
    """When no endpoint is specified"""
    def get(self):
        self.write('No endpoint specified in the URL!\n')

        
class ClientHandler(tornado.web.RequestHandler):
    """Adds a deque to the shared dictionary and performs a 
    transfer via http back to client"""
    def initialize(self, endpoint):
        self.C = Client()
        self.endpoint = endpoint
        addDequeToDict(self.endpoint, self.C)
        self.write(self.endpoint)
    
    #def get(self, endpoint):
    #    return endpoint
        #self.write(endpoint)


def makeApp():
    """Initialize application"""
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/(\w+)', ClientHandler)
    ])


#Helpers
def addDequeToDict(endpoint, C):
    """Initialize an empty deque for a client in the shared dictionary"""
    if endpoint in endpoints:
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


if __name__ == "__main__":
    #Initialize shared dictionary D with endpoints
    endpoints = readYaml()
    D = {}
    initializeDict(endpoints)

    #Create and start up listener thread
    worker = listener.createListener(D)
    startListener = threading.Thread(target=worker.run, name="Listener").start()
  
    #Run app
    application = makeApp()
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
