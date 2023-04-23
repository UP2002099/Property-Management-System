from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from website.models import *
import pytz

class Command(BaseCommand):
    help = 'Assign rooms to reservations based on number of single and twin beds'

    def handle(self, *args, **options):
        today = date.today()

        # Get all reservations with check-in date today
        reservations = bookingcomReservations.objects.filter(checkInDate=today)

        # Loop through reservations and assign rooms
        for res in reservations:
            # Check if reservation already has assigned room
            assigned_rooms = AssignedRoom.objects.filter(reservation=res)
            if assigned_rooms:
                continue
            
            # Assign each bed to an available room
            assigned_rooms = []
            for _ in range(res.numSingle):
                # Find available single bed room
                room = buildingRoom.objects.filter(
                    roomType="Single Bed Room",
                    roomStatus="available",
                    roomSection="Hotel",
                ).first()
                if room:
                    # Assign room to reservation
                    AssignedRoom.objects.create(
                        reservation=res,
                        room=room,
                    )
                    # Update room status to unavailable
                    room.roomStatus = "unavailable"
                    room.save()
                    assigned_rooms.append(room)
            
            for _ in range(res.numTwin):
                # Find available twin bed room
                room = buildingRoom.objects.filter(
                    roomType="Twin Bed Room",
                    roomStatus="available",
                    roomSection="Hotel",
                ).first()
                if room:
                    # Assign room to reservation
                    AssignedRoom.objects.create(
                        reservation=res,
                        room=room,
                    )
                    # Update room status to unavailable
                    room.roomStatus = "unavailable"
                    room.save()
                    assigned_rooms.append(room)
        return
