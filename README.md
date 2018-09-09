Ansible Openstack modules for create Snapshot and download Image
---------------------------------------------------------------

These modules are not presents in official ansible openstack cloud modules

https://docs.ansible.com/ansible/2.6/modules/list_of_cloud_modules.html

These modules are leveraged by openstack API(shade)

Requirement
-----------

1) Install openstack client
2) pip install shade

Copy this module to python install directory
-------------------------------------------

Copy these python files in to <python home>/site packages/ansible/modules/cloud/openstack

How to run this task in the playbook
------------------------------------

Set you environment authorization using os_auth

https://docs.ansible.com/ansible/2.6/modules/list_of_cloud_modules.html

os_snapshot
-----------

    - name: create snapshot from running instance
      os_snapshot:
        auth: "{{ os_auth }}"
        state: present
        instance_name: "{{ server_name }}"
        snapshot_name: "{{ snapshot_name }}"
        cacert: "{{ lookup('env', 'OS_CACERT') }}"
      register: snapshot

os_image_download
-----------------

    - name: download image from glance
      os_image_download:
        auth: "{{ os_auth }}"
        image_name: "{{ volume_name }}_QCOW2"
        output_file: "/home/jenkins/{{ volume_name }}_QCOW2.qcow2"
        cacert: "{{ lookup('env', 'OS_CACERT') }}"
      register: download


Contact
-------
Thanks for visiting this page. Please contact me if you have further questions.
gogs.ethics@gmail.com




