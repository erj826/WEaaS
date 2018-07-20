#Eric Jacobson
#erjacobs@redhat.com
#20 July 2018
#
#Watch endpoints as a service (WEaaS)
#


import tornado.ioloop
import tornado.web
import itertools
import resources.rabbitListener as listener
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
    def prepare(self):
        self.C = Client()

    def get(self, endpoint):
        self.write(endpoint)



###Helpers###


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
    Listener = threading.Thread(target=worker.run, name="Listener")
    Listener.daemon = True
    Listener.start()
  
    #Run app
    application = tornado.web.Application()
    application.add_handlers(r'(localhost|127\.0\.0\.1)',
    [
        (r'/', MainHandler),
        (r'/(\w+)', ClientHandler)
    ])
    application.listen(8888)
    
    try: 
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        print('\n')
        tornado.ioloop.IOLoop.current().stop()
