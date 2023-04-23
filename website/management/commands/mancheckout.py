from datetime import datetime
from django.core.management.base import BaseCommand
from website.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        # filter through bookingcomReservations and walkinReservations
        today = datetime.now().date()

        # only get reservations for checkOutDate of today or less
        guestCheckOut = bookingcomReservations.objects.filter(checkOutDate__lte=today)
        for reservation in guestCheckOut:
            try:
                assigned_room = AssignedRoom.objects.get(reservation=reservation)
                room = assigned_room.room
                room.roomStatus = 'available'
                room.save()
            except:
                assigned_room = AssignedRoom.objects.filter(reservation=reservation)
                for multi in assigned_room:
                    room = multi.room
                    room.roomStatus = 'available'
                    room.save()
            assigned_room.delete()
        
        # no try catch as walkinGuests enforced by 1 room per reservation
        walkinGuests = walkinReservations.objects.filter(checkOutDate__lte=today)
        for guest in walkinGuests:
            guest.assignedRoom.roomStatus = 'available'
            guest.assignedRoom.save()
            assigned_room.delete()
        # shutsdown heroku scheduler
        return
