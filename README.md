# WEaaS  
Watch Endpoints as a Service project for Red Hat. WEaaS is used in conjunction with OpenStack.

WEaaS is used as an alternative to OpenStack's APIs. By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information more quickly.

### Supported Endpoints
* Neutron:
  * Port

More info: https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/port.html

* Octavia:
  * Loadbalancer
  * Listener
  * Pool
  * Member

More info: https://docs.openstack.org/python-octaviaclient/latest/cli/index.html#loadbalancer


### Usage

##### To start up the app, run:
`python watchEndpoints.py`

##### Client usage:
Curl the server on which the app is running. 
End the url with the desired endpoint.
i.e.

`curl http://127.0.0.1:5000/port`

The app runs until terminated by a client.
