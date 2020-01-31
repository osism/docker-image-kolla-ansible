import re
import os

import ruamel.yaml

SITEFILE = "/repository/ansible/site.yml"
DSTPATH = "/ansible"

UNSUPPORTED_ROLES = [
    "baremetal",
    "ceph",
    "opendaylight"
]

with open(SITEFILE, "r") as fp:
    site = ruamel.yaml.safe_load(fp)

for play in site:
    if "name" not in play:
        continue

    if play["name"].startswith("Apply role"):
        name = re.sub(r"\s+", "", play["name"][11:])
        print("PROCESS ROLE %s" % name)

        if name in UNSUPPORTED_ROLES:
            print("ROLE %s IS NOT SUPPORTED" % name)

        else:
            play["gather_facts"] = "no"
            dump = ruamel.yaml.dump([play], Dumper=ruamel.yaml.RoundTripDumper, indent=4, block_seq_indent=2)
            if name == "rabbitmq(outward)":
                name = "rabbitmq-outward"

            with open(os.path.join(DSTPATH, "kolla-%s.yml" % name), "w+") as fp:
                fp.write("---\n")
                for line in dump.splitlines():
                    fp.write(line[2:])
                    fp.write("\n")

            with open(os.path.join(DSTPATH, "awx-kolla-%s.yml" % name), "w+") as fp:
                fp.write("---\n")
                for line in dump.splitlines():
                    fp.write(line[2:])
                    fp.write("\n")

                fp.write("  vars_files:\n")
                fp.write("    - /opt/configuration/environments/configuration.yml\n")
                fp.write("    - /opt/configuration/environments/images.yml\n")
                fp.write("    - /opt/configuration/environments/secrets.yml\n")
                fp.write("    - /opt/configuration/environments/kolla/configuration.yml\n")
                fp.write("    - /opt/configuration/environments/kolla/images.yml\n")
                fp.write("    - /opt/configuration/environments/kolla/secrets.yml\n")
