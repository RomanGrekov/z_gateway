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
    _instance = None

    def __init__(self, device=None, config=None):
        pass

    def init(self, device, config):
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

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
            class_._instance.init(*args, **kwargs)
            class_._instance.start(300)
        return class_._instance

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

    def get_home_id(self):
        return self.network.home_id

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
    def __del__(self):
        print "close!!!!"
        self.network.close()


