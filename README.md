# WEaaS
Project for Red Hat. WEaaS is used in conjunction with OpenStack.

WEaaS is used as an alternative to OpenStack's slow APIs. By communicating directly with RabbitMQ, OpenStack's messaging service, WEaaS is able to return endpoint information more quickly.

### Supported Endpoints
Neutron:
..* Port

More info: https://docs.openstack.org/python-openstackclient/pike/cli/command-objects/port.html

Octavia:
..* Load Balancer
..* Listener
..* Pool
..* Member

More info: https://docs.openstack.org/python-octaviaclient/latest/cli/index.html#loadbalancer
