from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone

import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

SERVICEBUSNAME = os.environ['SERVICEBUSNAME']
SERVICEQUEUENAME = os.environ["SERVICEQUEUENAME"]
credential = DefaultAzureCredential()

def one_workday_hence():
    return timezone.now() + timezone.timedelta(hours=1)

class VizNodeList(models.Model):

    title = models.CharField(max_length=100, unique=True)
    
    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def send_message(self):
        servicebus_client = ServiceBusClient(fully_qualified_namespace=SERVICEBUSNAME, credential=credential, logging_enable=True)
        sender = servicebus_client.get_queue_sender(queue_name=SERVICEQUEUENAME)
        message = ServiceBusMessage("Django Message")
        sender.send_messages(message)
        return self.title

    def __str__(self):
        return self.title


class VizNode(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_workday_hence)
    viznode_list = models.ForeignKey(VizNodeList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.viznode_list.id), str(self.id)]
        )

    def send_message(self):
        servicebus_client = ServiceBusClient(fully_qualified_namespace=SERVICEBUSNAME, credential=credential, logging_enable=True)
        sender = servicebus_client.get_queue_sender(queue_name=SERVICEQUEUENAME)
        message = ServiceBusMessage("Django Message")
        sender.send_messages(message)
        return 
    
    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]