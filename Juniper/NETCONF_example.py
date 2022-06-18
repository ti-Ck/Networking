from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from pprint import pprint

dev1 = Device(host='172.16.10.1', user='root', password='Password3')
dev1.open()

try:
    dev1.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)

hostname = dev1.facts['hostname']
print("Hostname:", hostname)

facts = dev1.facts
pprint(facts)
dev1.close()
