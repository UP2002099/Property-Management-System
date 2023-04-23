from datetime import datetime
from django.core.management.base import BaseCommand
from website.models import *
import pytz

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Heroku scheduler runs code at 1200 thai time
        thaiTimezone = pytz.timezone('Asia/Bangkok')
        now = datetime.now(thaiTimezone)
        currentTime = now.time()
        
        # filter through bookingcomReservations and walkinReservations
        if currentTime == datetime.time(12):
            guestCheckOut = bookingcomReservations.objects.filter(checkOutDate=now.date())
            for reservation in guestCheckOut:
                assigned_room = AssignedRoom.objects.filter(reservation=reservation)
                assigned_room.roomStatus = 'cleaning'
                assigned_room.save()
            walkinGuests = walkinReservations.objects.filter(checkOutDate=now.date())
            for guest in walkinGuests:
                guest.assignedRoom.roomStatus = 'cleaning'
                guest.assignedRoom.save()
            # shutsdown heroku scheduler
            return
        
        # Heroku scheduler runs code at 1400 thai time
        if currentTime == datetime.time(14):
            # set roomStatus to 'available'
            cleaningRooms = buildingRoom.objects.filter(roomStatus='cleaning')
            for room in cleaningRooms:
                room.roomStatus = 'available'
                room.save()
            # shutsdown heroku scheduler
            return
