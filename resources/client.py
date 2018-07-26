#Eric Jacobson
#erjacobs@redhat.com
#
#13 July 2018
#
#Client class
#

from collections import deque

class Client():
    def __init__(self):
        self.deque = deque()
        self.projectID = ''
