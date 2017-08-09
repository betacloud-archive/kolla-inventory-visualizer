# Kolla Inventory Visualizer (KIV)

The ``Kolla Inventory Visualizer`` is a Python script that creates a simple network-diagram from
a ``kolla-ansible`` configuration and inventory file.

## Environment variables

* ``GLOBALSFILE``:  path to the ``globals.yml`` file
* ``INVENTORYFILE``: path to the ``inventory`` file

## Sample usage

![visualized kolla inventory](https://github.com/betacloud/kolla-inventory-visualizer/raw/master/samples/sample.png "visualized kolla inventory")

```code
# virtualenv venv
# source venv/bin/activate
# pip install -r requirements.txt
# GLOBALSFILE=samples/globals.yml INVENTORYFILE=samples/inventory python src/kiv.py > samples/sample.diag
# nwdiag samples/sample.diag -o samples/sample.png
```

## References

* [kolla-ansible - Ansible deployment of the Kolla containers](https://github.com/openstack/kolla-ansible)
* [nwdiag - simple network-diagram image generators](http://blockdiag.com/en/nwdiag/)

## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Author information

This script was created by [Betacloud Solutions GmbH](https://betacloud-solutions.de).
