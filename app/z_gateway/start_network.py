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

def louie_network_started(network):
    print("Network:\n    Started: homeid: %0.8x - %d nodes were found." % (network.home_id, network.nodes_count))

def louie_network_failed(network):
    print("Network: can't load :(.")

def louie_network_ready(network):
    print("Network:\n    Controller is: %s" % network.controller)
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

def louie_node_update(network, node):
    print('Node:\n    %s.' % node)

def louie_value_update(network, node, value):
    print('Value:\n    %s.' % value)

class ZNetwork(object):
    def __init__(self, device, config):
        self.device = device
        self.config = config

        options = ZWaveOption(self.device, config_path=self.config, user_path=".", cmd_line="")
        options.set_log_file("OZW_Log.log")
        options.set_append_log_file(False)
        options.set_console_output(False)
        options.set_save_log_level('Debug')
        options.set_logging(True)
        self.network = None

        options.lock()
        self.network = ZWaveNetwork(options, autostart=False)

        dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
        dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def start(self, timeout):
        print "Start network... "
        self.network.start()

        for i in range(0,timeout):
            if self.network.state >= self.network.STATE_READY:
                return 0
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(1.0)
        return 1

    def stop(self):
        self.network.stop()

    def get_node(self, node_id):
        return self.network.nodes[node_id]

    def get_nodes_count(self):
        return self.network.nodes_count

    def get_nodes(self):
        return self.network.nodes

    def get_nodes_ids(self):
        return [self.network.nodes[node].node_id for node in self.get_nodes()]

    def get_nodes_full_info(self):
        nodes = []
        for node_key in self.get_nodes():
            node = self.network.nodes[node_key]
            node_id = node.node_id
            node_dict = {}
            node_dict["Id"] = node_id
            node_dict["Name"] = node.name
            node_dict["ManufactName"] = node.manufacturer_name
            node_dict["ProductName"] = node.product_name
            node_dict["Version"] = node.version
            node_dict["CmdClasses"] = node.command_classes_as_string
            node_dict["Capabilities"] = node.capabilities
            node_dict["Neigbors"] = node.neighbors
            node_dict["CanSleep"] = node.can_wake_up()
            nodes.append(node_dict)
        return nodes

        '''
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
        '''

#network.controller.node.name = "Test node"
#time.sleep(10.0)

#network.controller.node.location = "Test location"
#time.sleep(120.0)
'''
print "we are done"
print "Nodes in network : %s" % network.nodes_count


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
'''

device = "/dev/ttyUSB0"
config = "../../python-openzwave/openzwave/config"

network = ZNetwork(device, config)
if network.start(180) == 1:
    print "\nNetwork start fail!"

else:
    print "\nNetwork start successful!"
    if network.get_nodes_count() > 1:
        for node in network.get_nodes_full_info():
            print node

        node = network.get_node(2)
        for val in node.get_switches():
            print "Switcher: %s" % val
            node.set_switch(val, True)
        for val in node.get_sensors():
            print "Sensor: %s" % val
            print "Sensor val: %s" % node.get_sensor_value(val)
    time.sleep(100)
network.stop()
