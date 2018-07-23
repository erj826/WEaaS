#Eric Jacobson
#erjacobs@redhat.com
#20 July 2018
#
#Watch endpoints as a service (WEaaS)
#


import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.gen
import tornado.httpclient
import tornado.netutil
import itertools
import resources.rabbitListener as listener
import threading
from yaml import load
from resources.client import Client


pathToYamlConfig = 'config.yml'


##########################################################################


class MainHandler(tornado.web.RequestHandler):
    """When no endpoint is specified"""
    def get(self):
        self.write('No endpoint specified in the URL!\n')

        
class ClientHandler(tornado.web.RequestHandler):
    """Class that handles client connections"""
    #def __init__(self, *path_args, **path_kwargs):
    #    self.stream.set_close_callback(self._onclose)

    def prepare(self):
        """Initializes class variables and adds deque to D"""
        self.C = Client()
        self.endpoint = self.path_args[0]
        addDequeToDict(self.endpoint, self.C)

    @tornado.gen.coroutine
    def transfer(self):
        while self.C.connected:
            try:
                yield self.write(self.C.deque.popleft())
            except IndexError:
                pass

    @tornado.gen.coroutine
    def get(self, *path_args, **path_kwargs):
        """"""
        print "Connected to client at %s" % self.request.remote_ip
        raise tornado.gen.Return(self.transfer())


    def on_finish(self):
        """Remove deque from D"""
        D[self.endpoint].remove(self.C.deque)


##########################################################################


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


##########################################################################


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
  
    #Initialize app
    application = tornado.web.Application()
    application.add_handlers(r'(localhost|127\.0\.0\.1)',
    [
        tornado.web.URLSpec(r'/', MainHandler),
        tornado.web.URLSpec(r'/(\w+)', ClientHandler)
    ])

    port = 8888
    server = tornado.httpserver.HTTPServer(application)
    server.listen(port)
    print "Running on port: %s" % port
    
    #Run app
    try: 
        tornado.ioloop.IOLoop.current().start()

    except KeyboardInterrupt:
        print('\n')
        tornado.ioloop.IOLoop.current().stop()


##########################################################################
