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
        return str(self.roomNum) + " " + str(self.roomType) + " Floor " + str(self.roomFloor) + " (" + str(self.roomSection) + ") " + str(self.propertyName) + " | " + self.roomStatus

class priceForRoomType(models.Model):
    roomPricesID = models.AutoField(primary_key=True)
    roomType = models.CharField(max_length=25, choices=buildingRoom.ROOMTYPE, null=True, blank=True)
    roomPrice = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.roomType) + " = " + str(self.roomPrice)

class bookingcomReservations(models.Model):
    intReservationId = models.AutoField(primary_key=True)
    extReservationId = models.CharField(max_length=20, null=True, blank=True)
    propertyName = models.CharField(max_length=15, blank=True)
    guestName = models.CharField(max_length=30)
    numGuests = models.IntegerField()
    numSingle = models.IntegerField()
    numTwin = models.IntegerField()
    checkInDate = models.DateField()
    checkOutDate = models.DateField()
    reservationStatus = models.CharField(max_length=15, null=True, blank=True)
    totalPayment = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    commission = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE, null=True, blank=True)
    importTime = models.DateField()
    
    def __str__(self):
        return self.guestName + " | ID: " + str(self.intReservationId) + " | S: " + str(self.numSingle) + " | T: " + str(self.numTwin) + " | " + str(self.checkInDate) + " - " + str(self.checkOutDate)
    def numNights(self):
        return (self.checkOutDate - self.checkInDate).days
    
class AssignedRoom(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(bookingcomReservations, on_delete=models.CASCADE)
    room = models.ForeignKey(buildingRoom, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.reservation) + " - " + str(self.room)
    
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
    assignedRoom = models.ForeignKey(buildingRoom, null=True, blank=True, on_delete=models.SET_NULL)
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