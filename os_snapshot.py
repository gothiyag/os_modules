#!/usr/bin/python

# Copyright (c) 2017, Gogs <gogs.ethics@gmail.com>
#TODO(mordred): we need to support "location"(v1) and "locations"(v2)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: os_snapshot
short_description: Create a snapshot of a running instance
description:
   - Create a snapshot of a running instance
options:
   :
   os_auth
     description:
        - Openstack auth credential.
     required: true
   state:
     description:
        - Indicate desired state of the resource
     choices: ['present', 'absent']
     default: present
   instance_name:
     description:
        - Name that has to be given to the instance
     required: true
     default: None
   snapshot_name
     description:
       - Name given to the snapshot to be created
     required: true
     default: None
requirements: ["shade"]
'''

EXAMPLES = '''
# Set necessary variables for Openstack Auth and other tasks
- set_fact:
    os_auth:
       auth_url: "{{ lookup('env', 'OS_AUTH_URL') }}"
       username: "{{ lookup('env', 'OS_USERNAME') }}"
       password: "{{ lookup('env', 'OS_PASSWORD') }}"
       project_name: "{{ lookup('env', 'OS_PROJECT_NAME') }}"
       project_domain_name: default
       user_domain_name: default
#Creates a new new snapshot of the instance
- os_snapshot:
       os_auth: "{{auth}}"
       state: present
       instance_name: vm1
       snapshot_name: vm1_snapshot1
'''

try:
    import shade
    HAS_SHADE = True
except ImportError:
    HAS_SHADE = False

def _create_snapshot(module, cloud, server):
    try:
        result = cloud.create_image_snapshot(module.params['snapshot_name'],server)
    except Exception, e:
        module.fail_json(msg="There was an error snapshoting the instance: %s" % e.message)
    module.exit_json(changed=True, result=result )

def _get_server(module, cloud):
    server = None
    state = module.params['state']
    try:
        server = cloud.get_server(module.params['instance_name'])
    except Exception, e:
        module.fail_json(msg = "Error in getting the server list: %s" % e.message)
    if server and state == 'present':
        if server.status != 'ACTIVE':
            module.fail_json( msg="The VM is available but not Active. state:" + server.status)
    return server


def main():

    argument_spec = openstack_full_argument_spec(
        instance_name     = dict(required=True),
        snapshot_name     = dict(required=True),
        state             = dict(default='present', choices=['absent', 'present']),
    )
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    if not HAS_SHADE:
        module.fail_json(msg='shade is required for this module')

    try:
        cloud = shade.openstack_cloud(**module.params)
	server = _get_server(module, cloud)
	if server:
            _create_snapshot(module, cloud, server)
        else:
            module.exit_json(changed=False)

    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *

if __name__ == "__main__":
    main()
