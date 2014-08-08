from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import get_list_or_404

from device_handler.models import Node

import logging
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


