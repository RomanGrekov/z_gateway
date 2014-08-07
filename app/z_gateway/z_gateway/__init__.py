import os, sys
sys.path.append(os.path.abspath("../"))
from start_network import ZNetwork
config = os.path.abspath("../../python-openzwave/openzwave/config")
device = "/dev/ttyUSB0"

network = ZNetwork(device, config)

