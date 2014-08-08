from django.shortcuts import render
from django.http import HttpResponse
import json
import logging
logger = logging.getLogger(__name__)

import sys, os
sys.path.append(os.path.abspath("../"))
from start_network import ZNetwork, Network

def index(request):
    home_id = "not known"
    network = Network()
    if network:
        if network.get_status() == 0:
            network = ZNetwork(network.network)
            home_id = network.get_home_id_str()
    context = {"network_name": home_id,
               "page_name": "Network"}
    return render(request, 'network/network.html', context)

def start_network(request):
    config = os.path.abspath("../../python-openzwave/openzwave/config")
    device = "/dev/ttyUSB0"
    timeout = 300
    Network(device, config, timeout)
    json_ = json.dumps({"resp": timeout})
    return HttpResponse(json_, mimetype='application/json')

def stop_network(request):
    network = Network()
    network.stop()
    state = ["on", "off"][network.is_stopped()]
    context = {"state": state}
    json_ = json.dumps(context)
    return HttpResponse(json_, mimetype='application/json')

def network_get_timeout(request):
    network = Network()
    try:
        timeout = network.next()
    except:
        timeout = network.get_timout()
    context = {"timeout": timeout}
    json_ = json.dumps(context)
    return HttpResponse(json_, mimetype='application/json')

def network_get_start_status(request):
    network = Network()
    context = {"status": network.get_status()}
    json_ = json.dumps(context)
    return HttpResponse(json_, mimetype='application/json')

def network_get_state(request):
    network = Network()
    if network:
        state = ["off", "on"][network.is_running()]
    else:
        state = "off"
    context = {"state": state}
    json_ = json.dumps(context)
    return HttpResponse(json_, mimetype='application/json')

def get_home_id(request):
    network = Network()
    network = ZNetwork(network.network)
    home_id = network.get_home_id_str()
    context = {"home_id": home_id}
    json_ = json.dumps(context)
    return HttpResponse(json_, mimetype='application/json')
