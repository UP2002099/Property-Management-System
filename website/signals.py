from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

def updateRoomInventory(website):
    website.roomInventory = buildingRoom.objects.filter(listedWebsites=website).count()
    website.save()

@receiver([post_save, post_delete], sender=buildingRoom)
def buildingRoomUpdate(sender, instance, **kwargs):
    updateRoomInventory(instance.listedWebsites)

# @receiver(post_save, sender=buildingRoom)
# def set_price(sender, instance, created, **kwargs):
#     if created:
#         if instance.roomType == "Single room":
#             instance.price = 1000.00
#         elif instance.roomType == "Double room":
#             instance.price = 1000.00
#         instance.save()