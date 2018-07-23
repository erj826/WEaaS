# WEaaS  
Watch Endpoints as a Service project for Red Hat. WEaaS is used in conjunction with OpenStack.

WEaaS is used as an alternative to OpenStack's APIs. By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information more quickly.

### Supported Endpoints
* Neutron:
  * port

More info: https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/port.html

* Octavia:
  * loadbalancer
  * listener
  * pool
  * member

More info: https://docs.openstack.org/python-octaviaclient/latest/cli/index.html#loadbalancer

* Nova:
  * compute


### Usage

##### To start up the app server, run:
`python watchEndpoints.py`

##### Client usage:
Run the user.py script. Pass it an endpoint as an argument:

`python user.py port`

Client and server should be terminated by a keyboard interrupt.
