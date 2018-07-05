#Eric Jacobson
#erjacobs@redhat.com
#2 July 2018
#
#Event queue class 
#

class eventQueue:
    def __init__(self):
        self.events = []

    def notEmpty(self):
        return self.events != []

    def enqueue(self, event):
        self.events.insert(len(self.events), event)

    def dequeue(self):
        return self.events.pop(0)

    def __repr__(self):
        return str(self.events)
