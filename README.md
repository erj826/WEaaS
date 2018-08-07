# WEaaS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <img src="https://u.imageresize.org/v2/44defaa8-3bc5-475f-b210-9239ae35b4fc.png" width="150" />

Watch Endpoints as a Service project for Red Hat. WEaaS is intended for use in conjunction with Kuryr.

WEaaS (a.k.a stop polling all the things) is offered as a more efficient alternative to monitor endpoints by tapping directly into Neutron's messaging queue. Currently, the Kuryr Controller polls the OpenStack API to watch for networking events. 
By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information faster than polling of the API.

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

### Client:
For ease of testing purposes, 
run the user.py script. Pass it an endpoint as an argument:

`python user.py port`

In production,
curl the url:

`curl http://127.0.0.1:5000/endpoint`

or

`curl http://127.0.0.1:5000/someTokenHere/endpoint`

_Notes:_
&nbsp;&nbsp;&nbsp;&nbsp; _Authentication can be enabled or disabled from the watchEndpoints.py script_
&nbsp;&nbsp;&nbsp;&nbsp; _If authentication is disabled, passing a token is optional_
&nbsp;&nbsp;&nbsp;&nbsp; _Client and server may be terminated by a keyboard interrupt._

***

## WEaaS Developer Guide

### Project Architecture:
<p align="center"><img src="https://github.com/erj826/WEaaS/blob/master/resources/Architecture.png" width="560" align="middle"/></p>
