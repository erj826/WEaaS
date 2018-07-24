# 
# Adapted from script by celebdor
# Found at: https://gist.github.com/celebdor/06cf4bf06637a72358b982832c366429
#

 
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

 
rabbit_url = "amqp://stackrabbit:pass@192.168.2.4:5672/"


##########################################################################
 

class Worker(ConsumerMixin):
    def __init__(self, connection, queues, D):
        self.connection = connection
        self.queues = queues
        self.D = D
        self.debug = True
 
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]
 
    def on_message(self, body, message):
        #Add to deques based on message type
        try:
            endpoint = body['event_type'].split('.')[0]
            for deque in self.D[endpoint]:
                deque.append('{0}'.format(body))
        except:
            if self.debug:
                print 'Unable to place message: ' + '{0}'.format(body)
            else:
                pass
        message.ack()


############################################################################


def createListener(D):  
    exchange = Exchange('neutron', type='topic', durable=False, auto_delete=False)
    queues = [Queue('notifications.info', exchange, routing_key='notifications.info', durable=False, auto_delete=False, exclusive=False)]

    with Connection(rabbit_url, heartbeat=4) as conn:
        worker = Worker(conn, queues, D)
        return worker
    return None


###########################################################################
