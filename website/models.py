from django.db import models

# Create your models here.

# Autoimport only from booking.com properties dashboard, not individual property dashboard
    # Not importing from properties dashboard will cause null error for columns with #Autoimport...
# Add autoimport reminder for other third party booking websites too!

class reservation(models.Model):
    PROPERTIES = (
        ("paraiso", "Paraiso"),
        ("rosiate", "Rosiate"),
    )
    
    ROOMTYPE = (
        ("Single room", "Single room"),
        ("Double room", "Double room")
    )
    intReservationId = models.AutoField(primary_key=True)
    extReservationId = models.CharField(max_length=20, null=True)
    # Autoimport from .csv
    propertyName = models.CharField(max_length=15, choices=PROPERTIES)
    guestFirstName = models.CharField(max_length=15)
    guestLastName = models.CharField(max_length=15)
    numGuests = models.IntegerField()
    numRooms = models.IntegerField()
    bookedRoomType = models.CharField(max_length=12, choices=ROOMTYPE)
    checkInDate = models.DateField(max_length=8)
    checkOutDate = models.DateField(max_length=8)
    # Autoimport from .csv
    reservationStatus = models.CharField(max_length=15, null=True)
    totalPayment = models.DecimalField(max_digits=5, decimal_places=2)
    commission = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    # requires new workarounds to identify the website when dealing with multiple third party booking websites
    website = models.CharField(max_length=15, null=True)
    
    def __str__(self):
        return self.guestFirstName + " " + self.guestLastName + " | ID: " + str(self.intReservationId) + " | " + str(self.checkInDate) + " - " + str(self.checkOutDate)
    def numNights(self):
        return (self.checkOutDate - self.checkInDate).days

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

class roomPrices(models.Model):
    ROOMTYPE = (
        ("Single room", "Single room"),
        ("Double room", "Double room")
    )
    roomPricesID = models.AutoField(primary_key=True)
    listedWebsite = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE)
    roomType = models.CharField(max_length=12, choices=ROOMTYPE)
    roomPrice = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.listedWebsite) + ": " + str(self.roomType) + " = " + str(self.roomPrice)

class buildingRoom(models.Model):
    STATUS = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("cleaning", "Cleaning"),
    )
    ROOMSECTION = (
        ("Hotel", "Hotel"),
        ("Apartment", "Apartment")
    )
    
    roomNum = models.IntegerField(primary_key=True)
    roomFloor = models.IntegerField()
    roomType = models.ForeignKey(roomPrices, on_delete=models.CASCADE)
    roomStatus = models.CharField(max_length=15, choices=STATUS)
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE, null=True, blank=True)
    roomSection = models.CharField(max_length=10, choices=ROOMSECTION)
    propertyName = models.ForeignKey(building, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.roomNum) + " Floor " + str(self.roomFloor) + " (" + str(self.roomSection) + ") " + str(self.propertyName) + " | " + self.roomStatus

class employee(models.Model):
    employeeID = models.AutoField(primary_key=True)
    employeeFirstName = models.CharField(max_length=15)
    employeeLastName = models.CharField(max_length=15)
    employeeSalary = models.DecimalField(max_digits=5, decimal_places=2)
    accessLevel = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=10)
    
    def __str__(self):
        return self.employeeID