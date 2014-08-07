from django.contrib import admin
from device_handler.models import Network
from device_handler.models import Node

admin.site.register(Network)
admin.site.register(Node)
