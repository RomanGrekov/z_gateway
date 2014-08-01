#!/usr/bin/python2.7

import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
from louie import dispatcher, All
import sys

device = "/dev/ttyUSB0"
options = ZWaveOption(device, config_path="python-openzwave/openzwave/config", user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level('Debug')
options.set_logging(True)
network = None

options.lock()
network = ZWaveNetwork(options, autostart=False)

def louie_network_started(network):
    print("Hello from network : I'm started : homeid %0.8x - %d nodes were found." % (network.home_id, network.nodes_count))

def louie_network_failed(network):
    print("Hello from network : can't load :(.")

def louie_network_ready(network):
    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
    print("Hello from network : my controller is : %s" % network.controller)
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

def louie_node_update(network, node):
    print('Hello from node : %s.' % node)

def louie_value_update(network, node, value):
    print('Hello from value : %s.' % value)

dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

network.start()

for i in range(0,90):
    if network.state>=network.STATE_READY:
        print "***** Network is ready"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

network.controller.node.name = "Test node"
#time.sleep(10.0)

network.controller.node.location = "Test location"
#time.sleep(120.0)

print "we are done"
'''
ctrl1 = ZWaveController(1, network)
if ctrl1.begin_command_add_device():
    print "Enrolling is started"
'''
print "Nodes in network : %s" % network.nodes_count

for node in network.nodes:
    print
    print "------------------------------------------------------------"
    print "%s - Name : %s" % (network.nodes[node].node_id,network.nodes[node].name)
    print "%s - Manufacturer name / id : %s / %s" % (network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id)
    print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
    print "%s - Version : %s" % (network.nodes[node].node_id, network.nodes[node].version)
    print "%s - Command classes : %s" % (network.nodes[node].node_id,network.nodes[node].command_classes_as_string)
    print "%s - Capabilities : %s" % (network.nodes[node].node_id,network.nodes[node].capabilities)
    print "%s - Neigbors : %s" % (network.nodes[node].node_id,network.nodes[node].neighbors)
    print "%s - Can sleep : %s" % (network.nodes[node].node_id,network.nodes[node].can_wake_up())
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print "%s - Groups : %s" % (network.nodes[node].node_id, groups)
    values = {}
    for val in network.nodes[node].values :
        values[network.nodes[node].values[val].object_id] = {
            'label':network.nodes[node].values[val].label,
            'help':network.nodes[node].values[val].help,
            'command_class':network.nodes[node].values[val].command_class,
            'max':network.nodes[node].values[val].max,
            'min':network.nodes[node].values[val].min,
            'units':network.nodes[node].values[val].units,
            'data':network.nodes[node].values[val].data_as_string,
            'ispolled':network.nodes[node].values[val].is_polled
            }

    #print "%s - Values : %s" % (network.nodes[node].node_id, values)
    #print "------------------------------------------------------------"
    for cmd in network.nodes[node].command_classes:
        print "   ---------   "
        #print "cmd = ",cmd
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        #print "%s - Values for command class : %s : %s" % (network.nodes[node].node_id,
        #                            network.nodes[node].get_command_class_as_string(cmd),
        #                            values)
        print "type: %s" % network.nodes[node].values[val].type
    print "------------------------------------------------------------"
print "------------------------------------------------------------"


for node in network.nodes:
    for val in network.nodes[node].get_switches():
        print("Activate switch")
        network.nodes[node].set_switch(val,True)
        time.sleep(10.0)
        print("Deactivate switch")
        network.nodes[node].set_switch(val,False)
    #We only activate the first switch
    #exit
time.sleep(120.0)


network.stop()
