# WEaaS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://u.imageresize.org/v2/44defaa8-3bc5-475f-b210-9239ae35b4fc.png" width="150" />

Watch Endpoints as a Service project for Red Hat. WEaaS is used in conjunction with OpenStack.

WEaaS (a.k.a Stop Polling All the Things) is used as a faster alternative to monitor endpoints by avoiding the repeated usage of the OpenStack API. By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information faster and more efficiently than repeated polling of the API.

Intended client: Kuryr Controller

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
`gunicorn -b 127.0.0.1:5000 --threads 8 watchEndpoints:app`

More info on gunicorn args [here](http://docs.gunicorn.org/en/stable/settings.html).

_Notes:_

&nbsp;&nbsp;&nbsp;&nbsp; _Authentication can be enabled or disabled from the watchEndpoints.py script_

### Client:
Run the user.py script. Pass it an endpoint as an argument:

`python user.py port`


_Note: Client and server should be terminated by a keyboard interrupt._
