from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

def updateRoomInventory(website):
    website.roomInventory = buildingRoom.objects.filter(listedWebsites=website).count()
    website.save()

@receiver([post_save, post_delete], sender=buildingRoom)
def buildingRoomUpdate(sender, instance, **kwargs):
    updateRoomInventory(instance.listedWebsites)