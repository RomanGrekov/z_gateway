#!/usr/bin/python2.7

from start_network import ZNetwork

network = ZNetwork()
print "\nNetwork start successful!"
if network.get_nodes_count() > 1:
    for node in network.get_nodes_full_info():
        print node

    node = network.get_node(2)
    while True:
        command = input("Set command (on, off, get_val):\n\n")
        if command == "on":
            for val in node.get_switches():
                print "Switcher: %s" % val
                node.set_switch(val, True)
        if command == "off":
            for val in node.get_switches():
                print "Switcher: %s" % val
                node.set_switch(val, False)
        if command == "get_val":
            for val in node.get_sensors():
                print "Sensor: %s" % val
                print "Sensor val: %s" % node.get_sensor_value(val)

