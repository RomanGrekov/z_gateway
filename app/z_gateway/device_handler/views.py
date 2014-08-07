from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_list_or_404

from device_handler.models import Node

import sys, os
sys.path.append(os.path.abspath("../"))
from start_network import ZNetwork

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hello world!")

def devices(request):
    nodes = []
    for node in get_list_or_404(Node):
        nodes.append(model_to_dict(node))
    context = {"nodes_list": nodes,
               "page_name": "Nodes"}
    return render(request, 'device_handler/device_list.html', context)

def get_network(request):
    network = ZNetwork()
    context = {"network_name": str(network.get_home_id()),
               "page_name": "Network"}
    return render(request, 'device_handler/network.html', context)
