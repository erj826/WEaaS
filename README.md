# WEaaS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://u.imageresize.org/v2/44defaa8-3bc5-475f-b210-9239ae35b4fc.png" width="150" />

Watch Endpoints as a Service project for Red Hat. WEaaS is for use with Kuryr and OpenStack.

WEaaS (a.k.a stop polling all the things) is offered as a more efficient alternative to monitor endpoints by tapping directly into Neutron's messaging queue. Currently, the Kuryr Controller polls the Neutron using the OpenStack API to watch for networking events. 
By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information faster than polling.

Intended client: Kuryr Controller

## Supported Endpoints
* Neutron:
  * port

More info [here](https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/port.html).

* LBaaS v2:
  * loadbalancer
  * listener
  * pool
  * member

More info [here](https://docs.openstack.org/mitaka/networking-guide/config-lbaas.html).


## Usage

### Admin: 
#### To start up the gunicorn app server, run:
`gunicorn -b 127.0.0.1:5000 --threads 8 watchEndpoints:app`

More info on gunicorn args [here](http://docs.gunicorn.org/en/stable/settings.html).

### Client:
If Keystone authentication is on, use:

`curl http://127.0.0.1:5000/endpoint -H "X-Auth-Token: $A_VALID_TOKEN"`

If Keystone authentication is off, use:

`curl http://127.0.0.1:5000/endpoint`


_Notes:_

&nbsp;&nbsp;&nbsp;&nbsp; _Authentication can be enabled or disabled from the watchEndpoints.py script_

&nbsp;&nbsp;&nbsp;&nbsp; _Client and server may be terminated by a keyboard interrupt_

***

## WEaaS Developer Guide

### Project Architecture:
<p align="center"><img src="https://github.com/erj826/WEaaS/blob/master/resources/WEaaSArchitecture.png" width="650"/></p>

#### More coming soon...
***
