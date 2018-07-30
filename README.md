# WEaaS  
Watch Endpoints as a Service project for Red Hat. WEaaS is used in conjunction with OpenStack.

WEaaS is used as an alternative to OpenStack's APIs. By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information faster than the API can.

## Supported Endpoints
* Neutron:
  * port

More info [here](https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/port.html).

* Octavia:
  * loadbalancer
  * listener
  * pool
  * member

More info [here](https://docs.openstack.org/python-octaviaclient/latest/cli/index.html#loadbalancer).

* Nova:
  * compute


## Usage

### Admin: 
#### To start up the gunicorn app server, run:
`gunicorn -b 127.0.0.1:5000 --threads 24 watchEndpoints:app`

More info on gunicorn args [here](http://docs.gunicorn.org/en/stable/settings.html).

_Notes:_

  _each client requires 2 threads_
  
  _authentication can be enabled or disabled from the watchEndpoints.py script__

### Client:
Run the user.py script. Pass it an endpoint as an argument:

`python user.py port`

Client and server should be terminated by a keyboard interrupt.
