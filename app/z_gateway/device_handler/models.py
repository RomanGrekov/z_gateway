from django.db import models

class Network(models.Model):
    network_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Node(models.Model):
    node_id = models.IntegerField(unique=True)
    network_id = models.ForeignKey(Network, to_field='network_id', db_column='network_id')
    name = models.CharField(max_length=200)
    manufact_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.manufact_name
