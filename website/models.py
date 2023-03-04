from django.db import models

# Create your models here.

# Autoimport only from booking.com properties dashboard, not individual property dashboard
    # Not importing from properties dashboard will cause null error for columns with #Autoimport...
# Add autoimport reminder for other third party booking websites too!

class reservation(models.Model):
    intReservationId = models.AutoField(primary_key=True)
    extReservationId = models.CharField(max_length=20)
    # Autoimport from .csv
    propertyName = models.CharField(max_length=15)
    guestFirstName = models.CharField(max_length=15)
    guestLastName = models.CharField(max_length=15)
    numGuests = models.IntegerField()
    numRooms = models.IntegerField()
    checkInDate = models.DateField(max_length=8)
    checkOutDate = models.DateField(max_length=8)
    # Autoimport from .csv
    reservationStatus = models.CharField(max_length=15)
    totalPayment = models.DecimalField(max_digits=5, decimal_places=2)
    commission = models.DecimalField(max_digits=5, decimal_places=2)
    # requires new workarounds to identify the website when dealing with multiple third party booking websites
    website = models.CharField(max_length=15)
    
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

class buildingRoom(models.Model):
    STATUS = (
        ("Available", "Available"),
        ("Unavailable", "Unavailable"),
        ("Needs Cleaning", "Needs Cleaning"),
    )
    ROOMTYPE = (
        ("Single room", "Single room"),
        ("Double room", "Double room")
    )
    ROOMSECTION = (
        ("Hotel", "Hotel"),
        ("Apartment", "Apartment")
    )
    
    roomNum = models.IntegerField(primary_key=True)
    roomFloor = models.IntegerField()
    roomType = models.CharField(max_length=12, choices=ROOMTYPE)
    roomStatus = models.CharField(max_length=15, choices=STATUS)
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE, null=True)
    roomSection = models.CharField(max_length=10, choices=ROOMSECTION)
    
    def __str__(self):
        return self.roomNum
    
class employee(models.Model):
    employeeID = models.AutoField(primary_key=True)
    employeeFirstName = models.CharField(max_length=15)
    employeeLastName = models.CharField(max_length=15)
    employeeSalary = models.DecimalField(max_digits=5, decimal_places=2)
    accessLevel = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=10)
    
    def __str__(self):
        return self.employeeID

class building(models.Model):
    propertyName = models.CharField(primary_key=True, max_length=20)
    totalRooms = models.IntegerField()
    listedWebsites = models.ForeignKey(bookingWebsite, on_delete=models.CASCADE)
    intReservationId = models.ForeignKey(reservation, on_delete=models.CASCADE)