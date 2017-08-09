#!/usr/bin/env python

# http://docs.ansible.com/ansible/dev_guide/developing_api.html

import enum
import json
import os
import sys

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
import jinja2
import yaml


class Network(enum.Enum):
    DEFAULT = 'network_interface'
    CLUSTER = 'cluster_interface'
    INTERNAL = 'api_interface'
    NEUTRON_EXTERNAL = 'neutron_external_interface'
    STORAGE = 'storage_interface'
    TUNNEL = 'tunnel_interface'
    VIP_EXTERNAL = 'kolla_external_vip_interface'


GLOBALSFILE = os.environ.get('GLOBALSFILE', 'samples/globals.yml')
INVENTORYFILE = os.environ.get('INVENTORYFILE', 'samples/inventory')

TEMPLATEFILE = 'nwdiag.j2'
GROUPS = {
    'manager': [Network.INTERNAL],
    'network': [Network.INTERNAL, Network.VIP_EXTERNAL, Network.NEUTRON_EXTERNAL, Network.TUNNEL],
    'compute': [Network.INTERNAL, Network.TUNNEL, Network.STORAGE],
    'control': [Network.INTERNAL, Network.CLUSTER],
    'storage': [Network.INTERNAL, Network.CLUSTER, Network.STORAGE]
}


def get_hosts_in_group(inventory, group):
    hosts = []
    for host in inventory.list_hosts(group):
        hosts.append(str(host))
    return hosts


def load_inventory_from_file(inventoryfile):
    inventory = Inventory(
        loader = DataLoader(),
        variable_manager = VariableManager(),
        host_list = inventoryfile
    )
    return inventory

def load_vars_from_file(varsfile):
    vars = yaml.load(open(varsfile))

    if Network.DEFAULT.value not in vars:
        print "%s has to be set in %s" % (Network.DEFAULT.value, varsfile)
        sys.exit(1)

    for interface in Network:
        if interface.value not in vars:
            vars[interface.value] = vars[Network.DEFAULT.value]

    return vars

loader = jinja2.FileSystemLoader(searchpath="templates/")
environment = jinja2.Environment(loader=loader)
template = environment.get_template(TEMPLATEFILE)

inventory = load_inventory_from_file(INVENTORYFILE)
vars = load_vars_from_file(GLOBALSFILE)

networks = {}
for network in Network:
    networks[network.value] = {
        'name': str(network),
#        'cidr': '1.2.3.0/24',
        'nodes': []
    }

groups = {}
for group in GROUPS.keys():
    hosts = get_hosts_in_group(inventory, group)
    groups[group] = []

    for host in hosts:
        hostvars = inventory.get_vars(host)
        groups[group].append(hostvars['inventory_hostname_short'])
        for network in GROUPS[group]:
            networks[network.value]['nodes'].append({
                'name': hostvars['inventory_hostname_short'],
                'device': hostvars.get(network.value, vars[network.value])
#                'address': '1.2.3.4'
            })

result = template.render({
    'groups': groups,
    'networks': networks,
    'internal_vip': vars.get('kolla_internal_vip_address', 'n/a'),
    'external_vip': vars.get('kolla_external_vip_address', 'n/a')
})

print result
