from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(reservationModel)
admin.site.register(building)
admin.site.register(buildingRoom)
admin.site.register(employee)
admin.site.register(bookingWebsite)
admin.site.register(priceForRoomType)
admin.site.register(walkinReservationModel)