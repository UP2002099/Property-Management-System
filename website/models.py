from django.db import models

class bookingWebsite(models.Model):
    websiteID = models.AutoField(primary_key=True)
    websiteName = models.CharField(max_length=20)
    roomInventory = models.IntegerField(null=True)
    
    def __str__(self):
        return self.websiteName

class building(models.Model):
    propertyName = models.CharField(primary_key=True, max_length=20)
    totalRooms = models.IntegerField()
    totalFloors = models.IntegerField()
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.propertyName

class buildingRoom(models.Model):
    # 
    STATUS = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("cleaning", "Cleaning"),
        ("apartment", "Apartment")
    )
    ROOMSECTION = (
        ("Hotel", "Hotel"),
        ("Apartment", "Apartment")
    )
    ROOMTYPE = (
        ("Single Bed Room", "Single Bed Room"),
        ("Twin Bed Room", "Twin Bed Room"),
    )
    
    roomNum = models.IntegerField(primary_key=True)
    roomFloor = models.IntegerField()
    # if room type = blank, room section is apartment!
    roomType = models.CharField(max_length=25, choices=ROOMTYPE, blank=True)
    roomStatus = models.CharField(max_length=15, choices=STATUS)
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE, null=True, blank=True)
    roomSection = models.CharField(max_length=10, choices=ROOMSECTION)
    propertyName = models.ForeignKey(building, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.roomNum) + " Floor " + str(self.roomFloor) + " (" + str(self.roomSection) + ") " + str(self.propertyName) + " | " + self.roomStatus

class priceForRoomType(models.Model):
    roomPricesID = models.AutoField(primary_key=True)
    roomType = models.CharField(max_length=25, choices=buildingRoom.ROOMTYPE, null=True, blank=True)
    roomPrice = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.roomType) + " = " + str(self.roomPrice)

class bookingcomReservations(models.Model):
    intReservationId = models.AutoField(primary_key=True)
    extReservationId = models.CharField(max_length=20, null=True, blank=True)
    # Autoimport from csv
    propertyName = models.CharField(max_length=15)
    guestName = models.CharField(max_length=15)
    numGuests = models.IntegerField()
    numSingle = models.IntegerField()
    numTwin = models.IntegerField()
    roomType = models.CharField(max_length=25)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    # Autoimport from csv
    reservationStatus = models.CharField(max_length=15, null=True, blank=True)
    totalPayment = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    # requires new workarounds to identify the website when dealing with multiple third party booking websites
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE, null=True, blank=True)
    assignedRoom = models.ForeignKey(buildingRoom, null=True, blank=True, on_delete=models.SET_NULL)
    importTime = models.DateField()
    
    def __str__(self):
        return self.guestName + " | ID: " + str(self.intReservationId) + " | " + str(self.checkInDate) + " - " + str(self.checkOutDate)
    def numNights(self):
        return (self.checkOutDate - self.checkInDate).days
    
    def assignRoom(self):
        # get all available rooms of the booked type in the relevant building
        availableRooms = buildingRoom.objects.filter(
            propertyName__name=self.propertyName,
            roomType__roomType=self.assignedRoom,
            roomStatus='available'
        )

        # if there are no available rooms, return False
        if not availableRooms:
            return False

        # assign the first available room to the reservation
        assignedRoom = availableRooms.first()
        assignedRoom.roomStatus = 'unavailable'
        assignedRoom.save()
        self.assignedRoom = assignedRoom
        self.save()

        return True
    
class walkinReservations(models.Model):
    PROPERTIES = (
        ("paraiso", "Paraiso"),
    )
    
    intReservationId = models.AutoField(primary_key=True)
    propertyName = models.CharField(max_length=15, choices=PROPERTIES)
    guestFirstName = models.CharField(max_length=15)
    guestLastName = models.CharField(max_length=15)
    numGuests = models.IntegerField()
    numRooms = models.IntegerField()
    roomType = models.CharField(max_length=25, choices=buildingRoom.ROOMTYPE, null=True, blank=True)
    assignedRoom = models.ForeignKey(buildingRoom, null=True, on_delete=models.SET_NULL)
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    totalPayment = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.guestFirstName + " " + self.guestLastName + " | ID: " + str(self.intReservationId) + " | " + str(self.checkInDate) + " - " + str(self.checkOutDate)
    def numNights(self):
        return (self.checkOutDate - self.checkInDate).days
    # FOR allReservations.html reservation.website, parity with reservationModel
    def website(self):
        return ("Internal booking")

class employee(models.Model):
    employeeID = models.AutoField(primary_key=True)
    employeeFirstName = models.CharField(max_length=15)
    employeeLastName = models.CharField(max_length=15)
    employeeSalary = models.DecimalField(max_digits=5, decimal_places=2)
    accessLevel = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=10)
    
    def __str__(self):
        return self.employeeID