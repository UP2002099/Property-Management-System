from django.core.management.base import BaseCommand
from website.models import *

# RUN ONLY WHEN REBUILDING DATABASE!!!
# OTHERWISE UPDATE ROOMS VIA THE ADMIN VIEW!
class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # Initialise bookingWebsite
        websiteList = ["Booking.com", "NOT_HOTEL"]
        for website in websiteList:
            createWebsite = bookingWebsite.objects.create(
                websiteName = website,
                roomInventory = 0
            )
            createWebsite.save()
        
        # Initialise building
        property = building.objects.create(
            propertyName = "Paraiso",
            totalRooms = 64,
            totalFloors = 5,
            listedWebsites = bookingWebsite.objects.get(websiteName = "Booking.com")
        )
        property.save()
        
        # Initialise buildingRoom
        totalFloors = 5
        allHotelRooms = [101, 102, 107, 108, 109, 110, 111, 201, 212, 302, 306, 312, 401, 403, 408, 504, 507, 508, 509]
        twinBedRoom = [102, 108, 110, 212, 408]
        singleBedRoom = list(set(allHotelRooms).symmetric_difference(set(twinBedRoom)))
        f1firstLastRoom = [101, 111]
        f2firstLastRoom = [201, 213]
        f3firstLastRoom = [301, 313]
        f4firstLastRoom = [401, 413]
        f5firstLastRoom = [501, 513]

        rows = []
        roomNum = 1

        for roomFloor in range(1, totalFloors+1):
            first, last = eval(f'f{roomFloor}firstLastRoom')
            roomNum = first
            for room in range(first, last+1):
                if room in singleBedRoom:
                    roomType = "Single Bed Room"
                    roomSection = "Hotel"
                    roomStatus = "available"
                    website = bookingWebsite.objects.get(websiteName = "Booking.com")
                elif room in twinBedRoom:
                    roomType = "Twin Bed Room"
                    roomSection = "Hotel"
                    roomStatus = "available"
                    website = bookingWebsite.objects.get(websiteName = "Booking.com")
                else:
                    roomType = ""
                    roomSection = "Apartment"
                    roomStatus = "apartment"
                    website = bookingWebsite.objects.get(websiteName = "NOT_HOTEL")
                rows.append([roomNum, roomFloor, roomType, roomStatus, website, roomSection, "Paraiso"])
                roomNum += 1

        for row in rows:
            room = buildingRoom.objects.create(
                roomNum=row[0],
                roomFloor=row[1],
                roomType=row[2],
                roomStatus=row[3],
                listedWebsites=website,
                roomSection=row[5],
                propertyName=building.objects.get(propertyName = "Paraiso")
            )
            room.save()
        
        # Initialise priceForRoomType
        roomTypePriceList = [["Single Bed Room", 1000], ["Twin Bed Room", 1000]]
        for roomType, roomPrice in roomTypePriceList:
            roomTypePrice = priceForRoomType.objects.create(
                roomType = roomType,
                roomPrice = roomPrice
            )
            roomTypePrice.save()