# 
# Adapted from script by celebdor
# Found at: https://gist.github.com/celebdor/06cf4bf06637a72358b982832c366429
#

from eventQueue import eventQueue 
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
 
rabbit_url = "amqp://stackrabbit:pass@192.168.2.4:5672/"
 
class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues
        self.Events = eventQueue()
 
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message])]
 
    def on_message(self, body, message):
        self.Events.enqueue('{0}'.format(body))
        print str(self.Events)
        message.ack()

    #Additional Error Checking:
    # 
    #    def on_connection_error(*args):
    #        print('ERROR: {}'.format(args))
    # 
    #    def on_consume_ready(self, connection, channel, consumers):
    #        print("On consume ready: {}, {}, {}".format(connection, channel, consumers))
    # 
    #    def on_decode_error(self, message, exc):
    #        print("On decode error: {}, {}".format(message, exc))
 

def createListener():  
    exchange = Exchange('neutron', type='topic', durable=False, auto_delete=False)
    queues = [Queue('notifications.info', exchange, routing_key='notifications.info', durable=False, auto_delete=False, exclusive=False)]

    with Connection(rabbit_url, heartbeat=4) as conn:
        worker = Worker(conn, queues)
        return worker
    return None
