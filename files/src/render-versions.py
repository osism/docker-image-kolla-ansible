import os

import jinja2
import yaml

# get environment parameters

VERSION = os.environ.get("VERSION", "latest")
OPENSTACK_VERSION = os.environ.get("OPENSTACK_VERSION", "latest")

# load versions files from release repository

with open("/release/%s/base.yml" % VERSION, "rb") as fp:
    versions = yaml.load(fp, Loader=yaml.FullLoader)

# prepare jinja2 environment

loader = jinja2.FileSystemLoader(searchpath="/src/templates/")
environment = jinja2.Environment(loader=loader)

# render versions.yml

template = environment.get_template("versions.yml.j2")

if VERSION == "latest":
    result = template.render({
      'openstack_version': OPENSTACK_VERSION,
      'openstackclient_version': OPENSTACK_VERSION
    })
else:
    with open("/release/%s/openstack.yml" % VERSION, "rb") as fp:
        versions_openstack = yaml.load(fp, Loader=yaml.FullLoader)

    result = template.render({
      'openstack_version': versions['manager_version'],
      'openstackclient_version': versions_openstack['docker_images']['openstackclient'] 
    })

with open("/ansible/group_vars/all/versions.yml", "w+") as fp:
    fp.write(result)

# render motd

template = environment.get_template("motd.j2")
result = template.render({
  'manager_version': versions['manager_version']
})
with open("/etc/motd", "w+") as fp:
    fp.write(result)
