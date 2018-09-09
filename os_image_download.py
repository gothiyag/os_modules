#!/usr/bin/python

# Copyright (c) 2017 Nokia.
# Copyright (c) 2017, Gogs <gogulakrishnan.thiyagarajan@nokia.com>
#TODO(mordred): we need to support "location"(v1) and "locations"(v2)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: os_image_download
short_description: Download image from upstream
description:
   - Download image from upstream and save it in local file
options:
   :
   os_auth
     description:
        - Openstack auth credential.
     required: true
   image_name:
     description:
        - Name of the image from upstream
     required: true
   output_file
     description:
       - location where the file stored
     required: true
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
- os_image_download:
       os_auth: "{{auth}}"
       image_name: image1
       output_file: /tm/image1
'''

try:
    import shade
    HAS_SHADE = True
except ImportError:
    HAS_SHADE = False

def _download_image(module, cloud, image):
    try:
        result = cloud.download_image(image,module.params['output_file'],None)
    except Exception, e:
        module.fail_json(msg="There was an error downloading the image: %s" % e.message)
    module.exit_json(changed=True, result='image downloaded successfully!' )

def _get_image(module, cloud):
    image = None
    try:
        image = cloud.get_image(module.params['image_name'])
    except Exception, e:
        module.fail_json(msg = "Error in getting image: %s" % e.message)
    if image:
        return image.name


def main():

    argument_spec = openstack_full_argument_spec(
        image_name     = dict(required=True),
        output_path    = dict(default=None),
        output_file    = dict(required=True),
    )
    module_kwargs = openstack_module_kwargs(
        mutually_exclusive=[
            ['output_path', 'output_file'],
        ],
    )

    module = AnsibleModule(argument_spec, **module_kwargs)

    if not HAS_SHADE:
        module.fail_json(msg='shade is required for this module')

    try:
        cloud = shade.openstack_cloud(**module.params)
	image = _get_image(module, cloud)
	if image:
            _download_image(module, cloud, image)
        else:
            module.exit_json(changed=False)

    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
from ansible.module_utils.openstack import *

if __name__ == "__main__":
    main()
